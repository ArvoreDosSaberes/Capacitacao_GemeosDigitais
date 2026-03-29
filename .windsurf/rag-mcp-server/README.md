# RAG MCP Server para Windsurf

Extensão personalizada do Windsurf que integra com sua base de embeddings local.

## Funcionalidades

- **Busca Semântica**: Encontre documentos relevantes usando embeddings
- **Lista de Livros**: Visualize todos os livros indexados
- **Conteúdo de Livros**: Acesse conteúdo completo ou páginas específicas
- **Documentos Similares**: Encontre documentos similares a um texto
- **Estatísticas**: Veja estatísticas da base de dados

## Instalação

1. Instale as dependências:
```bash
cd .windsurf/rag-mcp-server
npm install
```

2. Configure o Windsurf para usar o MCP server:

Adicione ao seu arquivo de configuração do Windsurf:

```json
{
  "mcpServers": {
    "rag-local": {
      "command": "node",
      "args": ["./.windsurf/rag-mcp-server/server.js"],
      "cwd": "/home/carlosdelfino/workspace/Faculdades e Cursos/GemeosDigitais"
    }
  }
}
```

## Uso

### Buscar Documentos
Use a ferramenta `rag_search` para encontrar documentos relevantes:

```
Busque por "redes neurais convolucionais" na minha base de documentos
```

### Listar Livros
Use `rag_list_books` para ver todos os livros indexados:

```
Liste todos os livros disponíveis na base
```

### Obter Conteúdo Específico
Use `rag_get_book_content` para acessar conteúdo de um livro:

```
Obtenha o conteúdo do livro com ID "abc123" das páginas 1, 2, 3
```

### Encontrar Documentos Similares
Use `rag_similar_documents`:

```
Encontre documentos similares a "transformer architecture"
```

### Ver Estatísticas
Use `rag_get_stats` para informações da base:

```
Mostre as estatísticas da minha base de documentos
```

## Configuração

O servidor usa as variáveis de ambiente do seu arquivo `.env`:

- `DATA_DIR`: Diretório dos dados (padrão: `.data`)
- `CHROMA_DB_PATH`: Caminho para o ChromaDB
- `SQLITE_DB_PATH`: Caminho para o SQLite
- `OLLAMA_HOST`: Host do Ollama (padrão: `http://localhost:11434`)
- `OLLAMA_MODEL`: Modelo de embeddings (padrão: `mxbai-embed-large`)

## Exemplos Práticos

### Pesquisa Acadêmica
```
Busque por "machine learning algorithms" e mostre os 5 resultados mais relevantes
```

### Estudo Específico
```
Liste todos os livros, depois obtenha o conteúdo do livro sobre "Python" das páginas 10-20
```

### Documentação Similar
```
Encontre documentos similares a "deep learning frameworks"
```

### Análise da Base
```
Mostre as estatísticas completas da minha base de documentos
```

## Troubleshooting

### Erro de Conexão
Verifique se o Ollama está rodando:
```bash
ollama list
```

### Base de Dados Não Encontrada
Verifique se os caminhos em `.env` estão corretos:
```bash
ls -la .data/
```

### Permissões
Garanta que o Node.js tenha acesso aos arquivos:
```bash
chmod +x .windsurf/rag-mcp-server/server.js
```

## Arquitetura

- **ChromaDB**: Armazenamento de embeddings
- **SQLite**: Metadados e conteúdo dos documentos
- **Ollama**: Geração de embeddings
- **MCP Protocol**: Integração com Windsurf
