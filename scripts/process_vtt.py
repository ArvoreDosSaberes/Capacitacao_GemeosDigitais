#!/usr/bin/env python3
"""
Processador agentic de transcrições VTT → Markdown didático.

Pipeline multi-fase:
  1. Extrai texto limpo dos arquivos .vtt
  2. Melhora a transcrição via GPT (com bibliografia e referências cruzadas)
  3. Gera brief editorial agentic (título canônico, descrição, pontos-chave)
  4. Revisão final em chunks (elimina duplicação e truncagem)
  5. Padroniza o AULAS.md com metadados extraídos

Usa estado persistente em JSON para processamento incremental.
"""

import os
import re
import sys
import json
import hashlib
import time
import argparse
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Caminhos base
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
LIVROS_DIR = PROJECT_ROOT / "Livros e Apostilas"
LIVROS_README = LIVROS_DIR / "README.md"
AULAS_MD = PROJECT_ROOT / "AULAS.md"
STATE_FILE = PROJECT_ROOT / ".vtt_processing_state.json"
OUTPUT_SUFFIX = "_transcricao.md"

# ---------------------------------------------------------------------------
# Carrega variáveis de ambiente
# ---------------------------------------------------------------------------
ENV_FILE = PROJECT_ROOT / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

ENHANCE_ENABLED = OPENAI_API_KEY != ""
OPENAI_ENHANCEMENT_ACTIVE = ENHANCE_ENABLED

# Limites de tokens para cada fase
OPENAI_ENHANCE_MAX_TOKENS = 16_000
OPENAI_REVIEW_CHUNK_CHAR_LIMIT = 9_000
OPENAI_REVIEW_MAX_COMPLETION_TOKENS = 16_000
OPENAI_AGENTIC_BRIEF_MAX_COMPLETION_TOKENS = 4_000
MAX_CHARS_PER_CHUNK = 12_000


# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------
def log_info(message):
    print(f"ℹ️ {message}")


def log_success(message):
    print(f"✅ {message}")


def log_warn(message):
    print(f"⚠️ {message}")


def log_error(message):
    print(f"❌ {message}", file=sys.stderr)


# ---------------------------------------------------------------------------
# OpenAI error handler (centralizado)
# ---------------------------------------------------------------------------
def _handle_openai_error(exc, context_msg):
    """Trata erros da OpenAI de forma padronizada. Retorna True se desativou enhancement."""
    global OPENAI_ENHANCEMENT_ACTIVE

    error_text = str(exc)
    lower_text = error_text.lower()
    status_code = (
        getattr(exc, "status_code", None)
        or getattr(getattr(exc, "response", None), "status_code", None)
    )

    if status_code == 429 or "insufficient_quota" in lower_text:
        OPENAI_ENHANCEMENT_ACTIVE = False
        log_error(f"Cota da OpenAI esgotada (429 / insufficient_quota) durante {context_msg}.")
        return True

    if status_code == 404 or "model_not_found" in lower_text:
        log_error(f"Modelo OpenAI '{OPENAI_MODEL}' não encontrado ou sem acesso durante {context_msg}.")
        return False

    if status_code in (401, 403):
        log_error(f"Falha de autenticação/permissão na API da OpenAI durante {context_msg}.")
        return False

    log_error(f"Erro inesperado durante {context_msg}: {error_text}")
    return False


# ============================= VTT PARSING =================================

