#!/usr/bin/env bash
# ===========================================================================
# setup_and_run.sh
#
# Prepara o ambiente virtual Python e executa o script de processamento
# de transcrições VTT → Markdown didático.
#
# Uso:
#   ./scripts/setup_and_run.sh                       # processa todos os VTTs
#   ./scripts/setup_and_run.sh --force                # reprocessa tudo (ignora cache)
#   ./scripts/setup_and_run.sh --dry-run              # apenas lista os VTTs e estado
#   ./scripts/setup_and_run.sh --file "caminho"       # processa um arquivo específico
#   ./scripts/setup_and_run.sh --skip-standardize     # pula padronização do AULAS.md
# ===========================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Diretórios
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"
ENV_FILE="$PROJECT_ROOT/.env"
PYTHON_SCRIPT="$SCRIPT_DIR/process_vtt.py"

# ---------------------------------------------------------------------------
# Cores para saída
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERRO]${NC}  $*"; }

# ---------------------------------------------------------------------------
# Verificações iniciais
# ---------------------------------------------------------------------------
echo ""
echo "============================================================"
echo "  Processador de Transcrições VTT → Markdown Didático"
echo "============================================================"
echo ""

# Verifica se o arquivo .env existe
if [ ! -f "$ENV_FILE" ]; then
    error "Arquivo .env não encontrado em: $ENV_FILE"
    warn "Copie o .env.example e configure sua chave da OpenAI:"
    echo "  cp $PROJECT_ROOT/.env.example $PROJECT_ROOT/.env"
    echo "  # Edite o .env e insira sua OPENAI_API_KEY"
    exit 1
fi

# Verifica se a OPENAI_API_KEY está configurada (não é o valor padrão)
source "$ENV_FILE" 2>/dev/null || true
if [ -z "${OPENAI_API_KEY:-}" ] || [ "$OPENAI_API_KEY" = "sk-proj-SUA_CHAVE_AQUI" ]; then
    error "OPENAI_API_KEY não configurada ou com valor padrão."
    warn "Edite o arquivo .env e insira sua chave real da OpenAI."
    exit 1
fi
ok "Arquivo .env encontrado e OPENAI_API_KEY configurada."

# ---------------------------------------------------------------------------
# Verifica/instala Python 3
# ---------------------------------------------------------------------------
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    error "Python 3 não encontrado. Instale o Python 3.9+ antes de continuar."
    exit 1
fi

PYTHON_VERSION=$($PYTHON --version 2>&1)
info "Python encontrado: $PYTHON_VERSION"

# ---------------------------------------------------------------------------
# Cria/atualiza ambiente virtual
# ---------------------------------------------------------------------------
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

# Recria o venv se ele não tiver um python funcional
if [ ! -x "$VENV_PYTHON" ]; then
    if [ -d "$VENV_DIR" ]; then
        warn "Ambiente virtual existente está incompleto. Recriando…"
        rm -rf "$VENV_DIR"
    fi
    info "Criando ambiente virtual em: $VENV_DIR"
    $PYTHON -m venv "$VENV_DIR"
    ok "Ambiente virtual criado."
else
    ok "Ambiente virtual encontrado: $VENV_DIR"
fi

# ---------------------------------------------------------------------------
# Instala/atualiza dependências (usa binários do venv diretamente)
# ---------------------------------------------------------------------------
info "Atualizando pip…"
"$VENV_PYTHON" -m pip install --upgrade pip --quiet

info "Instalando dependências de: $REQUIREMENTS"
"$VENV_PIP" install -r "$REQUIREMENTS" --quiet
ok "Dependências instaladas."

# ---------------------------------------------------------------------------
# Executa o script Python
# ---------------------------------------------------------------------------
echo ""
echo "------------------------------------------------------------"
info "Iniciando processamento das transcrições…"
echo "------------------------------------------------------------"
echo ""

"$VENV_PYTHON" "$PYTHON_SCRIPT" "$@"

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    ok "Processamento concluído com sucesso!"
else
    error "Processamento encerrado com código de erro: $EXIT_CODE"
fi

exit $EXIT_CODE
