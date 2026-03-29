# 📚 Document Processor - Tutorial Completo

![visitors](https://visitor-badge.laobi.icu/badge?page_id=ArvoreDosSaberes.Capacitacao_GemeosDigitais.Tutorial)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
![Tutorial](https://img.shields.io/badge/Type-Tutorial-orange)
![Educational](https://img.shields.io/badge/Type-Educational-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

## 🎯 Objetivo do Tutorial

Este tutorial completo documenta o **Document Processor**, uma ferramenta poderosa para converter documentos em vários formatos (PDF, EPUB, Djvu) para Markdown limpo, extrair embeddings semânticos e permitir busca por conteúdo usando modelos de linguagem avançados.

## 📋 Sumário

1. [Descrição](#descrição)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Uso Básico](#uso-básico)
5. [Exemplos Práticos](#exemplos-práticos)
6. [Busca Semântica](#busca-semântica)
7. [Gerenciamento de Dados](#gerenciamento-de-dados)
8. [Troubleshooting](#troubleshooting)

---

## 📖 Descrição

O **Document Processor** é uma ferramenta poderosa para converter documentos em vários formatos (PDF, EPUB, Djvu) para Markdown limpo, extrair embeddings semânticos e permitir busca por conteúdo usando modelos de linguagem avançados.

### Funcionalidades Principais

- **🔄 Conversão de Documentos**: PDF, EPUB, Djvu → Markdown
- **🧹 Limpeza Inteligente**: Remove formatação desnecessária
- **🤖 Embeddings Semânticos**: Usa Ollama com modelos especializados
- **🔍 Busca Semântica**: Busca por similaridade de conteúdo
- **💾 Banco de Dados**: SQLite + ChromaDB para armazenamento profissional
- **🔒 Cache Inteligente**: Evita reprocessamento de arquivos
- **📊 Gerenciamento**: IDs únicos, listagem e remoção de livros
- **⚡ Performance**: Processamento em chunks com sobreposição
- **🌐 Multi-idioma**: Suporte a OCR em diferentes idiomas

---

## 🚀 Instalação

### Passo 1: Instalar Dependências Python

```bash
cd /home/carlosdelfino/workspace/Faculdades\ e\ Cursos/GemeosDigitais/scripts
pip install -r requirements.txt
```

### Passo 2: Instalar Dependências de Sistema

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-por poppler-utils
# Para suporte DjVu (opcional)
sudo apt-get install djvulibre-bin
```

#### macOS:
```bash
brew install tesseract poppler
# Para suporte DjVu (opcional)
brew install djvulibre
```

#### Windows:
- Baixe e instale [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
- Baixe e instale [Poppler](https://blog.alivate.com.au/poppler-windows/)
- Para suporte DjVu: Baixe e instale [DjVuLibre](https://djvu.org/)

### Passo 3: Instalar Ollama

```bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Baixe o instalador em https://ollama.ai/
```

---

## ⚙️ Configuração

### Arquivo .env

Crie um arquivo `.env` na pasta `scripts`:

```bash
# Configurações do Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mxbai-embed-large
# Outras opções:
# nomic-embed-text-v2-moe  (para português/multilíngue)
# bge-m3                   (para grandes acervos heterogêneos)

# ⚠️ ATENÇÃO: Uma vez criada a base de embeddings, não é possível trocar o modelo
# Para usar um modelo diferente, apague o diretório .data e recrie com o novo modelo

# Configurações do Conversor
DATA_DIR=.data
CONVERTED_DIR=../Livros e Apostilas/converteds
CHUNK_SIZE=500
CHUNK_OVERLAP=50
SIMILARITY_THRESHOLD=0.3

# Configurações de OCR
TESSERACT_LANG=por
# Para outros idiomas: eng, spa, fra, etc.
```

### Modelos de Embeddings

| Modelo | Caso de Uso | Características |
|--------|-------------|----------------|
| **nomic-embed-text-v2-moe** | Livros em português ou multilíngues | Excelente para português, suporte multilíngue |
| **mxbai-embed-large** | Corpus simples e foco em qualidade | Alta qualidade, bem consolidado |
| **bge-m3** | Acervo grande, heterogêneo e multilíngue | Ideal para grandes volumes de documentos |

### Instalar Modelos

```bash
# Modelo padrão
ollama pull mxbai-embed-large

# Para livros em português
ollama pull nomic-embed-text-v2-moe

# Para grandes acervos multilíngues
ollama pull bge-m3

# Verificar modelos instalados
ollama list
```

---

## 📖 Uso Básico

### Formas de Usar o Script

#### 1. Uso Direto (Mais Simples)

```bash
# Converter um arquivo
python document.py "livro.pdf"

# Converter toda uma pasta
python document.py "./Livros e Apostilas"
```

#### 2. Com Flags (Mais Controle)

```bash
# Converter arquivo específico
python document.py --convert "livro.pdf"

# Converter pasta inteira
python document.py --convert-all "./Livros e Apostilas"

# Buscar nos documentos
python document.py --search "redes neurais"
```

#### 3. Gerenciamento de Livros

```bash
# Listar todos os livros indexados
python document.py --list

# Remover um livro específico pelo ID
python document.py --delete "ABC123DEF4"
```

#### 4. Configuração Avançada

```bash
# Especificar idioma do OCR
python document.py --lang eng "./Livros e Apostilas"
python document.py --lang spa --convert documento_espanhol.pdf

# Configurar chunks personalizados
python document.py --chunk-size 1000 --chunk-overlap 100 --convert livro_grande.pdf
```

---

## 🎯 Exemplos Práticos

### Exemplo 1: Processar Biblioteca de IA

```bash
# Entrar na pasta do projeto
cd /home/carlosdelfino/workspace/Faculdades\ e\ Cursos/GemeosDigitais/scripts

# Processar toda a biblioteca com modelo adequado para português
python document.py --model nomic-embed-text-v2-moe "../Livros e Apostilas"
```

**Saída esperada:**
```
📋 Log iniciado: .data/converter_20260329_101534.log
🎯 Pasta de saída: ../Livros e Apostilas/converteds
🤖 Modelo embeddings: nomic-embed-text-v2-moe
🌐 Idioma OCR: por
⚠️  **ATENÇÃO**: Base de embeddings já existe em .data/chroma_db
⚠️  Para trocar de modelo, apague o diretório .data e recrie com novo modelo
⚠️  Modelo atual: nomic-embed-text-v2-moe
============================================================
[10:15:23] INFO: Verificando modelo Ollama...
[10:15:23] INFO: Modelo nomic-embed-text-v2-moe já está instalado
[10:15:23] INFO: Usando modelo Ollama: nomic-embed-text-v2-moe
[10:15:24] INFO: Encontrados 15 documentos para processar
Convertendo livro1.pdf...
Convertendo PDF |██████████████████████████████████████████████████| 100.0% 343/343 páginas
[10:17:08] SUCCESS: Livro livro1.pdf processado com sucesso! ID: U4C2QtGo41 (47.7s)
```

### Exemplo 2: Buscar Conceitos Específicos

```bash
# Buscar sobre redes neurais
python document.py --search "redes neurais convolucionais"

# Buscar sobre séries temporais
python document.py --search "séries temporais previsão"
```

**Saída esperada:**
```
🔍 Buscando por: 'redes neurais convolucionais'

📊 3 resultados encontrados para 'redes neurais convolucionais':

📈 **Detalhes dos Resultados:**

**Resultado 1** (Similaridade: 0.892)
📄 **Documento:** deep_learning_book.pdf
📖 **Página:** 45
🎯 **Chunk Relevante:** Redes neurais convolucionais (CNNs) são uma classe especial de redes neurais profundas que se destacam no processamento de dados com estrutura de grade, como imagens, através do uso de camadas convolucionais que aplicam filtros para detectar características espaciais hierárquicas.
--------------------------------------------------------------------------------
```

### Exemplo 3: Workflow Completo

```bash
# Passo 1: Configurar modelo para português
echo "OLLAMA_MODEL=nomic-embed-text-v2-moe" >> .env
echo "TESSERACT_LANG=por" >> .env

# Passo 2: Processar documentos
python document.py --convert-all "../Livros e Apostilas"

# Passo 3: Fazer buscas específicas
python document.py --search "inteligência artificial"
python document.py --search "machine learning algoritmos"
python document.py --search "data science python"

# Passo 4: Gerenciar biblioteca
python document.py --list
```

---

## 🔍 Busca Semântica Avançada

### Estratégias de Busca

#### 1. Busca por Conceito
```bash
python document.py --search "aprendizado profundo"
python document.py --search "processamento de linguagem natural"
```

#### 2. Busca por Aplicação
```bash
python document.py --search "previsão de mercado"
python document.py --search "análise de sentimento"
```

#### 3. Busca Multi-idioma
```bash
# Com modelo bge-m3 configurado no .env
python document.py --search "neural networks"
python document.py --search "redes neurais"
```

### Dicas para Buscas Efetivas

- **Seja específico**: "redes neurais convolucionais" é melhor que "redes"
- **Use termos técnicos**: "backpropagation" em vez de "treinamento"
- **Combine conceitos**: "transformer attention mechanism"
- **Varie os termos**: Tente sinônimos se não encontrar resultados

---

## 📊 Gerenciamento de Dados

### Estrutura de Diretórios

```
.data/
├── documents.db          # Banco SQLite com metadados
├── chroma_db/           # Banco ChromaDB com embeddings
│   ├── chroma.sqlite3
│   └── document_embeddings/
├── converter_*.log      # Logs de processamento
└── ../Livros e Apostilas/
    └── converteds/       # Arquivos Markdown
        ├── livro1.md
        └── livro2.md
```

### IDs Únicos de Livros

Cada livro recebe um ID alfanumérico de 10 caracteres (ex: `U4C2QtGo41`):

```bash
# Listar livros com IDs
python document.py --list

# Saída:
📚 3 livros indexados:

| ID | Livro | Tamanho | Processado em | Chunks |
|----|-------|--------|--------------|--------|
| U4C2QtGo41 | livro_ia.pdf | 15.2MB | 29/03/2026 10:15 | 45 |
| XYZ789GHI2 | deep_learning.epub | 8.7MB | 29/03/2026 10:20 | 28 |
| MNO456PQR3 | python_guide.pdf | 12.1MB | 29/03/2026 10:25 | 38 |
```

### Cache Inteligente

O sistema detecta automaticamente arquivos modificados:

```bash
# Se executar novamente, pula arquivos não modificados
python document.py --convert-all "../Livros e Apostilas"

# Saída:
[10:20:15] INFO: Livro livro_ia.pdf já processado e inalterado (ID: U4C2QtGo41)
[10:20:16] INFO: Livro livro_novo.pdf modificado, reprocessando (ID: XYZ789GHI2)
```

### Remoção de Livros

```bash
# Remover livro específico
python document.py --delete "U4C2QtGo41"

# Saída:
🗑️  Removendo livro: livro_ia.pdf (ID: U4C2QtGo41)
✅ Removido: ../Livros e Apostilas/converteds/livro_ia.md
✅ Embeddings do livro U4C2QtGo41 removidos do ChromaDB
✅ Livro 'U4C2QtGo41' removido com sucesso!
```

---

## ⚙️ Configuração Avançada

### Troca de Modelo (⚠️ Importante)

**AVISO**: Uma vez criada a base de embeddings, não é possível trocar o modelo sem recriar a base.

```bash
# Para trocar de modelo:
# 1. Apagar base antiga
rm -rf .data

# 2. Configurar novo modelo no .env
echo "OLLAMA_MODEL=bge-m3" >> .env

# 3. Recriar base com novo modelo
python document.py --convert-all "../Livros e Apostilas"
```

### Performance para Grandes Acervos

```bash
# Usar chunks maiores para menos overhead
python document.py --chunk-size 1000 --chunk-overlap 150 --convert-all "./documentos_longos"

# Ajustar threshold de similaridade
echo "SIMILARITY_THRESHOLD=0.2" >> .env  # Mais resultados
echo "SIMILARITY_THRESHOLD=0.4" >> .env  # Mais precisão
```

### Configuração de OCR

```bash
# Inglês
python document.py --lang eng --convert documento_ingles.pdf

# Espanhol
python document.py --lang spa --convert documento_espanhol.pdf

# Francês
python document.py --lang fra --convert documento_frances.pdf
```

---

## 🛠️ Troubleshooting

### Problemas Comuns

#### 1. "Modelo não encontrado"
```bash
# Verificar modelos disponíveis
ollama list

# Instalar modelo específico
ollama pull nomic-embed-text-v2-moe
```

#### 2. "Tesseract não encontrado"
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-por

# macOS
brew install tesseract
```

#### 3. "Base de embeddings incompatível"
```bash
# Se mudou o modelo no .env
rm -rf .data
python document.py --convert-all "../Livros e Apostilas"
```

#### 4. "Memória insuficiente"
```bash
# Reduzir tamanho dos chunks
echo "CHUNK_SIZE=300" >> .env
echo "CHUNK_OVERLAP=50" >> .env
```

### Logs e Debug

O sistema gera logs detalhados:

```bash
# Ver logs de processamento
ls .data/converter_*.log

# Log em tempo real
python document.py --convert livro.pdf 2>&1 | tee processamento.log
```

### Performance Tips

1. **Use SSD** para armazenar `.data/`
2. **Memória RAM**: Mínimo 8GB para grandes acervos
3. **Processador**: Multi-core acelera extração de embeddings
4. **Modelo**: Escolha adequado ao volume de documentos

---

## 🎓 Exemplo de Workflow Completo

### Cenário: Pesquisa sobre "Deep Learning"

```bash
# 1. Configurar ambiente
cd /home/carlosdelfino/workspace/Faculdades\ e\ Cursos/GemeosDigitais/scripts
echo "OLLAMA_MODEL=nomic-embed-text-v2-moe" >> .env
echo "TESSERACT_LANG=por" >> .env

# 2. Instalar modelo
ollama pull nomic-embed-text-v2-moe

# 3. Processar biblioteca
python document.py --convert-all "../Livros e Apostilas"

# 4. Fazer buscas específicas
python document.py --search "deep learning"
python document.py --search "redes neurais profundas"
python document.py --search "tensorflow keras pytorch"

# 5. Gerenciar resultados
python document.py --list
```

### Resultados Esperados

- **Documentos processados**: Todos em `../Livros e Apostilas/converteds/`
- **Embeddings gerados**: Em `.data/chroma_db/`
- **Metadados**: Em `.data/documents.db`
- **Buscas semânticas**: Resultados com scores de similaridade
- **Cache inteligente**: Reprocessamento automático apenas de novos arquivos

---

## 📈 Próximos Passos

1. **Experimente diferentes modelos** para seu caso de uso
2. **Crie scripts de busca** para pesquisas recorrentes
3. **Integre com outras ferramentas** (Jupyter, VSCode)
4. **Backup do .data** é recomendado para acervos valiosos

---

## 💡 Dicas Finais

- **Comece pequeno**: Teste com poucos documentos primeiro
- **Escolha o modelo certo** para seu tipo de conteúdo
- **Use buscas específicas** para melhores resultados
- **Monitore espaço em disco** para grandes acervos
- **⚠️ ATENÇÃO**: Configure o modelo desejado no `.env` ANTES de processar documentos

---

*Última atualização: Março 2026*  
*Versão: 2.0 - Tutorial Completo com SQLite + ChromaDB*  
*Script: `document.py`*
