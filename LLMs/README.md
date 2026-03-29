# 🤖 Large Language Models (LLMs) - Módulo de Capacitação

![visitors](https://visitor-badge.laobi.icu/badge?page_id=ArvoreDosSaberes.Capacitacao_GemeosDigitais.LLMs)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![Transformers](https://img.shields.io/badge/Transformers-HuggingFace-yellow)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-LLMs-green)
![Status](https://img.shields.io/badge/Status-Educa%C3%A7%C3%A3o-brightgreen)

## 🎯 Foco do Módulo

Este módulo é dedicado ao **estudo prático e teórico de Large Language Models (LLMs)**, explorando desde os fundamentos matemáticos até implementações avançadas com modelos state-of-the-art. O objetivo é proporcionar uma compreensão profunda de como os modelos de linguagem funcionam internamente e como aplicá-los em cenários reais.

### 📚 Áreas de Estudo

- **Arquiteturas de LLMs**: BERT, GPT-2, IBM Granite e beyond
- **Mecanismos de Atenção**: Fundamentos matemáticos e implementações práticas
- **Tokenização e Embeddings**: Como textos viram representações vetoriais
- **Geração de Texto**: Estratégias de sampling e controle de criatividade
- **Modelos Multilingues**: Comparação entre modelos treinados em diferentes idiomas
- **Fine-tuning e Instrução-tuning**: Técnicas de adaptação de modelos

## 🚀 Como Usar este Módulo

### Pré-requisitos

- Python 3.8 ou superior
- GPU recomendada (para modelos maiores)
- Conhecimento básico de Python e Machine Learning

### Configuração do Ambiente

1. **Instale as dependências:**

   ```bash
   pip install transformers torch scikit-learn -q
   ```

2. **Importe as bibliotecas principais:**

   ```python
   from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
   import torch
   import torch.nn.functional as F
   from sklearn.metrics.pairwise import cosine_similarity
   import numpy as np
   ```

## 📁 Estrutura do Módulo

```text
LLMs/
├── README.md                                    # Este arquivo - documentação completa
├── Aula 3 - LLMs.vtt                           # Vídeo da aula gravada
├── Como-um-modelo-de-linguagem-realmente-funciona-versão-lite.pdf    # Material teórico simplificado
├── Como-um-modelo-de-linguagem-realmente-funciona-versão-média.pdf   # Material teórico completo
├── Modelos-de-Linguagem-Como-maquinas-entendem-texto.pdf             # Material complementar
├── Tutorial_Comparacao_Notebooks.md            # Guia comparativo dos notebooks
├── LLMs_por_dentro.ipynb                      # Notebook original - funcionamento básico
├── LLMs_por_dentro-corrigido_professor.ipynb   # Notebook corrigido - melhor organização
└── LLMs_por_dentro_granite_ibm.ipynb          # Notebook com IBM Granite 4.0
```

## 📊 Notebooks Disponíveis

### 1. LLMs_por_dentro.ipynb - Versão Original
- **Foco**: Introdução ao funcionamento interno de LLMs
- **Conteúdo**: Tokenização, embeddings, mecanismo de atenção
- **Modelos**: BERT, GPT-2 básico
- **Ideal**: Primeiro contato com o tema

### 2. LLMs_por_dentro-corrigido_professor.ipynb - Versão Melhorada
- **Foco**: Mesmo conteúdo com melhorias organizacionais
- **Conteúdo**: Explicações mais detalhadas, melhor fluxo didático
- **Modelos**: BERT, GPT-2, GPT-2 Large, modelo em português
- **Ideal**: Estudo aprofundado e referência

### 3. LLMs_por_dentro_granite_ibm.ipynb - IBM Granite
- **Foco**: Análise comparativa com modelo moderno
- **Conteúdo**: IBM Granite 4.0 Micro vs BERT vs GPT-2
- **Modelos**: IBM Granite 4.0 Micro
- **Ideal**: Comparação de arquiteturas e tecnologias recentes

## 🔍 Conceitos Fundamentais Abordados

### Tokenização
- Como textos são divididos em tokens
- Diferenças entre tokenizadores (BERT vs GPT-2)
- Vocabulários e IDs numéricos

### Embeddings
- Representação vetorial do significado
- Dimensões típicas (768 para BERT/GPT-2)
- Similaridade semântica entre tokens

### Mecanismo de Atenção
- Matrizes Query, Key, Value
- Similaridade contextual entre palavras
- Atenção bidirecional vs causal

### Geração de Texto
- Logits e probabilidades
- Estratégias de sampling (greedy, top-k, top-p)
- Controle de criatividade (temperature)

## 🆚 Comparação de Modelos

| Característica | BERT (2018) | GPT-2 (2019) | Granite 4.0 (2024) |
|---------------|-------------|--------------|-------------------|
| **Arquitetura** | Encoder-only | Decoder-only | Decoder-only |
| **Foco** | Compreensão | Geração | Geração + Compreensão |
| **Atenção** | Bidirecional | Causal | Causal otimizada |
| **Multilingue** | Limitado | Principalmente inglês | Sim, incluindo português |
| **Instruções** | Não | Não | Sim (instrução-tuning) |
| **Vocabulário** | ~30k tokens | ~50k tokens | ~50k tokens otimizado |

## 🛠️ Tecnologias Utilizadas

- **Transformers (Hugging Face)**: Framework principal para modelos
- **PyTorch**: Backend de deep learning
- **Scikit-learn**: Métricas e similaridade
- **NumPy**: Computação numérica
- **Jupyter**: Ambiente interativo de desenvolvimento

## 📖 Exemplo Prático Rápido

### Geração de Texto com GPT-2

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

# Carregar modelo e tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

# Texto de entrada
text = "O gato subiu no"
inputs = tokenizer(text, return_tensors="pt")

# Gerar continuação
output = model.generate(
    **inputs,
    max_length=50,
    do_sample=True,
    top_k=50,
    top_p=0.9,
    temperature=0.7
)

# Resultado
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)
```

### Análise de Embeddings com BERT

```python
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

# Carregar BERT
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# Processar texto
text = "O gato subiu no telhado"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)
embeddings = outputs.last_hidden_state

