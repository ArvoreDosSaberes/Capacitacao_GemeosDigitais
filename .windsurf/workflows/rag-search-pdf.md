---
description: Busca contextual na base de documentos com links clicáveis para PDFs
---

# Workflow de Busca Contextual RAG com PDF Links

Este workflow permite realizar buscas inteligentes na sua base de documentos e abrir os PDFs diretamente na página encontrada.

## Uso

Digite `/rag-search-pdf` seguido do termo que deseja pesquisar.

## Exemplos

- `/rag-search-pdf redes neurais convolucionais`
- `/rag-search-pdf machine learning algorithms`
- `/rag-search-pdf python programming`
- `/rag-search-pdf data science`

## O que acontece

1. **Busca Semântica**: Encontra documentos relevantes usando embeddings
2. **Links Clicáveis**: Gera links diretos para os PDFs na página específica
3. **Abertura Automática**: Oferece opção para abrir o PDF no visualizador padrão
4. **Contexto Rico**: Mostra trechos relevantes com alta similaridade

## Resultados

Cada resultado inclui:
- 📄 Nome do documento
- 📖 Página específica com link clicável
- 🎯 Trecho relevante
- 📊 Pontuação de similaridade
- 🔗 Link direto: `file://[caminho]#page=[numero]`
- 🚀 Botão para abrir PDF automaticamente

## Funcionalidades Especiais

### Links Clicáveis
- Clique nos links `file://` para abrir o PDF diretamente na página
- Funciona com a maioria dos visualizadores de PDF
- Links são absolutos e funcionam em qualquer sistema

### Abertura Automática
- Use a ferramenta `rag_open_pdf` para abrir automaticamente
- Suporta Windows, macOS e Linux
- Abre no visualizador padrão do sistema

### Exemplo de Uso Avançado

```
Busque por "transformer architecture" e me mostre os 3 melhores resultados com links para PDF
```

## Dicas

- **Termos Específicos**: Use linguagem técnica para melhores resultados
- **Combinar Conceitos**: `deep learning convolutional networks`
- **Navegação Rápida**: Clique nos links para ir direto ao conteúdo
- **Visualização**: Os PDFs abrem na página exata do conteúdo encontrado

## Comandos Relacionados

- `/rag-search-pdf` - Busca com links para PDFs
- `rag_open_pdf` - Abre PDF automaticamente
- `rag_list_books` - Lista todos os livros disponíveis

## Configuração

Este workflow usa o MCP server `rag-local` com suporte aprimorado para PDFs. Certifique-se de que os PDFs originais estejam acessíveis nos caminhos registrados no banco de dados.
