# Exemplos Práticos de Uso do RAG com PDF Links

## Busca Simples com Links

**Usuário:** `/rag-search-pdf redes neurais`

**Cascade:** 🔍 Buscando por: 'redes neurais'

📊 **5 resultados encontrados:**

### 📄 **Resultado 1** (Similaridade: 0.892) 🧠 [semântico]
- **Documento:** Deep_Learning_Fundamentals.pdf
- **Página:** [📖 Página 45](file:///home/carlosdelfino/workspace/Faculdades e Cursos/GemeosDigitais/Livros e Apostilas/Deep_Learning_Fundamentals.pdf#page=45)
- **🎯 Trecho Relevante:** Redes neurais artificiais são sistemas computacionais inspirados na estrutura do cérebro humano, compostos por neurônios interconectados que processam informações de forma paralela.
- **🚀 [Abrir PDF Automaticamente](rag_open_pdf:book_id=abc123&page_number=45)**

---

### 📄 **Resultado 2** (Similaridade: 0.856) 🧠 [semântico]
- **Documento:** Machine_Learning_Basics.pdf
- **Página:** [📖 Página 23](file:///home/carlosdelfino/workspace/Faculdades e Cursos/GemeosDigitais/Livros e Apostilas/Machine_Learning_Basics.pdf#page=23)
- **🎯 Trecho Relevante:** O aprendizado de máquina utiliza algoritmos de redes neurais para identificar padrões complexos em grandes conjuntos de dados.
- **🚀 [Abrir PDF Automaticamente](rag_open_pdf:book_id=def456&page_number=23)**

## Abertura Direta de PDF

**Usuário:** Abra o PDF do livro "Deep_Learning_Fundamentals" na página 45

**Cascade:** 📂 **PDF Aberto:** Deep_Learning_Fundamentals.pdf  
📄 **Página:** 45  
🔗 **Link Direto:** file:///home/carlosdelfino/workspace/Faculdades e Cursos/GemeosDigitais/Livros e Apostilas/Deep_Learning_Fundamentals.pdf#page=45

💡 **Dica:** Use o link acima se o PDF não abrir automaticamente.

## Busca Específica com Múltiplos Resultados

**Usuário:** `/rag-search-pdf transformer attention mechanism` top_k=3

**Cascade:** 🔍 Buscando por: 'transformer attention mechanism'

📊 **3 resultados encontrados:**

### 📄 **Resultado 1** (Similaridade: 0.934) 🧠 [semântico]
- **Documento:** Attention_Is_All_You_Need.pdf
- **Página:** [📖 Página 3](file:///home/carlosdelfino/workspace/Faculdades e Cursos/GemeosDigitais/Livros e Apostilas/Attention_Is_All_You_Need.pdf#page=3)
- **🎯 Trecho Relevante:** O mecanismo de atenção permite que o modelo foque em diferentes partes da sequência de entrada ao produzir cada elemento da saída.
- **🚀 [Abrir PDF Automaticamente](rag_open_pdf:book_id=ghi789&page_number=3)**

---

## Workflow Completo de Pesquisa

1. **Busca Inicial:** Use `/rag-search-pdf` para encontrar tópicos
2. **Navegação Rápida:** Clique nos links `file://` para abrir PDFs diretamente
3. **Leitura Focada:** Os PDFs abrem na página exata do conteúdo encontrado
4. **Exploração:** Use `rag_open_pdf` para abrir outros livros automaticamente

## Dicas Avançadas

### Combinação de Termos
```
/rag-search-pdf "convolutional neural networks" image recognition
```

### Busca por Autores
```
/rag-search-pdf "Geoffrey Hinton" deep learning
```

### Pesquisa por Conceitos Específicos
```
/rag-search-pdf "backpropagation algorithm" gradient descent
```

## Formatos de Links Suportados

- **Linux:** `file:///path/to/document.pdf#page=45`
- **macOS:** `file:///path/to/document.pdf#page=45`
- **Windows:** `file:///C:/path/to/document.pdf#page=45`

## Visualizadores Compatíveis

- **Adobe Acrobat Reader** - Suporte total a links com página
- **Evince (Linux)** - Suporte nativo
- **Preview (macOS)** - Suporte integrado
- **Navegadores modernos** - Chrome, Firefox, Edge

## Solução de Problemas

### Link não funciona?
1. Verifique se o caminho do arquivo está correto
2. Use `rag_open_pdf` para abrir automaticamente
3. Verifique se o visualizador suporta links com página

### PDF não abre na página correta?
1. Alguns visualizadores mais antigos podem não suportar `#page=N`
2. Abra o PDF normalmente e navegue manualmente
3. Considere atualizar seu visualizador de PDF
