---
description: Encontra páginas específicas em livros com base em texto ou número de página
---

# Workflow de Busca de Páginas Específicas

Este workflow permite encontrar páginas específicas em livros digitando o texto entre aspas ou um número de página. Se múltiplas páginas forem encontradas, apresenta um menu interativo para escolher.

## Uso

Digite `/rag-find-page` seguido do texto entre aspas ou número de página.

## Exemplos

- `/rag-find-page "redes neurais convolucionais"`
- `/rag-find-page "machine learning algorithms"`
- `/rag-find-page 42`
- `/rag-find-page "attention mechanism"`

## O que acontece

1. **Análise da Query**: Identifica se é texto entre aspas ou número de página
2. **Busca Inteligente**: 
   - Para texto: usa busca semântica para encontrar páginas relevantes
   - Para número: busca direta pela página específica em todos os livros
3. **Menu Interativo**: Se múltiplos resultados, apresenta opções numeradas
4. **Seleção e Recuperação**: Recupera o conteúdo da página escolhida
5. **Contexto Rico**: Apresenta o conteúdo completo da página para uso no chat

## Fluxo de Funcionamento

### Busca por Texto
```
/rag-find-page "texto pesquisado"
↓
Busca semântica em todos os livros
↓
Se múltiplos resultados → Menu de escolha
↓
Recupera conteúdo completo da página
↓
Apresenta conteúdo para uso no chat
```

### Busca por Número de Página
```
/rag-find-page 42
↓
Busca página 42 em todos os livros indexados
↓
Se encontrado em múltiplos livros → Menu de escolha
↓
Recupera conteúdo completo da página
↓
Apresenta conteúdo para uso no chat
```

## Menu Interativo

Quando múltiplas páginas são encontradas, o sistema apresenta:

```
📚 Encontradas X páginas com o texto pesquisado:

[1] Livro A - Página 23 - "trecho do conteúdo..."
[2] Livro B - Página 156 - "trecho do conteúdo..."
[3] Livro C - Página 89 - "trecho do conteúdo..."

Digite o número da página desejada (1-3) ou 'todos' para ver todas:
```

## Resultados

Após seleção, apresenta:

### Conteúdo Completo da Página
- 📄 **Livro**: Nome do documento
- 📖 **Página**: Número da página
- 📝 **Conteúdo**: Texto completo da página
- 🔗 **Link PDF**: Link clicável para abrir no visualizador
- 🚀 **Opção**: Botão para abrir PDF automaticamente

### Opções Adicionais
- **Abrir PDF**: Abre o documento na página específica
- **Copiar Conteúdo**: Copia o texto para área de transferência
- **Buscar Similares**: Encontra outras páginas com conteúdo similar
- **Ver Contexto**: Mostra páginas anteriores e posteriores

## Comandos Especiais

### Navegação Avançada
- `anterior` - Ver página anterior
- `proxima` - Ver próxima página  
- `inicio` - Ver primeira página do capítulo
- `fim` - Ver última página do capítulo

### Filtros
- `livro:"nome"` - Buscar apenas em livro específico
- `pagina:X-Y` - Buscar em intervalo de páginas
- `similar:0.8` - Ajustar limiar de similaridade

## Exemplos de Uso Avançado

```
/rag-find-page "transformer architecture"
↓
📚 Encontradas 5 páginas:

[1] Deep Learning Book - Página 234 - "The transformer architecture..."
[2] NLP Handbook - Página 89 - "Transformer models use..."
[3] ML Guide - Página 412 - "The attention mechanism..."

Digite 2 para selecionar:
↓
[Apresenta conteúdo completo da página 89 do NLP Handbook]
```

```
/rag-find-page 156
↓
📚 Página 156 encontrada em 3 livros:

[1] Algorithms Book - Página 156
[2] Data Science Guide - Página 156  
[3] Programming Manual - Página 156

Digite 1 para selecionar:
↓
[Apresenta conteúdo completo da página 156]
```

## Dicas de Uso

### Para Melhores Resultados
- **Texto Específico**: Use frases exatas entre aspas
- **Termos Técnicos**: Use linguagem técnica e precisa
- **Contexto**: Inclua contexto para buscas mais relevantes
- **Números de Página**: Use quando souber a página exata

### Estratégias de Busca
- **Citações**: `"attention is all you need"`
- **Conceitos**: `"gradient descent optimization"`
- **Autores**: `"Geoffrey Hinton"`
- **Fórmulas**: `"backpropagation algorithm"`

## Integração com Chat

O conteúdo recuperado fica disponível para:
- **Análise**: Estudar o conteúdo em detalhes
- **Resumo**: Criar resumos personalizados
- **Explicação**: Pedir explicações sobre conceitos
- **Tradução**: Traduzir conteúdo para outros idiomas
- **Comparação**: Comparar com outras páginas ou documentos

## Configuração

Este workflow usa o MCP server `rag-local` com:
- Busca semântica avançada
- Recuperação de conteúdo completo
- Links diretos para PDFs
- Interface interativa de seleção

## Comandos Relacionados

- `/rag-find-page` - Busca de páginas específicas
- `/rag-search` - Busca contextual geral
- `/rag-search-pdf` - Busca com links para PDFs
- `rag_open_pdf` - Abre PDF automaticamente
- `rag_list_books` - Lista todos os livros
