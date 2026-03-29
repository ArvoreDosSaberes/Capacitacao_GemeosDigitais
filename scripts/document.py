#!/usr/bin/env python3
"""
Conversor de Documentos para Markdown com Busca Semântica

Este script converte PDF, EPUB, Djvu e outros formatos para Markdown,
extrai embeddings semânticos e permite busca por conteúdo.

Uso:
    python document.py --convert arquivo.pdf
    python document.py --search "termo de busca"
    python document.py --convert-all ./pasta
    python document.py -i  # modo interativo
"""

import os
import sys
import re
import argparse
import json
import hashlib
import signal
import string
import random
import sqlite3
import chromadb
from pathlib import Path
from typing import List, Dict, Any, Optional
import subprocess
import shutil
from datetime import datetime
import time
from dotenv import load_dotenv

# Importações para processamento de documentos
print("🔄 Carregando bibliotecas de processamento de documentos...")
try:
    import fitz  # PyMuPDF
    print("  ✅ PyMuPDF carregado")
    import ebooklib
    from ebooklib import epub
    print("  ✅ Ebooklib carregado")
    import pytesseract
    print("  ✅ Pytesseract carregado")
    from PIL import Image
    print("  ✅ PIL carregado")
    import pdf2image
    print("  ✅ PDF2Image carregado")
    import markdownify
    print("  ✅ Markdownify carregado")
    from bs4 import BeautifulSoup
    print("  ✅ BeautifulSoup carregado")
    print("📚 Bibliotecas de processamento carregadas com sucesso!")
except ImportError as e:
    print(f"Erro: Biblioteca necessária não encontrada: {e}")
    print("Instale as dependências com: pip install -r requirements.txt")
    sys.exit(1)

# Importações para embeddings e busca semântica
print("🔄 Carregando bibliotecas de embeddings e busca semântica...")
try:
    import numpy as np
    print("  ✅ NumPy carregado")
    print("  ⏳ Carregando SentenceTransformer...")
    from sentence_transformers import SentenceTransformer
    print("  ✅ SentenceTransformers carregado")
    import ollama
    print("  ✅ Ollama carregado")
    print("🧠 Bibliotecas de embeddings carregadas com sucesso!")
except ImportError as e:
    print(f"Erro: Biblioteca necessária não encontrada: {e}")
    print("Instale as dependências com: pip install -r requirements.txt")
    sys.exit(1)