# Calcular similaridade
emb = embeddings[0].detach().numpy()
similarity_matrix = cosine_similarity(emb)
print("Matriz de similaridade:", similarity_matrix.shape)
```

## 🎯 Fluxo de Aprendizado Recomendado

1. **Comece com o material teórico**:
   - Leia os PDFs fornecidos
   - Assista ao vídeo da Aula 3

2. **Execute os notebooks em ordem**:
   - `LLMs_por_dentro.ipynb` (conceitos básicos)
   - `LLMs_por_dentro-corrigido_professor.ipynb` (aprofundamento)
   - `LLMs_por_dentro_granite_ibm.ipynb` (tecnologia moderna)

3. **Experimente com diferentes parâmetros**:
   - Modifique temperature, top_k, top_p
   - Compare diferentes modelos
   - Teste com seus próprios textos

4. **Consulte o tutorial comparativo**:
   - `Tutorial_Comparacao_Notebooks.md` para entender diferenças

## 📚 Material Complementar

### PDFs Disponíveis
- **Como um modelo de linguagem realmente funciona (versão lite)**: Introdução simplificada
- **Como um modelo de linguagem realmente funciona (versão média)**: Explicação detalhada
- **Modelos de Linguagem - Como máquinas entendem texto**: Material complementar

### Vídeo
- **Aula 3 - LLMs.vtt**: Gravação completa da aula sobre LLMs

## 🚀 Desafios e Exercícios

### Para Estudantes
1. **Modifique os parâmetros de geração** e observe as diferenças
2. **Compare modelos de diferentes tamanhos** (small vs large)
3. **Teste com textos em diferentes idiomas**
4. **Implemente um sistema simples de RAG** usando os conceitos aprendidos

### Para Desenvolvedores
1. **Crie uma API de geração de texto** usando os modelos
2. **Implemente métricas de avaliação** customizadas
3. **Desenvolva um sistema de fine-tuning** para domínios específicos
4. **Construa uma interface web** para interação com os modelos

## ⚠️ Considerações Importantes

### Uso de Recursos
- Modelos grandes (GPT-2 Large, Granite) exigem GPU
- Considere usar Google Colab para acesso a GPUs
- Monitore o uso de memória ao carregar múltiplos modelos

### Limitações dos Modelos
- **Alucinações**: Modelos podem gerar informações falsas
- **Viés**: Podem refletir vieses dos dados de treinamento
- **Repetição**: Configurações inadequadas podem causar loops
- **Idioma**: Modelos em português podem ser limitados

### Boas Práticas
- Use `torch.no_grad()` para inference
- Configure `pad_token_id` para evitar warnings
- Experimente com diferentes estratégias de sampling
- Valide os resultados em aplicações críticas

## 🤔 Perguntas Comuns

### Qual a diferença entre BERT e GPT-2?
- **BERT**: Foco em compreensão, atenção bidirecional
- **GPT-2**: Foco em geração, atenção causal

### Por que os modelos geram textos diferentes?
- LLMs usam geração estocástica (aleatória)
- Parâmetros como temperature controlam a aleatoriedade
- Mesmo com os mesmos parâmetros, resultados podem variar

### Como escolher o modelo certo?
- **Tarefas de compreensão**: BERT ou variantes
- **Geração de texto**: GPT-2 ou Granite
- **Multilingue**: Granite ou modelos específicos
- **Recursos limitados**: Versões "small" ou "micro"

## 🔄 Atualizações e Roadmap

### Versão Atual: 1.0
- ✅ Notebooks fundamentais
- ✅ Material teórico completo
- ✅ Comparação de modelos
- ✅ Exemplos práticos

### Próximas Versões
- [ ] Fine-tuning de modelos customizados
- [ ] Técnicas avançadas de prompt engineering
- [ ] Modelos de visão + linguagem (VLMs)
- [ ] Aplicações específicas para português

## 🤝 Contribuição

Este é um módulo educacional em constante evolução. Contribuições são bem-vindas:

- **Novos exemplos**: Casos de uso e aplicações
- **Melhorias nos notebooks**: Otimizações e correções
- **Material complementar**: Artigos e tutoriais
- **Traduções**: Adaptação para outros idiomas

## 📄 Licença

Este módulo está licenciado sob Creative Commons Attribution-ShareAlike 4.0 International License.

---

## 📞 Suporte e Comunidade

- **Issues**: Reporte problemas ou sugira melhorias
- **Pull Requests**: Contribua diretamente com o conteúdo
- **Discussões**: Participe de conversas sobre LLMs

---

*Última atualização: Março 2026*
*Versão: 1.0 - Módulo completo de LLMs*
