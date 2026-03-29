---
description: Busca contextual na base de documentos usando embeddings
---

# Workflow de Busca Contextual RAG

Este workflow permite realizar buscas inteligentes na sua base de documentos indexados usando embeddings e busca semântica.

## Uso

Digite `/rag-search` seguido do termo que deseja pesquisar.

## Exemplos

- `/rag-search redes neurais convolucionais`
- `/rag-search machine learning algorithms`
- `/rag-search python programming`
- `/rag-search data science`

## O que acontece

1. **Geração de Embedding**: O termo de busca é convertido em um vetor numérico usando Ollama
2. **Busca Semântica**: O sistema encontra documentos com significados similares
3. **Ranking**: Resultados são ordenados por relevância (similaridade)
4. **Apresentação**: Top 5 resultados são exibidos com contexto

## Resultados

Cada resultado inclui:
- 📄 Nome do documento
- 📖 Página específica
- 🎯 Trecho relevante
- 📊 Pontuação de similaridade
- 🔧 Opções para explorar mais

## Dicas

- Use termos específicos e técnicos para melhores resultados
- Combine conceitos: `transformer attention mechanism`
- Varie os termos se não encontrar resultados
- A similaridade varia de 0.0 a 1.0 (maior = mais relevante)

## Configuração

Este workflow usa o MCP server `rag-local` que deve estar configurado no Windsurf.