def parse_vtt(vtt_path: Path) -> str:
    """Lê um arquivo VTT e retorna apenas o texto limpo (sem timestamps)."""
    text_lines = []
    with open(vtt_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line == "WEBVTT":
                continue
            if re.match(r"^[0-9a-f\-]{36}/", line) or re.match(r"^\d+$", line):
                continue
            if re.match(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->", line):
                continue
            if not line:
                continue
            text_lines.append(line)
    return " ".join(text_lines)


def vtt_file_hash(vtt_path: Path) -> str:
    """Gera um hash curto do conteúdo do VTT para detectar mudanças."""
    content = vtt_path.read_bytes()
    return hashlib.sha256(content).hexdigest()[:16]


def vtt_state_key(vtt_path: Path) -> str:
    """Gera uma chave de estado estável baseada no caminho relativo do VTT."""
    rel = vtt_path.relative_to(PROJECT_ROOT)
    return str(rel)


# ========================= STATE MANAGEMENT ================================

def load_state() -> dict:
    """Carrega o estado das transcrições já realizadas."""
    if not STATE_FILE.exists():
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        log_warn("Arquivo de estado corrompido. Tentando recuperar…")
        try:
            raw = STATE_FILE.read_text(encoding="utf-8")
        except OSError:
            raw = ""

        recovered = _recover_state_from_text(raw)
        if recovered is not None:
            backup = STATE_FILE.with_suffix(".json.corrompido")
            try:
                if backup.exists():
                    backup.unlink()
                STATE_FILE.rename(backup)
            except OSError:
                pass
            save_state(recovered)
            log_success(f"Estado recuperado com {len(recovered)} registro(s).")
            log_warn(f"Backup do arquivo corrompido: {backup}")
            return recovered

        backup = STATE_FILE.with_suffix(".json.corrompido")
        try:
            if backup.exists():
                backup.unlink()
            STATE_FILE.rename(backup)
        except OSError:
            pass
        log_error("Não foi possível recuperar o estado. Reiniciando com estado limpo.")
        return {}


def save_state(state: dict):
    """Salva o estado das transcrições realizadas."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def _skip_json_separators(text, index):
    while index < len(text) and text[index] in " \t\r\n,":
        index += 1
    return index


def _extract_json_string(text, index):
    if index >= len(text) or text[index] != '"':
        return None, index
    escaped = False
    for pos in range(index + 1, len(text)):
        char = text[pos]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            return text[index : pos + 1], pos + 1
    return None, index


def _extract_json_object(text, index):
    if index >= len(text) or text[index] != "{":
        return None, index
    depth = 0
    in_string = False
    escaped = False
    for pos in range(index, len(text)):
        char = text[pos]
        if in_string:
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[index : pos + 1], pos + 1
    return None, index


def _recover_state_from_text(raw_state):
    """Tenta recuperar um dicionário de estado a partir de JSON corrompido."""
    if not raw_state:
        return None

    cleaned = raw_state.strip()
    repair_candidates = [
        cleaned,
        re.sub(r",(\s*[}\]])", r"\1", cleaned),
        re.sub(r",\s*$", "", cleaned),
    ]
    for candidate in repair_candidates:
        try:
            loaded = json.loads(candidate)
            if isinstance(loaded, dict):
                return loaded
        except json.JSONDecodeError:
            pass

    recovered = {}
    cursor = cleaned.find("{")
    if cursor == -1:
        return None
    cursor += 1

    while cursor < len(cleaned):
        cursor = _skip_json_separators(cleaned, cursor)
        if cursor >= len(cleaned) or cleaned[cursor] == "}":
            break
        key_token, cursor_after_key = _extract_json_string(cleaned, cursor)
        if not key_token:
            break
        try:
            key = json.loads(key_token)
        except json.JSONDecodeError:
            break
        cursor = _skip_json_separators(cleaned, cursor_after_key)
        if cursor >= len(cleaned) or cleaned[cursor] != ":":
            break
        cursor += 1
        cursor = _skip_json_separators(cleaned, cursor)
        if cursor >= len(cleaned):
            break
        value_token = None
        if cleaned[cursor] == "{":
            value_token, cursor = _extract_json_object(cleaned, cursor)
        if not value_token:
            break
        try:
            recovered[key] = json.loads(value_token)
        except json.JSONDecodeError:
            repaired = re.sub(r",(\s*[}\]])", r"\1", value_token)
            try:
                recovered[key] = json.loads(repaired)
            except json.JSONDecodeError:
                pass

    return recovered or None


# ========================= BIBLIOGRAFIA ====================================

def build_book_list() -> list[dict]:
    """Extrai uma lista estruturada de livros a partir dos arquivos na pasta."""
    books = []
    if not LIVROS_DIR.exists():
        return books
    for item in sorted(LIVROS_DIR.iterdir()):
        if item.is_file() and item.suffix.lower() in (".pdf", ".epub"):
            books.append({"filename": item.name, "title": item.stem})
    return books


def format_book_titles_for_prompt(books: list[dict], max_items: int = 60) -> str:
    """Formata títulos dos livros para inclusão no prompt."""
    return "\n".join(f"- {b['title']}" for b in books[:max_items])


# ========================= AULAS.MD PARSING ================================

def parse_aulas_md() -> list[dict]:
    """
    Analisa o AULAS.md e extrai metadados das aulas.
    Retorna lista de dicts: {section, title, description, vtt_path (relativo), vtt_abs}
    """
    if not AULAS_MD.exists():
        return []

    content = AULAS_MD.read_text(encoding="utf-8")
    aulas = []
    current_section = ""
    current_title = ""
    current_description = ""
    aula_counter = 0

    # Subheadings que NÃO representam aulas
    SKIP_SUBHEADING_KEYWORDS = (
        "Materiais", "Recursos", "Conteúdo", "Aviso", "Direitos",
        "Finalidade", "Informações", "Reposição", "Formulário",
    )

    from urllib.parse import unquote

    for line in content.split("\n"):
        stripped = line.strip()

        # ## Seção principal — também pode ser o título da aula
        if re.match(r"^##\s+", stripped) and not stripped.startswith("### "):
            current_section = re.sub(r"^##\s+", "", stripped).strip()
            # Remove emojis de prefixo tipo 📚
            clean_section = re.sub(r"^[\U0001F300-\U0001FAFF\u2600-\u27BF]+\s*", "", current_section).strip()
            # Se parece com título de aula, usa como current_title
            if re.match(r"^Aula\s+\d+", clean_section) or "Aula de Abertura" in clean_section:
                current_title = clean_section
            else:
                current_title = current_section
            current_description = ""

        # ### Subtítulo — captura como título se não for um heading auxiliar
        elif re.match(r"^###\s+", stripped):
            sub_title = re.sub(r"^###\s+", "", stripped).strip()
            clean_sub = re.sub(r"^[\U0001F300-\U0001FAFF\u2600-\u27BF]+\s*", "", sub_title).strip()
            if not any(kw in clean_sub for kw in SKIP_SUBHEADING_KEYWORDS):
                current_title = clean_sub
                current_description = ""

        # # Título de nível 1 — ignora (é o título do documento)
        elif stripped.startswith("# ") and not stripped.startswith("## "):
            pass

        # Procura links para arquivos VTT
        vtt_match = re.search(r'\[.*?\]\(([^)]*\.vtt)\)', stripped)
        if vtt_match:
            vtt_rel = unquote(vtt_match.group(1))
            vtt_abs = PROJECT_ROOT / vtt_rel

            if vtt_abs.exists():
                aula_counter += 1
                aulas.append({
                    "section": current_section,
                    "title": current_title or current_section,
                    "description": current_description,
                    "vtt_rel": vtt_rel,
                    "vtt_abs": vtt_abs,
                    "aula_number": aula_counter,
                })

        # Texto descritivo (nem heading, nem link, nem lista especial)
        elif (
            stripped
            and not stripped.startswith("#")
            and not stripped.startswith("*")
            and not stripped.startswith("-")
            and not stripped.startswith("[")
            and not stripped.startswith("!")
            and not stripped.startswith(">")
            and not stripped.startswith("---")
            and current_title
        ):
            if not current_description:
                current_description = stripped

    return aulas


def find_vtt_files(root: Path) -> list[Path]:
    """Localiza todos os arquivos .vtt no projeto, ignorando .venv, .git e scripts."""
    vtt_files = []
    for p in sorted(root.rglob("*.vtt")):
        parts = p.relative_to(root).parts
        if any(part.startswith(".") for part in parts):
            continue
        if "scripts" in parts:
            continue
        vtt_files.append(p)
    return vtt_files


def _match_vtt_to_aula(vtt_path: Path, aulas: list[dict]) -> dict | None:
    """Busca metadados do AULAS.md para um dado arquivo VTT."""
    for aula in aulas:
        if aula["vtt_abs"].resolve() == vtt_path.resolve():
            return aula
    return None


# ========================= TEXT UTILITIES ==================================

def _normalize_text_excerpt(text, max_length=220):
    if not text:
        return ""
    cleaned = " ".join(line.strip() for line in text.splitlines() if line.strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if len(cleaned) <= max_length:
        return cleaned
    cut = cleaned[:max_length].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return f"{cut}..." if cut else cleaned[:max_length].rstrip()


def _combine_text_segments(*segments):
    """Concatena partes textuais não vazias com separação de parágrafo."""
    parts = []
    for seg in segments:
        if seg:
            text = str(seg).strip()
            if text:
                parts.append(text)
    return "\n\n".join(parts)


def _strip_code_fences(text):
    text = (text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:markdown|md|text|json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _parse_openai_json_object(text):
    """Converte uma resposta da OpenAI em dict JSON, aceitando fences e ruído ao redor."""
    cleaned = _strip_code_fences(text)
    if not cleaned:
        return None
    candidates = [cleaned]
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidates.append(cleaned[start : end + 1])
    for candidate in candidates:
        try:
            loaded = json.loads(candidate)
            if isinstance(loaded, dict):
                return loaded
        except json.JSONDecodeError:
            continue
    return None


# ========================= CHUNKING ========================================

def split_text_into_chunks(text: str, max_chars: int = MAX_CHARS_PER_CHUNK) -> list[str]:
    """Divide texto plano em blocos respeitando limites de palavras."""
    words = text.split()
    chunks = []
    current: list[str] = []
    current_len = 0
    for word in words:
        wlen = len(word) + 1
        if current_len + wlen > max_chars and current:
            chunks.append(" ".join(current))
            current = []
            current_len = 0
        current.append(word)
        current_len += wlen
    if current:
        chunks.append(" ".join(current))
    return chunks


def _split_markdown_block(block, max_chars):
    """Divide um bloco longo de Markdown preservando ao máximo a estrutura."""
    block = block.strip()
    if not block:
        return []
    lines = [line.rstrip() for line in block.splitlines()]
    if len(lines) <= 1:
        words = block.split()
        if not words:
            return []
        chunks = []
        current_words = []
        current_len = 0
        for word in words:
            tentative = len(word) if not current_words else current_len + 1 + len(word)
            if current_words and tentative > max_chars:
                chunks.append(" ".join(current_words).strip())
                current_words = [word]
                current_len = len(word)
            else:
                current_words.append(word)
                current_len = tentative
        if current_words:
            chunks.append(" ".join(current_words).strip())
        return [c for c in chunks if c]

    chunks = []
    current_lines = []
    current_len = 0
    for line in lines:
        line_len = len(line)
        tentative = line_len if not current_lines else current_len + 1 + line_len
        if current_lines and tentative > max_chars:
            chunks.append("\n".join(current_lines).strip())
            current_lines = [line]
            current_len = line_len
        else:
            current_lines.append(line)
            current_len = tentative
    if current_lines:
        chunks.append("\n".join(current_lines).strip())
    return [c for c in chunks if c]


def _split_markdown_into_chunks(text, max_chars):
    """Divide Markdown em chunks por blocos, sem overlap, para evitar repetição."""
    normalized = re.sub(r"\n{3,}", "\n\n", text.strip())
    if not normalized:
        return []
    blocks = [b.strip() for b in re.split(r"\n\s*\n", normalized) if b.strip()]
    chunks = []
    current_blocks = []
    current_len = 0

    def flush():
        nonlocal current_blocks, current_len
        if current_blocks:
            chunks.append("\n\n".join(current_blocks).strip())
            current_blocks = []
            current_len = 0

    for block in blocks:
        if len(block) > max_chars:
            flush()
            chunks.extend(_split_markdown_block(block, max_chars))
            continue
        block_len = len(block)
        tentative = block_len if not current_blocks else current_len + 2 + block_len
        if current_blocks and tentative > max_chars:
            flush()
        current_blocks.append(block)
        current_len = len("\n\n".join(current_blocks))

    flush()
    return chunks or [normalized]


# ========================= FASE 1: ENHANCE =================================

ENHANCE_SYSTEM_PROMPT = """\
Você é um assistente educacional especializado em criar material didático de alta qualidade \
a partir de transcrições de aulas universitárias sobre Gêmeos Digitais, IA, IoT e tecnologias relacionadas. \
Seu objetivo é transformar transcrições brutas (que podem conter erros de fala, repetições e \
informalidades) em textos corridos, fluidos, didáticos e bem estruturados em Markdown.

Diretrizes:
1. **Reescreva** o conteúdo de forma corrida, eliminando repetições, vícios de linguagem e \
   erros típicos de transcrição automática.
2. **Amplie bastante** o texto com explicações adicionais que ajudem o leitor a compreender os \
   conceitos mencionados na aula, sem inventar informações falsas.
3. **Estruture** o texto com títulos (####) e subtítulos (#####) apenas quando isso melhorar a leitura.
4. **Adicione contexto** técnico e teórico relevante para enriquecer a compreensão.
5. **Faça referências cruzadas** entre os temas abordados, indicando conexões com outras \
   disciplinas ou áreas do conhecimento do programa de Gêmeos Digitais.
6. **Sugira leituras complementares** da bibliografia fornecida, inserindo-as naturalmente \
   ao longo do texto quando um tema for mencionado. Use o formato: \
   📖 *Leitura recomendada: "Título do Livro" — Autor*
7. Mantenha o tom acadêmico porém acessível, como um bom livro-texto.
8. Preserve nomes de pessoas, instituições e tecnologias mencionadas na aula.
9. Evite excesso de listas; use listas apenas quando realmente ajudarem na compreensão.
10. Destaque os pontos mais importantes ao longo do texto com **negrito**.
11. Ao final, inclua "##### Pontos-Chave" com um resumo objetivo em tópicos.
12. Inclua uma seção "## Referências Bibliográficas" listando todos os livros recomendados.
13. Escreva inteiramente em **português brasileiro**.
"""


def enhance_transcription(raw_text, title, description, section, book_titles, chunk_index=0, total_chunks=1):
    """Fase 1: Melhora a transcrição bruta via GPT com referências bibliográficas."""
    global OPENAI_ENHANCEMENT_ACTIVE

    if not ENHANCE_ENABLED or not OPENAI_ENHANCEMENT_ACTIVE:
        log_warn("Melhoria via OpenAI desativada. Mantendo transcrição bruta.")
        return None

    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    chunk_info = ""
    if total_chunks > 1:
        chunk_info = (
            f"\n\n> Esta é a **parte {chunk_index + 1} de {total_chunks}** da transcrição. "
            f"Mantenha a continuidade narrativa."
        )

    user_prompt = f"""\
Seção do curso: {section}
Título da aula: {title}
Descrição: {description}
{chunk_info}

Transcrição bruta da aula (extraída de arquivo VTT):
---
{raw_text}
---

Bibliografia disponível no curso (para sugestões de leitura):
---
{book_titles}
---

Transforme esta transcrição em conteúdo didático em Markdown, \
ampliando bastante as explicações, usando estilo corrido e linguagem clara e fluida. \
Organize em capítulos e subcapítulos apenas quando isso melhorar a leitura, \
destaque os pontos mais importantes ao longo do texto e sugira leituras da bibliografia."""

    log_info(f"Fase 1 — Melhorando transcrição via OpenAI ({OPENAI_MODEL})…")
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": ENHANCE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_completion_tokens=OPENAI_ENHANCE_MAX_TOKENS,
        )
        enhanced = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if response.usage else "?"
        log_success(f"Melhoria concluída ({len(enhanced)} caracteres, {tokens_used} tokens).")
        return enhanced
    except Exception as exc:
        _handle_openai_error(exc, "melhoria da transcrição")
        return None


# ========================= FASE 2: AGENTIC BRIEF ===========================

def _fallback_agentic_brief(aula_meta, raw_text, enhanced_text):
    """Gera brief local quando a OpenAI não estiver disponível."""
    base_title = (aula_meta.get("title") or "").strip() if aula_meta else ""
    aula_number = aula_meta.get("aula_number") if aula_meta else None

    if re.match(r"^Aula\s+\d+\s+-\s+.+", base_title):
        canonical_title = base_title
    elif aula_number:
        canonical_title = f"Aula {aula_number}"
        if base_title and not re.match(r"^Aula\s+\d+\s*$", base_title):
            canonical_title = f"Aula {aula_number} - {base_title}"
    else:
        canonical_title = base_title or "Aula"

    desc_source = _combine_text_segments(
        aula_meta.get("description", "") if aula_meta else "",
        _normalize_text_excerpt(enhanced_text or raw_text, 260),
    )
    aulas_description = _normalize_text_excerpt(desc_source, 260)

    transcription_intro = _normalize_text_excerpt(
        (aula_meta.get("description") if aula_meta else "")
        or enhanced_text
        or raw_text,
        220,
    )

    key_points = []
    if aula_meta and aula_meta.get("section"):
        key_points.append(aula_meta["section"])

    return {
        "canonical_title": canonical_title,
        "aulas_description": aulas_description,
        "transcription_intro": transcription_intro,
        "key_points": key_points,
        "source": "fallback",
    }


def build_agentic_lesson_brief(aula_meta, raw_text, enhanced_text):
    """Fase 2: Sintetiza contexto editorial da aula em JSON estruturado via GPT."""
    global OPENAI_ENHANCEMENT_ACTIVE

    fallback = _fallback_agentic_brief(aula_meta, raw_text, enhanced_text)

    if not ENHANCE_ENABLED or not OPENAI_ENHANCEMENT_ACTIVE:
        return fallback

    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_prompt = """Você é um agente editorial técnico que opera em múltiplas etapas.
Sua função é sintetizar metadados de aula em um brief curto e confiável para atualizar documentos do curso.

Regras:
1. Não invente fatos.
2. Prefira a transcrição enriquecida como fonte principal.
3. Preserve o número da aula no título quando fizer sentido.
4. Retorne somente JSON válido, sem markdown, sem blocos de código e sem explicações.
5. Use português brasileiro."""

    section = aula_meta.get("section", "") if aula_meta else ""
    aula_number = aula_meta.get("aula_number", "") if aula_meta else ""
    title = aula_meta.get("title", "") if aula_meta else ""
    description = aula_meta.get("description", "") if aula_meta else ""

    # Limita o tamanho do texto enviado ao brief
    source_text = _normalize_text_excerpt(enhanced_text or raw_text, 3000)

    user_prompt = f"""\
Seção: {section}
Número da aula: {aula_number}
Título atual: {title}
Descrição: {description}

Transcrição enriquecida (trecho):
---
{source_text}
---

Crie um JSON com as chaves:
- canonical_title: título padronizado da aula
- aulas_description: 1 a 3 frases para o arquivo AULAS.md
- transcription_intro: 1 frase curta de contexto para a abertura da transcrição
- key_points: lista com 3 a 6 tópicos curtos
- source: valor curto indicando se o conteúdo veio de transcription ou mixed

Se houver qualquer dúvida, mantenha o texto factual e objetivo."""

    log_info(f"Fase 2 — Agente editorial: sintetizando brief via OpenAI ({OPENAI_MODEL})…")
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_completion_tokens=OPENAI_AGENTIC_BRIEF_MAX_COMPLETION_TOKENS,
        )
        brief = _parse_openai_json_object(response.choices[0].message.content)
        if not brief:
            log_warn("Não foi possível interpretar o brief da OpenAI. Usando fallback.")
            return fallback

        normalized = {
            "canonical_title": (brief.get("canonical_title") or fallback["canonical_title"]).strip(),
            "aulas_description": _normalize_text_excerpt(
                brief.get("aulas_description") or fallback["aulas_description"], 260
            ),
            "transcription_intro": _normalize_text_excerpt(
                brief.get("transcription_intro") or fallback["transcription_intro"], 220
            ),
            "key_points": (
                brief.get("key_points")
                if isinstance(brief.get("key_points"), list)
                else fallback["key_points"]
            ),
            "source": (brief.get("source") or fallback["source"]).strip(),
        }
        tokens_used = response.usage.total_tokens if response.usage else "?"
        log_success(f"Brief editorial: '{normalized['canonical_title']}' ({tokens_used} tokens).")
        return normalized
    except Exception as exc:
        _handle_openai_error(exc, "brief editorial da aula")
        return fallback


# ========================= FASE 3: REVIEW ==================================

def review_transcription_chunk(raw_chunk, title, description, section, chunk_index, total_chunks):
    """Fase 3: Revisa um chunk sem repetir conteúdo de outros chunks."""
    global OPENAI_ENHANCEMENT_ACTIVE

    if not ENHANCE_ENABLED or not OPENAI_ENHANCEMENT_ACTIVE:
        return None

    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_prompt = """Você é um revisor final de conteúdo didático em Markdown.

Sua tarefa é revisar apenas um trecho de uma única aula, que faz parte de uma revisão em chunks sequenciais.

Regras:
1. Trabalhe somente com o trecho fornecido.
2. Não repita conteúdo de outros chunks, nem adicione introduções ou despedidas.
3. Preserve o estilo corrido, expandindo apenas quando isso melhorar a didática.
4. Corrija repetições, truncagens e trechos confusos, mantendo a coerência.
5. Preserve a estrutura Markdown já existente quando ela fizer sentido.
6. Não invente informações novas.
7. Responda somente com o Markdown revisado do trecho atual.
8. Use português brasileiro."""

    user_prompt = f"""\
Seção do curso: {section}
Título da aula: {title}
Descrição: {description}

Você está revisando o trecho {chunk_index}/{total_chunks} desta aula.

Trecho atual:
---
{raw_chunk}
---

Revisar apenas este trecho, sem repetir trechos anteriores ou posteriores. \
Se houver uma boa forma de reduzir duplicação ou melhorar a fluidez, faça isso sem alterar o sentido."""

    log_info(f"Fase 3 — Revisão final ({OPENAI_MODEL}) chunk {chunk_index}/{total_chunks}…")
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_completion_tokens=OPENAI_REVIEW_MAX_COMPLETION_TOKENS,
        )
        reviewed = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if response.usage else "?"
        log_success(f"Chunk {chunk_index}/{total_chunks} revisado ({len(reviewed)} chars, {tokens_used} tokens).")
        return reviewed
    except Exception as exc:
        _handle_openai_error(exc, f"revisão final do chunk {chunk_index}/{total_chunks}")
        return None


def review_lesson_content(content, title, description, section):
    """Revisa o conteúdo completo de uma aula em chunks sem overlap."""
    if not ENHANCE_ENABLED or not OPENAI_ENHANCEMENT_ACTIVE:
        return None

    chunks = _split_markdown_into_chunks(content, OPENAI_REVIEW_CHUNK_CHAR_LIMIT)
    if not chunks:
        return None

    log_info(f"Revisão final de '{title}' em {len(chunks)} chunk(s).")

    reviewed_chunks = []
    for idx, chunk in enumerate(chunks, 1):
        reviewed = review_transcription_chunk(chunk, title, description, section, idx, len(chunks))
        reviewed_chunks.append((reviewed or chunk).strip())

    return "\n\n".join(c for c in reviewed_chunks if c).strip()


# ========================= AULAS.MD STANDARDIZATION ========================

def _build_aulas_standardization_draft(aulas_with_briefs):
    """Constrói rascunho padronizado do AULAS.md baseado nos briefs."""
    lines = ["# Aulas do Curso - Gêmeos Digitais", ""]
    current_section = ""

    for entry in aulas_with_briefs:
        section = entry.get("section", "")
        if section and section != current_section:
            current_section = section
            lines.append(f"## {current_section}")
            lines.append("")

        title = entry.get("canonical_title") or entry.get("title", "")
        description = entry.get("aulas_description") or entry.get("description", "")
        vtt_rel = entry.get("vtt_rel", "")

        lines.append(f"### {title}")
        lines.append("")
        if description:
            lines.append(description)
            lines.append("")
        if vtt_rel:
            from urllib.parse import quote
            vtt_encoded = quote(vtt_rel, safe="/")
            lines.append(f"- **[Transcrição VTT]({vtt_encoded})**")
            # Adiciona link para o MD gerado se existir
            md_name = Path(vtt_rel).stem + OUTPUT_SUFFIX
            md_rel = str(Path(vtt_rel).parent / md_name)
            md_encoded = quote(md_rel, safe="/")
            lines.append(f"- **[Resumo Didático]({md_encoded})**")
            lines.append("")

    return "\n".join(lines).strip() + "\n"


def standardize_aulas_md(state):
    """Padroniza o AULAS.md com metadados dos briefs editoriais."""
    if not AULAS_MD.exists():
        log_warn(f"AULAS.md não encontrado: {AULAS_MD}")
        return

    original = AULAS_MD.read_text(encoding="utf-8")
    aulas = parse_aulas_md()
    if not aulas:
        return

    needs_update = False
    enriched_aulas = []

    for aula in aulas:
        key = vtt_state_key(aula["vtt_abs"])
        entry = state.get(key, {})
        enriched = dict(aula)

        canonical = entry.get("canonical_title", "")
        aulas_desc = entry.get("aulas_description", "")

        if canonical:
            enriched["canonical_title"] = canonical
        if aulas_desc:
            enriched["aulas_description"] = aulas_desc

        if canonical and canonical != aula.get("title", ""):
            needs_update = True
        if aulas_desc and aulas_desc != aula.get("description", ""):
            needs_update = True

        enriched_aulas.append(enriched)

    if not needs_update:
        log_info("AULAS.md já está atualizado.")
        return

    if ENHANCE_ENABLED and OPENAI_ENHANCEMENT_ACTIVE:
        gpt_result = _standardize_aulas_via_gpt(original, enriched_aulas)
        if gpt_result:
            standardized = gpt_result
        else:
            standardized = _build_aulas_standardization_draft(enriched_aulas)
    else:
        standardized = _build_aulas_standardization_draft(enriched_aulas)

    if standardized.strip() != original.strip():
        backup = AULAS_MD.with_suffix(".md.bak")
        backup.write_text(original, encoding="utf-8")
        AULAS_MD.write_text(standardized, encoding="utf-8")
        log_success(f"AULAS.md padronizado e atualizado. Backup: {backup.name}")


def _standardize_aulas_via_gpt(original_content, aulas):
    """Usa GPT para padronizar o AULAS.md preservando URLs e estrutura."""
    global OPENAI_ENHANCEMENT_ACTIVE

    if not ENHANCE_ENABLED or not OPENAI_ENHANCEMENT_ACTIVE:
        return None

    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    payload = []
    for a in aulas:
        payload.append({
            "section": a.get("section", ""),
            "aula_number": a.get("aula_number", ""),
            "current_title": a.get("title", ""),
            "canonical_title": a.get("canonical_title", ""),
            "current_description": a.get("description", ""),
            "aulas_description": a.get("aulas_description", ""),
            "vtt_rel": a.get("vtt_rel", ""),
        })

    draft = _build_aulas_standardization_draft(aulas)

    system_prompt = """Você é um editor técnico de Markdown.
Sua tarefa é padronizar o arquivo AULAS.md sem alterar a ordem das aulas nem os URLs/links.

Regras:
1. Preserve o conteúdo factual e todos os links existentes.
2. Corrija ortografia, gramática e capitalização.
3. Padronize o formato com # Aulas, ## Seção e ### Aula N - Título.
4. Para aulas incompletas, use os metadados fornecidos como referência.
5. Mantenha descrições curtas e claras.
6. Não invente novos links ou aulas.
7. Preserve seções de avisos, direitos de uso e informações adicionais.
8. Responda somente com o Markdown final, sem explicações."""

    user_prompt = f"""Arquivo atual:
---
{original_content}
---

Rascunho padronizado sugerido:
---
{draft}
---

Metadados das aulas:
---
{json.dumps(payload, ensure_ascii=False, indent=2)}
---

Use o rascunho como base e devolva uma versão final padronizada do AULAS.md."""

    log_info(f"Padronizando AULAS.md via OpenAI ({OPENAI_MODEL})…")
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_completion_tokens=OPENAI_REVIEW_MAX_COMPLETION_TOKENS,
        )
        standardized = _strip_code_fences(response.choices[0].message.content)
        tokens_used = response.usage.total_tokens if response.usage else "?"
        log_success(f"Padronização do AULAS.md concluída ({len(standardized)} chars, {tokens_used} tokens).")
        return standardized
    except Exception as exc:
        _handle_openai_error(exc, "padronização do AULAS.md")
        return None


# ========================= OUTPUT GENERATION ===============================

def output_path_for_vtt(vtt_path: Path) -> Path:
    """Determina o caminho do arquivo .md de saída para um dado .vtt."""
    return vtt_path.with_name(vtt_path.stem + OUTPUT_SUFFIX)


def build_output_markdown(vtt_path, canonical_title, transcription_intro, enhanced_content, brief):
    """Monta o documento Markdown final para uma aula."""
    title = canonical_title or vtt_path.stem

    header = f"# {title}\n\n"
    header += (
        "> 📝 Material gerado a partir da transcrição da aula, "
        "revisado e ampliado com auxílio de IA para fins didáticos.\n"
        ">\n"
        f"> 📂 Arquivo de origem: `{vtt_path.name}`\n"
    )
    if transcription_intro:
        header += f">\n> {transcription_intro}\n"
    header += "\n---\n\n"

    body = enhanced_content or ""

    # Adiciona pontos-chave do brief se não estiverem já no texto
    if brief and brief.get("key_points") and "Pontos-Chave" not in body:
        body += "\n\n##### Pontos-Chave\n\n"
        for kp in brief["key_points"]:
            body += f"- {kp}\n"

    return header + body + "\n"


# ========================= MAIN PIPELINE ===================================

def process_single_vtt(vtt_path: Path, aula_meta: dict | None, book_titles: str, state: dict, force: bool) -> bool:
    """Pipeline completo de processamento de um arquivo VTT."""
    global OPENAI_ENHANCEMENT_ACTIVE

    key = vtt_state_key(vtt_path)
    entry = state.get(key, {})
    file_hash = vtt_file_hash(vtt_path)
    out_path = output_path_for_vtt(vtt_path)

    # Verifica se precisa processar
    already_enhanced = "enhanced" in entry
    already_reviewed = entry.get("reviewed", False)
    same_hash = entry.get("file_hash") == file_hash

    if same_hash and already_enhanced and already_reviewed and out_path.exists() and not force:
        log_info(f"⏭  Já processado: {vtt_path.name}")
        return False

    print(f"\n🎬 Processando: {vtt_path.relative_to(PROJECT_ROOT)}")

    section = aula_meta.get("section", "") if aula_meta else ""
    title = aula_meta.get("title", vtt_path.stem) if aula_meta else vtt_path.stem
    description = aula_meta.get("description", "") if aula_meta else ""

    # --- Fase 0: Extração do texto do VTT ---
    if not same_hash or "raw_text" not in entry:
        raw_text = parse_vtt(vtt_path)
        if not raw_text.strip():
            log_warn(f"Arquivo VTT vazio: {vtt_path.name}")
            return False
        log_info(f"Texto extraído: {len(raw_text)} caracteres")
        entry["raw_text"] = raw_text
        entry["file_hash"] = file_hash
    else:
        raw_text = entry["raw_text"]
        log_info(f"Texto em cache: {len(raw_text)} caracteres")

    # --- Fase 1: Enhancement ---
    if not already_enhanced or not same_hash or force:
        chunks = split_text_into_chunks(raw_text)
        log_info(f"Dividido em {len(chunks)} chunk(s) para enhancement.")
        enhanced_parts = []
        for i, chunk in enumerate(chunks):
            result = enhance_transcription(
                chunk, title, description, section, book_titles,
                chunk_index=i, total_chunks=len(chunks),
            )
            if result:
                enhanced_parts.append(result)
            else:
                enhanced_parts.append(chunk)

        enhanced = "\n\n".join(enhanced_parts)
        entry["enhanced"] = enhanced
        entry["reviewed"] = False  # reset review flag
        save_state(state)
        log_success(f"Fase 1 concluída: {len(enhanced)} caracteres melhorados.")
    else:
        enhanced = entry["enhanced"]
        log_info("Enhancement em cache.")

    # --- Fase 2: Agentic Brief ---
    brief = build_agentic_lesson_brief(aula_meta, raw_text, enhanced)
    if brief:
        entry["agentic"] = brief
        entry["canonical_title"] = brief.get("canonical_title", title)
        entry["aulas_description"] = brief.get("aulas_description", "")
        entry["transcription_intro"] = brief.get("transcription_intro", "")
        save_state(state)

    # --- Fase 3: Revisão Final ---
    if not entry.get("reviewed", False) or force:
        reviewed = review_lesson_content(enhanced, title, description, section)
        if reviewed:
            entry["enhanced"] = reviewed
            entry["reviewed"] = True
            enhanced = reviewed
            save_state(state)
            log_success("Fase 3 concluída: revisão final aplicada.")
        else:
            entry["reviewed"] = False
    else:
        log_info("Revisão final em cache.")

    # --- Gerar arquivo .md ---
    canonical_title = entry.get("canonical_title", title)
    transcription_intro = entry.get("transcription_intro", "")
    content = build_output_markdown(vtt_path, canonical_title, transcription_intro, enhanced, brief)
    out_path.write_text(content, encoding="utf-8")
    log_success(f"Salvo: {out_path.relative_to(PROJECT_ROOT)} ({len(content)} caracteres)")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Processador agentic de transcrições VTT → Markdown didático."
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Reprocessa tudo, ignorando cache e estado.",
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Processa apenas o arquivo VTT especificado.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas lista os arquivos VTT encontrados sem processá-los.",
    )
    parser.add_argument(
        "--skip-standardize",
        action="store_true",
        help="Pula a padronização do AULAS.md.",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("🚀 Processador Agentic de Transcrições VTT → Markdown")
    print("=" * 60)

    if not OPENAI_API_KEY:
        log_error("OPENAI_API_KEY não definida. Configure o arquivo .env")
        sys.exit(1)

    log_info(f"Modelo: {OPENAI_MODEL}")
    log_info(f"Projeto: {PROJECT_ROOT}")

    # Carregar bibliografia
    books = build_book_list()
    book_titles = format_book_titles_for_prompt(books)
    log_info(f"Bibliografia carregada: {len(books)} livros/apostilas")

    # Carregar estado
    state = load_state()
    log_info(f"Estado carregado: {len(state)} registro(s)")

    # Parsear AULAS.md
    aulas_meta = parse_aulas_md()
    log_info(f"Aulas no AULAS.md: {len(aulas_meta)}")

    # Localizar VTTs
    if args.file:
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = PROJECT_ROOT / file_path
        if not file_path.exists():
            log_error(f"Arquivo não encontrado: {file_path}")
            sys.exit(1)
        vtt_files = [file_path]
    else:
        vtt_files = find_vtt_files(PROJECT_ROOT)

    log_info(f"Arquivos VTT encontrados: {len(vtt_files)}")

    if args.dry_run:
        for vtt in vtt_files:
            key = vtt_state_key(vtt)
            out = output_path_for_vtt(vtt)
            md_exists = "✅ md existe" if out.exists() else "❌ md não existe"
            state_exists = "✅ no estado" if key in state else "❌ sem estado"
            reviewed = "✅ revisado" if state.get(key, {}).get("reviewed") else "❌ não revisado"
            meta = _match_vtt_to_aula(vtt, aulas_meta)
            title = meta["title"] if meta else vtt.stem
            log_info(f"  [{title}] {vtt.relative_to(PROJECT_ROOT)}")
            log_info(f"    → {out.name} ({md_exists}, {state_exists}, {reviewed})")
        return

    # Processar
    processed = 0
    skipped = 0
    errors = 0

    for vtt in vtt_files:
        try:
            meta = _match_vtt_to_aula(vtt, aulas_meta)
            if process_single_vtt(vtt, meta, book_titles, state, force=args.force):
                processed += 1
            else:
                skipped += 1
        except KeyboardInterrupt:
            log_warn("Interrompido pelo usuário. Salvando estado…")
            save_state(state)
            sys.exit(130)
        except Exception as exc:
            log_error(f"Erro ao processar {vtt.name}: {exc}")
            import traceback
            traceback.print_exc()
            errors += 1

    # Padronizar AULAS.md
    if not args.skip_standardize and processed > 0:
        print(f"\n{'=' * 60}")
        log_info("Padronizando AULAS.md com metadados editoriais…")
        try:
            standardize_aulas_md(state)
        except Exception as exc:
            log_error(f"Erro ao padronizar AULAS.md: {exc}")

    print(f"\n{'=' * 60}")
    log_success(f"Concluído: {processed} processados, {skipped} pulados, {errors} erros")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_warn("Execução interrompida. Encerrando com segurança…")
        sys.exit(130)
