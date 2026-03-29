#!/bin/bash

# Script de instalação do RAG MCP Server para Windsurf

echo "🚀 Instalando RAG MCP Server para Windsurf..."

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale o Node.js primeiro."
    echo "💡 Visite: https://nodejs.org/"
    exit 1
fi

# Verificar se npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm não encontrado. Por favor, instale o npm primeiro."
    exit 1
fi

# Verificar se Ollama está rodando
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama não encontrado. Verifique se está instalado e no PATH."
    echo "💡 Se não tiver Ollama, instale em: https://ollama.ai/"
fi

# Entrar no diretório do MCP server
cd "$(dirname "$0")"

# Instalar dependências
echo "📦 Instalando dependências..."
npm install

# Verificar se instalação foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso!"
else
    echo "❌ Erro ao instalar dependências."
    exit 1
fi

# Verificar se o arquivo .env existe no diretório raiz
if [ ! -f "../../.env" ]; then
    echo "⚠️  Arquivo .env não encontrado no diretório raiz."
    echo "💡 Copie .env.example para .env e configure suas variáveis."
    echo "   cp ../../.env.example ../../.env"
fi

# Verificar se a base de dados existe
if [ ! -d "../../.data" ]; then
    echo "⚠️  Diretório .data não encontrado."
    echo "💡 Execute o script de conversão de documentos primeiro:"
    echo "   python scripts/document.py --convert-all"
fi

# Testar o servidor
echo "🧪 Testando o servidor MCP..."
timeout 5s node server.js > /dev/null 2>&1
if [ $? -eq 124 ]; then
    echo "✅ Servidor MCP iniciou com sucesso!"
else
    echo "⚠️  O servidor pode precisar de configuração adicional."
fi

echo ""
echo "🎉 Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure o Windsurf para usar o MCP server:"
echo "   Adicione ao seu arquivo de configuração do Windsurf:"
echo ""
echo "   {"
echo "     \"mcpServers\": {"
echo "       \"rag-local\": {"
echo "         \"command\": \"node\","
echo "         \"args\": [\"./.windsurf/rag-mcp-server/server.js\"],"
echo "         \"cwd\": \"$(cd ../.. && pwd)\""
echo "       }"
echo "     }"
echo "   }"
echo ""
echo "2. Reinicie o Windsurf"
echo "3. Use /rag-search para buscar na sua base de documentos"
echo ""
echo "📚 Para mais informações, consulte README.md"