class DocumentConverter:
    def __init__(self, data_dir: str = ".data", embedding_model: str = "mxbai-embed-large", 
                 converted_dir: str = None, tesseract_lang: str = "por", 
                 chunk_size: int = 500, chunk_overlap: int = 50):
        # Carregar variáveis de ambiente do .env
        load_dotenv()
        
        # Sobrescrever com variáveis de ambiente se existirem
        data_dir_env = os.getenv('DATA_DIR', data_dir)
        self.data_dir = Path(data_dir_env).expanduser().resolve()
        # embedding_model from constructor (CLI) has priority over env var
        self.embedding_model = embedding_model or os.getenv('OLLAMA_MODEL', 'mxbai-embed-large')
        self.tesseract_lang = os.getenv('TESSERACT_LANG', tesseract_lang)
        self.chunk_size = int(os.getenv('CHUNK_SIZE', str(chunk_size)))
        self.chunk_overlap = int(os.getenv('CHUNK_OVERLAP', str(chunk_overlap)))
        self.similarity_threshold = float(os.getenv('SIMILARITY_THRESHOLD', '0.3'))
        
        # Configurar pasta de documentos convertidos
        if converted_dir:
            self.docs_dir = Path(converted_dir).expanduser().resolve()
        else:
            # Padrão: pasta converteds em Livros e Apostilas (relativo ao script)
            converted_dir_env = os.getenv('CONVERTED_DIR')
            if converted_dir_env:
                self.docs_dir = Path(converted_dir_env).expanduser().resolve()
            else:
                # Obter diretório do script e construir caminho absoluto
                script_dir = Path(__file__).parent.parent
                self.docs_dir = (script_dir / "Livros e Apostilas" / "converteds").expanduser().resolve()
        
        self.data_dir.mkdir(exist_ok=True)
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        print("📁 Diretórios criados/verificados com sucesso!")
        
        # Controle de interrupção
        self.interrupted = False
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        print("🛡️  Handlers de sinal configurados!")
        
        # Configurar logging
        print("📋 Configurando sistema de logging...")
        self._setup_logging()
        
        # Configurar bancos de dados
        print("🗄️  Configurando bancos de dados...")
        self._setup_databases()
        print("✅ Inicialização concluída!")
    
    def _signal_handler(self, signum, frame):
        """Handler para interrupção graciosa."""
        print(f"\n{'='*60}")
        print("⚠️  Interrupção detectada! Finalizando gracefulmente...")
        print("📁 Arquivos já processados foram salvos")
        print("🔄 Você pode continuar de onde parou")
        print(f"{'='*60}")
        self.interrupted = True
    
    def _setup_logging(self):
        """Configura sistema de logging."""
        self.log_file = self.data_dir / f"converter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.start_time = time.time()
        
        # Inicializar chroma_path aqui para poder usar no alerta
        self.chroma_path = self.data_dir / "chroma_db"
        
        print(f"📋 Log iniciado: {self.log_file}")
        print(f"🎯 Pasta de saída: {self.docs_dir}")
        print(f"🤖 Modelo embeddings: {self.embedding_model}")
        print(f"🌐 Idioma OCR: {self.tesseract_lang}")
        print(f"📏 Chunk size: {self.chunk_size}")
        print(f"🔄 Chunk overlap: {self.chunk_overlap}")
        print(f"🎯 Similarity threshold: {self.similarity_threshold}")
        
        # Alerta sobre modelo de embeddings
        if self.chroma_path.exists() and any(self.chroma_path.iterdir()):
            print(f"⚠️  **ATENÇÃO**: Base de embeddings já existe em {self.chroma_path}")
            print(f"⚠️  Para trocar de modelo, apague o diretório .data e recrie com novo modelo")
            print(f"⚠️  Modelo atual: {self.embedding_model}")
        
        print(f"{'='*60}")
    
    def _log(self, message: str, level: str = "INFO"):
        """Registra mensagem no log e console."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        
        # Salvar no arquivo
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
        
        # Exibir no console
        print(log_entry)
    
    def _show_progress(self, current: int, total: int, prefix: str = "", suffix: str = ""):
        """Mostra barra de progresso."""
        if total == 0:
            return
            
        percent = (current / total) * 100
        filled_length = int(50 * current // total)
        bar = '█' * filled_length + '-' * (50 - filled_length)
        
        print(f'\r{prefix} |{bar}| {percent:.1f}% {current}/{total} {suffix}', end='', flush=True)
        
        if current == total:
            print()  # Nova linha ao completar
    
    def _format_time(self, seconds: float) -> str:
        """Formata tempo em formato legível."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
    
    def _ensure_ollama_model(self):
        """Verifica se o modelo Ollama está instalado, se não, instala."""
        try:
            self._log("Verificando modelo Ollama...", "INFO")
            # Verificar modelos disponíveis
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if self.embedding_model not in result.stdout:
                self._log(f"Modelo {self.embedding_model} não encontrado. Instalando...", "WARN")
                self._show_progress(0, 1, "Instalando modelo", self.embedding_model)
                install_result = subprocess.run(['ollama', 'pull', self.embedding_model], 
                                              capture_output=True, text=True)
                self._show_progress(1, 1, "Instalando modelo", self.embedding_model)
                if install_result.returncode == 0:
                    self._log(f"Modelo {self.embedding_model} instalado com sucesso!", "INFO")
                else:
                    self._log(f"Erro ao instalar modelo: {install_result.stderr}", "ERROR")
                    raise Exception("Falha na instalação do modelo")
            else:
                self._log(f"Modelo {self.embedding_model} já está instalado", "INFO")
        except FileNotFoundError:
            self._log("Erro: Ollama não está instalado ou não está no PATH", "ERROR")
            self._log("Instale Ollama em: https://ollama.ai/", "INFO")
            sys.exit(1)
    
    def _init_embedding_model(self):
        """Inicializa o modelo de embeddings."""
        try:
            # Tentar usar Ollama primeiro
            self.model_type = "ollama"
            self._log(f"Usando modelo Ollama: {self.embedding_model}", "INFO")
        except Exception as e:
            self._log(f"Erro ao inicializar Ollama: {e}", "ERROR")
            # Fallback para sentence-transformers
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self.model_type = "sentence_transformers"
                self._log("Usando Sentence Transformers como fallback", "INFO")
            except Exception as e2:
                self._log(f"Erro ao carregar modelo fallback: {e2}", "ERROR")
                sys.exit(1)
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Gera embedding para um texto."""
        if self.model_type == "ollama":
            try:
                result = ollama.embeddings(model=self.embedding_model, prompt=text)
                return np.array(result['embedding'])
            except Exception as e:
                print(f"Erro ao gerar embedding com Ollama: {e}")
                # Fallback
                if self.model:
                    return self.model.encode(text)
                else:
                    raise e
        else:
            return self.model.encode(text)
    
    def convert_pdf_to_md(self, pdf_path: Path) -> str:
        """Converte PDF para Markdown de forma limpa."""
        try:
            self._log(f"Iniciando conversão PDF: {pdf_path.name}", "INFO")
            doc = fitz.open(str(pdf_path))
            total_pages = len(doc)
            markdown_content = []
            
            self._show_progress(0, total_pages, "Convertendo PDF", f"páginas")
            
            for page_num in range(total_pages):
                if self.interrupted:
                    self._log("Conversão interrompida pelo usuário", "WARN")
                    return ""
                
                page = doc[page_num]
                
                # Extrair texto
                text = page.get_text()
                
                # Limpar o texto
                text = self._clean_text(text)
                
                if text.strip():
                    markdown_content.append(f"## Página {page_num + 1}\n\n{text}\n")
                
                self._show_progress(page_num + 1, total_pages, "Convertendo PDF", f"páginas")
            
            doc.close()
            self._log(f"PDF convertido: {total_pages} páginas processadas", "SUCCESS")
            return "\n".join(markdown_content)
        except Exception as e:
            self._log(f"Erro ao converter PDF {pdf_path}: {e}", "ERROR")
            return ""
    
    def convert_epub_to_md(self, epub_path: Path) -> str:
        """Converte EPUB para Markdown."""
        try:
            book = epub.read_epub(str(epub_path))
            markdown_content = []
            
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    # Converter HTML para Markdown
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    # Remover scripts e styles
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Converter para Markdown
                    html_content = str(soup)
                    md_content = markdownify.markdownify(html_content)
                    
                    # Limpar conteúdo
                    md_content = self._clean_markdown(md_content)
                    
                    if md_content.strip():
                        markdown_content.append(md_content)
            
            return "\n\n".join(markdown_content)
        except Exception as e:
            print(f"Erro ao converter EPUB {epub_path}: {e}")
            return ""
    
    def convert_djvu_to_md(self, djvu_path: Path) -> str:
        """Converte Djvu para Markdown usando OCR (requer instalação manual do suporte DjVu)."""
        try:
            # Verificar se o suporte DjVu está disponível
            try:
                import djvu.decode
            except ImportError:
                print("AVISO: Suporte DjVu não está disponível. Instale as dependências manualmente:")
                print("sudo apt-get install djvulibre-bin  # Ubuntu/Debian")
                print("brew install djvulibre  # macOS")
                print("Ou baixe em https://djvu.org/  # Windows")
                return ""
            
            # Converter Djvu para imagens
            images = pdf2image.convert_from_path(str(djvu_path))
            
            markdown_content = []
            
            for i, image in enumerate(images):
                # OCR usando Tesseract
                text = pytesseract.image_to_string(image, lang=self.tesseract_lang)
                
                # Limpar texto
                text = self._clean_text(text)
                
                if text.strip():
                    markdown_content.append(f"## Página {i + 1}\n\n{text}\n")
            
            return "\n".join(markdown_content)
        except Exception as e:
            print(f"Erro ao converter Djvu {djvu_path}: {e}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Limpa texto extraído de documentos."""
        # Remover quebras de linha excessivas
        text = ' '.join(text.split())
        
        # Remover caracteres especiais problemáticos
        text = text.replace('ﬁ', 'fi').replace('ﬂ', 'fl')
        text = text.replace(''', "'").replace(''', "'")
        text = text.replace('"', '"').replace('"', '"')
        
        # Normalizar espaços
        text = ' '.join(text.split())
        
        return text
    
    def _clean_markdown(self, md_content: str) -> str:
        """Limpa conteúdo Markdown."""
        # Remover tags HTML residuais
        md_content = re.sub(r'<[^>]+>', '', md_content)
        
        # Limpar espaços excessivos
        md_content = re.sub(r'\n\s*\n', '\n\n', md_content)
        
        return md_content.strip()
    
    def process_document(self, file_path: Path) -> Dict[str, Any]:
        """Processa um documento e extrai embeddings usando bancos de dados."""
        if self.interrupted:
            self._log("Processamento interrompido", "WARN")
            return {}
        
        # Gerar ID único para o livro
        book_id = self._generate_id()
        
        # Verificar se livro já existe no SQLite
        absolute_file_path = file_path.resolve()
        cursor = self.conn.execute('SELECT id FROM books WHERE file_path = ?', (str(absolute_file_path),))
        existing_book = cursor.fetchone()
        existing_book_id = existing_book['id'] if existing_book else None
        
        # Se livro existe e não mudou, pular processamento
        if existing_book_id and self._is_book_unchanged(file_path, existing_book_id):
            self._log(f"Livro {file_path.name} já processado e inalterado (ID: {existing_book_id})", "INFO")
            return {'book_id': existing_book_id}
        
        # Se livro existe mas mudou, remover dados antigos
        if existing_book_id:
            self._log(f"Livro {file_path.name} modificado, reprocessando (ID: {existing_book_id})", "INFO")
            self.delete_book(existing_book_id)
        
        file_hash = self._get_file_hash(file_path)
        md_path = self.docs_dir / f"{file_path.stem}.md"
        
        # Converter para Markdown
        self._log(f"Processando {file_path.name} (ID: {book_id})...", "INFO")
        self._log(f"Salvando em: {self.docs_dir}", "INFO")
        
        start_time = time.time()
        
        if file_path.suffix.lower() == '.pdf':
            md_content = self.convert_pdf_to_md(file_path)
        elif file_path.suffix.lower() == '.epub':
            md_content = self.convert_epub_to_md(file_path)
        elif file_path.suffix.lower() == '.djvu':
            md_content = self.convert_djvu_to_md(file_path)
        else:
            self._log(f"Formato não suportado: {file_path.suffix}", "ERROR")
            return {}
        
        if self.interrupted:
            return {}
            
        if not md_content:
            self._log(f"Falha ao converter {file_path.name}", "ERROR")
            return {}
        
        # Salvar Markdown
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        conversion_time = time.time() - start_time
        self._log(f"Conversão concluída em {self._format_time(conversion_time)}", "SUCCESS")
        
        # Extrair embeddings
        self._log(f"Extraindo embeddings de {file_path.name}...", "INFO")
        chunk_dicts = self._split_into_chunks(md_content, file_path.stem, chunk_size=None, chunk_overlap=None)
        
        # Filtrar chunks vazios antes de gerar embeddings
        valid_chunks = [c for c in chunk_dicts if c['text'].strip()]
        
        # Gerar embeddings para cada chunk válido
        total_valid = len(valid_chunks)
        embeddings = []
        for i, chunk_info in enumerate(valid_chunks):
            if self.interrupted:
                return {}
            embedding = self.get_embedding(chunk_info['text'])
            embeddings.append(embedding)
            if (i + 1) % 10 == 0 or i == total_valid - 1:
                self._show_progress(i + 1, total_valid, "Gerando embeddings", "chunks")
        
        embedding_time = time.time() - start_time - conversion_time
        self._log(f"Embeddings gerados em {self._format_time(embedding_time)}", "SUCCESS")
        
        # Salvar nos bancos de dados
        self._save_book_to_sqlite(book_id, file_path, {
            'chunk_count': len(valid_chunks),
            'embedding_count': len(embeddings),
            'conversion_time': conversion_time
        })
        
        self._save_chunks_to_sqlite(book_id, valid_chunks)
        self._save_embeddings_to_chroma(book_id, valid_chunks, embeddings)
        
        total_time = time.time() - start_time
        self._log(f"Livro {file_path.name} processado com sucesso! ID: {book_id} ({self._format_time(total_time)})", "SUCCESS")
        return {'book_id': book_id}
    
    def _split_into_chunks(self, content: str, doc_name: str = None, chunk_size: int = None, chunk_overlap: int = None) -> List[Dict[str, Any]]:
        """Divide conteúdo em chunks com rastreamento de página.
        
        Retorna lista de dicts: [{'text': str, 'page': str}, ...]
        """
        chunk_size = chunk_size or self.chunk_size
        chunk_overlap = chunk_overlap or self.chunk_overlap
        
        # Se a sobreposição for maior que o chunk size, ajustar
        if chunk_overlap >= chunk_size:
            chunk_overlap = chunk_size // 4  # 25% de sobreposição como fallback
        
        self._log(f"Dividindo conteúdo em chunks de {chunk_size} caracteres com {chunk_overlap} de sobreposição", "INFO")
        
        # Padrão para detectar marcadores de página
        page_pattern = re.compile(r'## Página (\d+)')
        
        # Dividir por parágrafos e rastrear página corrente
        paragraphs = content.split('\n\n')
        chunks = []  # Lista de {'text': str, 'page': str}
        
        current_chunk = ""
        current_page = "1"
        chunk_start_page = "1"
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Detectar marcador de página no parágrafo
            page_match = page_pattern.search(paragraph)
            if page_match:
                current_page = page_match.group(1)
            
            # Se adicionar o parágrafo não exceder o chunk size
            if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
                    chunk_start_page = current_page
            else:
                # Salvar chunk atual se não estiver vazio
                if current_chunk.strip():
                    chunks.append({'text': current_chunk.strip(), 'page': chunk_start_page})
                
                # Iniciar novo chunk com o parágrafo
                current_chunk = paragraph
                chunk_start_page = current_page
        
        # Salvar último chunk
        if current_chunk.strip():
            chunks.append({'text': current_chunk.strip(), 'page': chunk_start_page})
        
        # Adicionar sobreposição entre chunks
        if chunk_overlap > 0 and len(chunks) > 1:
            overlapped_chunks = []
            
            for i, chunk_info in enumerate(chunks):
                # Manter o chunk original
                overlapped_chunks.append(chunk_info)
                
                # Se não for o último chunk, adicionar chunk sobreposto
                if i < len(chunks) - 1:
                    next_chunk = chunks[i + 1]
                    
                    # Pegar o início do próximo chunk para sobreposição
                    overlap_text = next_chunk['text'][:chunk_overlap]
                    
                    # Criar chunk sobreposto (herda página do chunk atual)
                    overlapped_text = chunk_info['text'][-chunk_overlap:] + " " + overlap_text
                    overlapped_chunks.append({
                        'text': overlapped_text.strip(),
                        'page': chunk_info['page']
                    })
            
            self._log(f"Criados {len(chunks)} chunks originais + {len(chunks)-1} chunks sobrepostos = {len(overlapped_chunks)} total", "INFO")
            return overlapped_chunks
        
        self._log(f"Criados {len(chunks)} chunks sem sobreposição", "INFO")
        return chunks
    
    def _setup_databases(self):
        """Configura bancos de dados SQLite e ChromaDB."""
        print("  📊 Configurando SQLite...")
        # Configurar SQLite
        self.db_path = self.data_dir / "documents.db"
        self._init_sqlite()
        print("  ✅ SQLite configurado!")
        
        print("  🧠 Configurando ChromaDB...")
        # Configurar ChromaDB (chroma_path já foi criado em _setup_logging)
        self._init_chroma()
        print("  ✅ ChromaDB configurado!")
        
        print("  🤖 Verificando modelo Ollama...")
        # Verificar e instalar modelo Ollama se necessário
        self._ensure_ollama_model()
        
        print("  🔧 Inicializando modelo de embeddings...")
        # Inicializar modelo de embeddings
        self.model = None
        self._init_embedding_model()
        print("  ✅ Modelo de embeddings inicializado!")
        
        print("  🔍 Verificando compatibilidade de modelo...")
        # Verificar compatibilidade do modelo com banco existente
        self._check_embedding_model_compatibility()
        
        self._log("Bancos de dados configurados", "INFO")
    
    def _init_sqlite(self):
        """Inicializa banco de dados SQLite."""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
            
            # Criar tabelas
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id TEXT PRIMARY KEY,
                    file_path TEXT UNIQUE,
                    file_hash TEXT,
                    file_size INTEGER,
                    processed_at TIMESTAMP,
                    chunk_count INTEGER,
                    embedding_count INTEGER,
                    conversion_time REAL,
                    metadata TEXT
                )
            ''')
            
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    book_id TEXT,
                    chunk_index INTEGER,
                    content TEXT,
                    page_number TEXT,
                    created_at TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books (id)
                )
            ''')
            
            # Tabela para metadados do sistema
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS system_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            self._log("Banco SQLite inicializado", "INFO")
        except Exception as e:
            self._log(f"Erro ao inicializar SQLite: {e}", "ERROR")
            raise
    
    def _save_embedding_model(self):
        """Salva o modelo de embeddings atual nos metadados."""
        try:
            self.conn.execute('''
                INSERT OR REPLACE INTO system_metadata (key, value, updated_at)
                VALUES (?, ?, ?)
            ''', ('embedding_model', self.embedding_model, datetime.now().isoformat()))
            self.conn.commit()
            self._log(f"Modelo de embeddings salvo: {self.embedding_model}", "INFO")
        except Exception as e:
            self._log(f"Erro ao salvar modelo de embeddings: {e}", "ERROR")
    
    def _get_stored_embedding_model(self) -> Optional[str]:
        """Obtém o modelo de embeddings armazenado no banco."""
        try:
            cursor = self.conn.execute('SELECT value FROM system_metadata WHERE key = ?', ('embedding_model',))
            result = cursor.fetchone()
            return result['value'] if result else None
        except Exception as e:
            self._log(f"Erro ao obter modelo armazenado: {e}", "ERROR")
            return None
    
    def _check_embedding_model_compatibility(self):
        """Verifica se o modelo atual é compatível com o banco existente."""
        stored_model = self._get_stored_embedding_model()
        
        if stored_model is None:
            # Primeira inicialização - salvar modelo atual
            self._save_embedding_model()
            return
        
        if stored_model != self.embedding_model:
            self._log(f"⚠️  **ALERTA CRÍTICO DE MODELO**", "ERROR")
            self._log(f"Modelo armazenado: {stored_model}", "ERROR")
            self._log(f"Modelo atual: {self.embedding_model}", "ERROR")
            self._log(f"Os embeddings foram gerados com '{stored_model}' e não são compatíveis com '{self.embedding_model}'", "ERROR")
            self._log(f"**Soluções:**", "ERROR")
            self._log(f"1. Use o mesmo modelo: --embedding-model {stored_model}", "ERROR")
            self._log(f"2. Apague o banco de dados e recrie com o novo modelo:", "ERROR")
            self._log(f"   rm -rf ~/.generativa/.data", "ERROR")
            self._log(f"3. Migre os embeddings (avançado)", "ERROR")
            
            # Perguntar ao usuário se deseja continuar
            print(f"\n{'='*80}")
            print(f"⚠️  **INCOMPATIBILIDADE DE MODELO DETECTADA**")
            print(f"{'='*80}")
            print(f"Modelo no banco: {stored_model}")
            print(f"Modelo atual:    {self.embedding_model}")
            print(f"\nUsar modelos diferentes pode causar resultados incorretos na busca!")
            print(f"\nDeseja continuar mesmo assim? [s/N]: ", end="")
            
            try:
                response = input().strip().lower()
                if response not in ['s', 'sim', 'yes', 'y']:
                    print("❌ Operação cancelada pelo usuário")
                    sys.exit(1)
                else:
                    self._log("⚠️  Usuário optou por continuar com modelo incompatível", "WARN")
                    # Atualizar o modelo no banco para evitar alertas futuros
                    self._save_embedding_model()
            except KeyboardInterrupt:
                print("\n❌ Operação cancelada pelo usuário")
                sys.exit(1)
        else:
            self._log(f"✅ Modelo de embeddings compatível: {self.embedding_model}", "INFO")
    
    def _init_chroma(self):
        """Inicializa ChromaDB para embeddings."""
        try:
            # Usar persistência local
            self.chroma_client = chromadb.PersistentClient(path=str(self.chroma_path))
            
            # Criar ou obter coleção
            self.collection = self.chroma_client.get_or_create_collection(
                name="document_embeddings",
                metadata={"hnsw:space": "cosine"}
            )
            
            self._log("ChromaDB inicializado", "INFO")
        except Exception as e:
            self._log(f"Erro ao inicializar ChromaDB: {e}", "ERROR")
            raise
    
    def _save_book_to_sqlite(self, book_id: str, file_path: Path, metadata: Dict[str, Any]):
        """Salva informações do livro no SQLite."""
        try:
            file_metadata = self._get_file_metadata(file_path)
            
            # Garantir que o caminho seja absoluto no banco de dados
            absolute_file_path = file_path.resolve()
            
            self.conn.execute('''
                INSERT OR REPLACE INTO books 
                (id, file_path, file_hash, file_size, processed_at, chunk_count, embedding_count, conversion_time, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                book_id,
                str(absolute_file_path),
                file_metadata['hash'],
                file_metadata['size'],
                datetime.now().isoformat(),
                metadata.get('chunk_count', 0),
                metadata.get('embedding_count', 0),
                metadata.get('conversion_time', 0),
                json.dumps(metadata)
            ))
            
            self.conn.commit()
            self._log(f"Livro {book_id} salvo no SQLite", "INFO")
        except Exception as e:
            self._log(f"Erro ao salvar livro no SQLite: {e}", "ERROR")
    
    def _save_chunks_to_sqlite(self, book_id: str, chunks: List[Dict[str, Any]]):
        """Salva chunks no SQLite. Cada chunk é {'text': str, 'page': str}."""
        try:
            chunk_data = []
            for i, chunk_info in enumerate(chunks):
                chunk_id = f"{book_id}_chunk_{i}"
                
                chunk_data.append((
                    chunk_id,
                    book_id,
                    i,
                    chunk_info['text'],
                    chunk_info['page'],
                    datetime.now().isoformat()
                ))
            
            self.conn.executemany('''
                INSERT OR REPLACE INTO chunks 
                (id, book_id, chunk_index, content, page_number, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', chunk_data)
            
            self.conn.commit()
            self._log(f"{len(chunks)} chunks salvos no SQLite", "INFO")
        except Exception as e:
            self._log(f"Erro ao salvar chunks no SQLite: {e}", "ERROR")
    
    def _save_embeddings_to_chroma(self, book_id: str, chunks: List[Dict[str, Any]], embeddings: List[np.ndarray]):
        """Salva embeddings no ChromaDB em lotes. Cada chunk é {'text': str, 'page': str}."""
        try:
            batch_size = 500
            total = len(chunks)
            
            for start in range(0, total, batch_size):
                end = min(start + batch_size, total)
                
                ids = [f"{book_id}_chunk_{i}" for i in range(start, end)]
                documents = [c['text'] for c in chunks[start:end]]
                metadatas = [{"book_id": book_id, "chunk_index": i, "page": chunks[i]['page']} for i in range(start, end)]
                embeddings_list = [emb.tolist() for emb in embeddings[start:end]]
                
                self.collection.add(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas,
                    embeddings=embeddings_list
                )
            
            self._log(f"{total} embeddings salvos no ChromaDB", "INFO")
        except Exception as e:
            self._log(f"Erro ao salvar embeddings no ChromaDB: {e}", "ERROR")
    
    def _search_chroma(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Busca embeddings no ChromaDB."""
        try:
            # Gerar embedding da query
            query_embedding = self.get_embedding(query)
            
            # Buscar no ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Processar resultados
            search_results = []
            for i, (doc_ids, documents, metadatas, distances) in enumerate(zip(
                results['ids'], results['documents'], results['metadatas'], results['distances']
            )):
                for j in range(len(doc_ids)):
                    document = documents[j]
                    metadata = metadatas[j]
                    distance = distances[j]
                    similarity = 1 - distance  # Converter distância para similaridade
                    
                    book_id = metadata['book_id']
                    page = metadata.get('page', 'N/A')
                    
                    # Obter nome do livro do SQLite
                    book_name = self._get_book_name(book_id)
                    
                    # Extrair parte relevante
                    relevant_chunk = self._extract_relevant_chunk(document, query)
                    clean_phrase = self._clean_chunk_for_display(relevant_chunk)
                    
                    search_results.append({
                        'query': query,
                        'book': book_name,
                        'page': page,
                        'phrase': clean_phrase,
                        'relevant_chunk': relevant_chunk,
                        'full_chunk': document,
                        'similarity': float(similarity),
                        'book_id': book_id,
                        'chunk_index': metadata['chunk_index'],
                        'match_type': 'semântico'
                    })
            
            return search_results
        except Exception as e:
            self._log(f"Erro ao buscar no ChromaDB: {e}", "ERROR")
            return []
    
    def _get_book_name(self, book_id: str) -> str:
        """Obtém o nome do livro pelo ID."""
        try:
            cursor = self.conn.execute('SELECT file_path FROM books WHERE id = ?', (book_id,))
            result = cursor.fetchone()
            if result:
                return Path(result['file_path']).name
            return 'Desconhecido'
        except Exception:
            return 'Desconhecido'
    
    def _delete_book_from_databases(self, book_id: str):
        """Remove um livro dos bancos de dados."""
        try:
            # Obter IDs reais dos chunks do SQLite
            cursor = self.conn.execute(
                'SELECT id FROM chunks WHERE book_id = ?', (book_id,)
            )
            chunk_ids = [row['id'] for row in cursor.fetchall()]
            
            # Remover do ChromaDB em lotes
            if chunk_ids:
                batch_size = 500
                for i in range(0, len(chunk_ids), batch_size):
                    batch = chunk_ids[i:i + batch_size]
                    try:
                        self.collection.delete(ids=batch)
                    except Exception as e:
                        self._log(f"Erro ao remover lote do ChromaDB: {e}", "WARN")
                self._log(f"{len(chunk_ids)} embeddings do livro {book_id} removidos do ChromaDB", "INFO")
            
            # Remover do SQLite
            self.conn.execute('DELETE FROM chunks WHERE book_id = ?', (book_id,))
            self.conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
            self.conn.commit()
            
            self._log(f"Livro {book_id} removido do SQLite", "INFO")
        except Exception as e:
            self._log(f"Erro ao remover livro dos bancos: {e}", "ERROR")
    
    def interactive_search(self):
        """Modo interativo de busca nos documentos."""
        print(f"\n🔍 **Modo Interativo de Busca**")
        print(f"📚 Buscando em {len(self._get_indexed_books())} livros indexados")
        print(f"💡 Dicas: Use termos específicos para melhores resultados")
        print(f"⚡ Digite 'sair', 'exit' ou 'quit' para encerrar")
        print(f"📋 Digite 'list' para ver todos os livros indexados")
        print(f"🔍 Digite 'help' para ajuda")
        print(f"{'='*80}")
        
        while True:
            try:
                # Obter entrada do usuário
                query = input(f"\n🔎 **Digite sua busca**: ").strip()
                
                # Comandos especiais
                if query.lower() in ['sair', 'exit', 'quit']:
                    print(f"\n👋 Encerrando modo interativo. Até logo!")
                    break
                
                if query.lower() == 'help':
                    self._show_interactive_help()
                    continue
                
                if query.lower() == 'list':
                    self.list_indexed_books()
                    continue
                
                if not query:
                    print(f"⚠️  Por favor, digite um termo para buscar.")
                    continue
                
                # Realizar busca
                print(f"\n🔍 Buscando por: '{query}'...")
                results = self.search_documents(query)
                
                if not results:
                    print(f"❌ Nenhum resultado encontrado para '{query}'")
                    print(f"💡 Tente usar termos diferentes ou mais genéricos.")
                    continue
                
                # Exibir resultados
                print(f"\n📊 {len(results)} resultados encontrados:")
                print(f"{'='*80}")
                
                for i, result in enumerate(results, 1):
                    match_type = result.get('match_type', 'semântico')
                    match_icon = "📌" if match_type == 'texto' else "🧠"
                    print(f"\n**Resultado {i}** (Similaridade: {result['similarity']:.3f}) {match_icon} [{match_type}]")
                    print(f"📄 **Documento:** {result['book']}")
                    print(f"📖 **Página:** {result['page']}")
                    print(f"🎯 **Chunk Relevante:** {result['relevant_chunk']}")
                    
                    # Opções para o resultado
                    print(f"\n🔧 **Opções:**")
                    print(f"   [1-{len(results)}] Ver mais detalhes do resultado {i}")
                    if i == 1:
                        print(f"   [n] Nova busca")
                        print(f"   [s] Sair")
                    
                    print("-" * 60)
                
                # Perguntar se quer ver detalhes ou fazer nova busca
                while True:
                    action = input(f"\n🤔 **O que deseja fazer?** [n-nova, s-sair, 1-{len(results)}-detalhes]: ").strip().lower()
                    
                    if action in ['n', 'nova', 'new']:
                        break  # Volta para nova busca
                    
                    if action in ['s', 'sair', 'exit', 'quit']:
                        print(f"\n👋 Encerrando modo interativo. Até logo!")
                        return
                    
                    # Verificar se é um número válido
                    try:
                        result_num = int(action)
                        if 1 <= result_num <= len(results):
                            self._show_detailed_result(results[result_num - 1])
                            break
                        else:
                            print(f"⚠️  Número inválido. Digite entre 1 e {len(results)}.")
                    except ValueError:
                        print(f"⚠️  Opção inválida. Tente novamente.")
                
            except KeyboardInterrupt:
                print(f"\n\n⚠️  Interrupção detectada! Encerrando modo interativo.")
                break
            except Exception as e:
                print(f"\n❌ Erro durante a busca: {e}")
                print(f"💡 Tente novamente ou use 'sair' para encerrar.")
    
    def _show_interactive_help(self):
        """Exibe ajuda do modo interativo."""
        print(f"\n📖 **Ajuda do Modo Interativo**")
        print(f"{'='*60}")
        print(f"🔍 **Comandos Disponíveis:**")
        print(f"   • **termo de busca** - Busca nos documentos indexados")
        print(f"   • **help** - Exibe esta ajuda")
        print(f"   • **list** - Lista todos os livros indexados")
        print(f"   • **sair/exit/quit** - Encerra o modo interativo")
        print(f"\n💡 **Dicas de Busca:**")
        print(f"   • Use termos específicos: 'redes neurais convolucionais'")
        print(f"   • Use termos técnicos: 'backpropagation' em vez de 'treinamento'")
        print(f"   • Combine conceitos: 'transformer attention mechanism'")
        print(f"   • Varie os termos se não encontrar resultados")
        print(f"\n📊 **Resultados:**")
        print(f"   • Similaridade varia de 0.0 a 1.0 (maior = mais relevante)")
        print(f"   • Pode ver detalhes de cada resultado")
        print(f"   • Base atual: {len(self._get_indexed_books())} livros")
        print(f"{'='*60}")
    
    def _show_detailed_result(self, result):
        """Exibe detalhes completos de um resultado."""
        print(f"\n📋 **Detalhes Completos do Resultado**")
        print(f"{'='*80}")
        print(f"📄 **Documento:** {result['book']}")
        print(f"📖 **Página:** {result['page']}")
        print(f"🎯 **Similaridade:** {result['similarity']:.3f}")
        print(f"🔍 **Query Original:** {result['query']}")
        print(f"\n📝 **Chunk Relevante:**")
        print(f"{result['relevant_chunk']}")
        print(f"\n📄 **Chunk Completo:**")
        print(f"{result['full_chunk']}")
        print(f"{'='*80}")
        
        input(f"\n⏎  Pressione Enter para continuar...")
    
    def _get_indexed_books(self):
        """Obtém lista de livros indexados do SQLite."""
        try:
            cursor = self.conn.execute('SELECT id, file_path FROM books')
            books = cursor.fetchall()
            return {book['id']: book['file_path'] for book in books}
        except Exception as e:
            self._log(f"Erro ao obter livros indexados: {e}", "ERROR")
            return {}
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calcula hash do arquivo para verificação de mudanças."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _generate_id(self, length: int = 10) -> str:
        """Gera ID alfanumérico único."""
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choices(chars, k=length))
    
    def _get_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Obtém metadados completos do arquivo para verificação de mudanças."""
        try:
            stat = file_path.stat()
            return {
                'size': stat.st_size,
                'mtime': stat.st_mtime,
                'ctime': stat.st_ctime,
                'hash': self._get_file_hash(file_path)
            }
        except Exception as e:
            self._log(f"Erro ao obter metadados de {file_path}: {e}", "ERROR")
            return {}
    
    def _is_book_unchanged(self, file_path: Path, book_id: str) -> bool:
        """Verifica se o livro mudou desde o último processamento usando SQLite."""
        try:
            cursor = self.conn.execute('''
                SELECT file_hash, file_size FROM books WHERE id = ?
            ''', (book_id,))
            
            result = cursor.fetchone()
            if not result:
                return False
            
            current_metadata = self._get_file_metadata(file_path)
            
            # Comparar metadados
            return (current_metadata.get('size') == result['file_size'] and
                    current_metadata.get('hash') == result['file_hash'])
        except Exception as e:
            self._log(f"Erro ao verificar mudanças do livro: {e}", "ERROR")
            return False
    
    def list_indexed_books(self):
        """Lista todos os livros indexados do SQLite."""
        try:
            cursor = self.conn.execute('''
                SELECT id, file_path, file_size, processed_at, chunk_count, embedding_count
                FROM books 
                ORDER BY processed_at DESC
            ''')
            
            books = cursor.fetchall()
            
            if not books:
                print("📚 Nenhum livro indexado encontrado.")
                return
            
            print(f"📚 {len(books)} livros indexados:\n")
            print("| ID | Livro | Tamanho | Processado em | Chunks |")
            print("|----|-------|--------|--------------|--------|")
            
            for book in books:
                file_path = Path(book['file_path'])
                size_mb = book['file_size'] / (1024*1024)
                processed_date = book['processed_at']
                chunk_count = book['chunk_count']
                
                # Formatar data
                try:
                    dt = datetime.fromisoformat(processed_date)
                    processed_date = dt.strftime('%d/%m/%Y %H:%M')
                except:
                    pass
                
                print(f"| {book['id']} | {file_path.name} | {size_mb:.1f}MB | {processed_date} | {chunk_count} |")
            
            print(f"\n📁 Arquivos em: {self.docs_dir}")
            print(f"💾 Banco de dados: {self.db_path}")
            print(f"🔍 Embeddings: {self.chroma_path}")
        except Exception as e:
            self._log(f"Erro ao listar livros: {e}", "ERROR")
            print(f"❌ Erro ao listar livros: {e}")
    
    def delete_book(self, book_id: str) -> bool:
        """Remove um livro dos bancos de dados e arquivos associados."""
        try:
            # Verificar se livro existe
            cursor = self.conn.execute('SELECT file_path FROM books WHERE id = ?', (book_id,))
            result = cursor.fetchone()
            
            if not result:
                print(f"❌ Livro com ID '{book_id}' não encontrado.")
                return False
            
            file_path = Path(result['file_path'])
            book_name = file_path.stem
            
            print(f"🗑️  Removendo livro: {file_path.name} (ID: {book_id})")
            
            # Remover arquivo Markdown
            md_path = self.docs_dir / f"{book_name}.md"
            if md_path.exists():
                md_path.unlink()
                print(f"✅ Removido: {md_path}")
            
            # Remover dos bancos de dados
            self._delete_book_from_databases(book_id)
            
            print(f"✅ Livro '{book_id}' removido com sucesso!")
            return True
        except Exception as e:
            self._log(f"Erro ao remover livro: {e}", "ERROR")
            print(f"❌ Erro ao remover livro: {e}")
            return False
    
    def search_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Busca híbrida: texto exato (SQLite) + semântica (ChromaDB)."""
        print(f"🔍 Buscando por: '{query}'")
        
        # 1. Busca textual exata/parcial no SQLite
        text_results = self._search_text(query, top_k)
        
        # 2. Busca semântica no ChromaDB
        semantic_results = self._search_chroma(query, top_k)
        
        # 3. Combinar resultados (texto exato primeiro, sem duplicatas)
        seen_chunk_ids = set()
        combined = []
        
        # Adicionar resultados textuais primeiro (boost de similaridade)
        for r in text_results:
            chunk_key = f"{r['book_id']}_{r['chunk_index']}"
            if chunk_key not in seen_chunk_ids:
                seen_chunk_ids.add(chunk_key)
                combined.append(r)
        
        # Adicionar resultados semânticos que não sejam duplicatas
        for r in semantic_results:
            if r['similarity'] <= self.similarity_threshold:
                continue
            chunk_key = f"{r['book_id']}_{r['chunk_index']}"
            if chunk_key not in seen_chunk_ids:
                seen_chunk_ids.add(chunk_key)
                combined.append(r)
        
        # Ordenar por similaridade (descendente)
        combined.sort(key=lambda x: x['similarity'], reverse=True)
        
        return combined[:top_k]
    
    def _search_text(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Busca textual no SQLite (match exato e parcial)."""
        try:
            # Buscar chunks que contenham o texto da query
            cursor = self.conn.execute('''
                SELECT c.book_id, c.chunk_index, c.content, c.page_number, b.file_path
                FROM chunks c
                JOIN books b ON c.book_id = b.id
                WHERE c.content LIKE ?
                ORDER BY 
                    CASE WHEN c.content LIKE ? THEN 0 ELSE 1 END,
                    c.chunk_index
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', top_k))
            
            results = []
            for row in cursor.fetchall():
                file_path = Path(row['file_path'])
                relevant_chunk = self._extract_relevant_chunk(row['content'], query)
                clean_phrase = self._clean_chunk_for_display(relevant_chunk)
                
                results.append({
                    'query': query,
                    'book': file_path.name,
                    'page': row['page_number'] or 'N/A',
                    'phrase': clean_phrase,
                    'relevant_chunk': relevant_chunk,
                    'full_chunk': row['content'],
                    'similarity': 1.0,  # Match exato = similaridade máxima
                    'book_id': row['book_id'],
                    'chunk_index': row['chunk_index'],
                    'match_type': 'texto'
                })
            
            if results:
                self._log(f"Busca textual: {len(results)} resultados encontrados", "INFO")
            
            return results
        except Exception as e:
            self._log(f"Erro na busca textual: {e}", "ERROR")
            return []
    
    def _clean_chunk_for_display(self, chunk: str) -> str:
        """Limpa o chunk para exibição na tabela."""
        # Remover marcações de página
        chunk = re.sub(r'## Página \d+', '', chunk)
        chunk = re.sub(r'Página \d+', '', chunk)
        
        # Remover quebras de linha excessivas
        chunk = ' '.join(chunk.split())
        
        # Manter o chunk completo para exibição detalhada
        return chunk.strip()
    
    def _extract_relevant_chunk(self, chunk: str, query: str) -> str:
        """Extrai a parte mais relevante do chunk em relação à query."""
        # 1. Tentar match exato da query no chunk (janela de contexto ao redor)
        chunk_lower = chunk.lower()
        query_lower = query.lower()
        pos = chunk_lower.find(query_lower)
        if pos != -1:
            # Expandir para incluir contexto ao redor (150 chars cada lado)
            context = 150
            start = max(0, pos - context)
            end = min(len(chunk), pos + len(query) + context)
            excerpt = chunk[start:end].strip()
            if start > 0:
                excerpt = '...' + excerpt
            if end < len(chunk):
                excerpt = excerpt + '...'
            return excerpt
        
        # 2. Dividir o chunk em sentenças e buscar por maior sobreposição de termos
        sentences = re.split(r'[.!?]+', chunk)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return chunk.strip()
        
        # Filtrar stop words curtas para evitar falsos positivos
        query_terms = [t for t in query_lower.split() if len(t) > 3]
        if not query_terms:
            query_terms = query_lower.split()
        
        # Pontuar sentenças pela quantidade de termos da query presentes
        scored = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            score = sum(1 for term in query_terms if term in sentence_lower)
            if score > 0:
                scored.append((score, sentence))
        
        if scored:
            scored.sort(key=lambda x: x[0], reverse=True)
            # Retornar as sentenças com maior pontuação
            best = [s for _, s in scored[:3]]
            return ' '.join(best)
        
        # 3. Fallback: retornar o início do chunk
        return chunk[:300] + '...' if len(chunk) > 300 else chunk
    
    def convert_all_in_directory(self, directory: Path):
        """Converte todos os documentos suportados em um diretório."""
        supported_extensions = {'.pdf', '.epub', '.djvu'}
        
        # Encontrar todos os arquivos suportados
        all_files = []
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                all_files.append(file_path)
        
        if not all_files:
            self._log(f"Nenhum documento suportado encontrado em {directory}", "WARN")
            return
        
        total_files = len(all_files)
        self._log(f"Encontrados {total_files} documentos para processar", "INFO")
        
        processed = 0
        skipped = 0
        failed = 0
        
        start_time = time.time()
        
        for i, file_path in enumerate(all_files):
            if self.interrupted:
                self._log("Processamento em lote interrompido", "WARN")
                break
            
            self._show_progress(i, total_files, "Processando arquivos", f"{file_path.name}")
            
            # Verificar se já foi processado via SQLite
            cursor = self.conn.execute('SELECT id FROM books WHERE file_path = ?', (str(file_path),))
            existing = cursor.fetchone()
            existing_book_id = existing['id'] if existing else None
            
            if existing_book_id and self._is_book_unchanged(file_path, existing_book_id):
                skipped += 1
                continue
            
            try:
                result = self.process_document(file_path)
                if result:
                    processed += 1
                else:
                    failed += 1
            except Exception as e:
                self._log(f"Erro ao processar {file_path.name}: {e}", "ERROR")
                failed += 1
        
        self._show_progress(total_files, total_files, "Processando arquivos", "concluído")
        
        total_time = time.time() - start_time
        self._log(f"Processamento concluído!", "SUCCESS")
        self._log(f"✅ Processados: {processed}", "INFO")
        self._log(f"⏭️  Pulados: {skipped}", "INFO")
        self._log(f"❌ Falhas: {failed}", "INFO")
        self._log(f"⏱️  Tempo total: {self._format_time(total_time)}", "INFO")


def main():
    parser = argparse.ArgumentParser(description='Conversor de Documentos com Busca Semântica')
    parser.add_argument('--convert', type=str, help='Converte arquivo específico')
    parser.add_argument('--convert-all', type=str, help='Converte todos os documentos no diretório')
    parser.add_argument('--search', type=str, help='Busca nos documentos processados')
    parser.add_argument('--interactive', '-i', action='store_true', help='Modo interativo de busca')
    parser.add_argument('--list', action='store_true', help='Lista todos os livros indexados')
    parser.add_argument('--delete', type=str, help='Remove um livro pelo ID')
    parser.add_argument('--data-dir', type=str, default='.data', help='Diretório de dados')
    parser.add_argument('--converted-dir', type=str, help='Pasta para arquivos convertidos (padrão: ../Livros e Apostilas/converteds)')
    parser.add_argument('--lang', type=str, default='por', help='Idioma do OCR (padrão: por)')
    parser.add_argument('--chunk-size', type=int, help='Tamanho dos chunks (padrão: 500)')
    parser.add_argument('--chunk-overlap', type=int, help='Sobreposição entre chunks (padrão: 50)')
    parser.add_argument('--embedding-model', type=str, help='Modelo de embeddings (padrão: mxbai-embed-large)')
    
    args = parser.parse_args()
    
    # Se nenhum argumento for fornecido, mostrar ajuda
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # Tratar None para chunk_size e chunk_overlap (CLI não fornecido → usar default do .env/construtor)
    kwargs = {
        'data_dir': args.data_dir,
        'converted_dir': args.converted_dir,
        'tesseract_lang': args.lang,
    }
    if args.chunk_size is not None:
        kwargs['chunk_size'] = args.chunk_size
    if args.chunk_overlap is not None:
        kwargs['chunk_overlap'] = args.chunk_overlap
    if args.embedding_model is not None:
        kwargs['embedding_model'] = args.embedding_model
    
    converter = DocumentConverter(**kwargs)
    
    # Processar argumentos
    if args.list:
        converter.list_indexed_books()
        return
    
    if args.delete:
        converter.delete_book(args.delete)
        return
    
    if args.interactive:
        converter.interactive_search()
        return
    
    if args.search:
        results = converter.search_documents(args.search)
        
        if not results:
            print("❌ Nenhum resultado encontrado")
            return
        
        print(f"\n🔍 {len(results)} resultados encontrados para '{args.search}':\n")
        
        print(f"📈 **Detalhes dos Resultados:**")
        for i, result in enumerate(results, 1):
            match_type = result.get('match_type', 'semântico')
            match_icon = "📌" if match_type == 'texto' else "🧠"
            print(f"\n**Resultado {i}** (Similaridade: {result['similarity']:.3f}) {match_icon} [{match_type}]")
            print(f"📄 **Documento:** {result['book']}")
            print(f"📖 **Página:** {result['page']}")
            print(f"🎯 **Chunk Relevante:** {result['relevant_chunk']}")
            print("-" * 80)
        
        total_time = time.time() - converter.start_time
        print(f"\n⏱️  Tempo total de execução: {converter._format_time(total_time)}")
        print(f"📋 Log salvo em: {converter.log_file}")
        return
    
    if args.convert:
        file_path = Path(args.convert)
        if not file_path.exists():
            print(f"Arquivo não encontrado: {file_path}")
            return
        converter.process_document(file_path)
        return
    
    if args.convert_all:
        directory = Path(args.convert_all)
        if not directory.exists():
            print(f"Diretório não encontrado: {directory}")
            return
        converter.convert_all_in_directory(directory)
        return
    
    # Detectar se o primeiro argumento sem -- é um arquivo ou pasta
    positional_args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    if positional_args:
        target = Path(positional_args[0])
        
        if not target.exists():
            print(f"Arquivo ou diretório não encontrado: {target}")
            return
        
        if target.is_file():
            print(f"� Convertendo arquivo: {target}")
            converter.process_document(target)
        elif target.is_dir():
            print(f"🔄 Convertendo todos os documentos na pasta: {target}")
            converter.convert_all_in_directory(target)
        return
    


if __name__ == "__main__":
    main()
