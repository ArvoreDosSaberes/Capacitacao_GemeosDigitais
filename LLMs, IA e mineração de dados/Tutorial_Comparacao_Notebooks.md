![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=Tutorial%20Comparativo%20de%20Notebooks&fontSize=40&fontAlignY=35&animation=twinkling)

# 📊 Tutorial Comparativo: LLMs_por_dentro.ipynb vs LLMs_por_dentro-corrigido_professor.ipynb

![visitors](https://visitor-badge.laobi.icu/badge?page_id=ArvoreDosSaberes.Capacitacao_GemeosDigitais.LLMs.Tutorial_Comparacao)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
![Tutorial](https://img.shields.io/badge/Type-Tutorial-orange)
![Jupyter](https://img.shields.io/badge/Format-Jupyter%20Notebook-blue)
![Status](https://img.shields.io/badge/Status-Reference-green)

## 📋 Visão Geral

Este tutorial compara duas versões do notebook sobre funcionamento interno de Large Language Models (LLMs), identificando as diferenças e explicando o impacto de cada modificação.

---

## 📐 Estrutura Comparativa

| Aspecto | LLMs_por_dentro.ipynb (Original) | LLMs_por_dentro-corrigido_professor.ipynb (Corrigido) |
|---------|----------------------------------|--------------------------------------------------------|
| **Total de Células** | 84 células | 85 células |
| **Conteúdo Principal** | Funcionamento básico de LLMs | Mesmo conteúdo com correções e melhorias |
| **Organização** | Boa | Slightly melhorada |

## 🔍 Principais Diferenças Identificadas

### 🔧 1. Instalação de Dependências (Células 38-39)

**Original:**
```python
!pip install transformers torch -q
```

**Corrigido:**
```python
# Instala bibliotecas necessárias (já instaladas anteriormente, mas mantido para completude)
!pip install transformers torch -q
```

**Impacto:** ✅ **Melhoria de Clareza**
- Adicionou comentário explicativo
- Reconhece que bibliotecas já foram instaladas anteriormente
- Mantém completude do código

### 💬 2. Geração de Texto com GPT-2 (Células 63, 69-70)

**Original:**
```python
# max_length=20
# Resultado: "O gato subiu no yu.\n\nI've always been a huge fan of the"
```

**Corrigido:**
```python
# max_length=20  
# Resultado: "O gato subiu no kara no kara no kara no kara no kara"
```

**Impacto:** ⚠️ **Diferença de Comportamento**
- Original gerou texto misturando português e inglês
- Corrigido mostrou comportamento de repetição (loop)
- Ambos demonstram problemas diferentes do modelo

### 🇧🇷 3. Modelo em Português (Células 73-74)

**Original:**
```python
# Código em célula única com tudo junto
# Carregando modelo e tokenizer em português
tokenizer_pt = AutoTokenizer.from_pretrained("pierreguillou/gpt2-small-portuguese")
# ... resto do código
```

**Corrigido:**
```python
# Dividido em duas células:
# Célula 73: Explicação e setup
# Célula 74: Execução do código
```

**Impacto:** ✅ **Melhoria Organizacional**
- Melhor separação entre explicação e execução
- Facilita entendimento passo a passo

### 📝 4. Resultados do Modelo Português

**Original:**
```
O gato subiu no dia seguinte e ficou para trás, mas não conseguiu evitar a chegada de um outro gato. Ele então foi para a sala, onde ficou o gato, que estava segurando o coração do gato. Quando os dois começaram a se aproximar,
```

**Corrigido:**
```
O gato subiu no teto e caiu sobre o chão, enquanto a fêmea ainda estava viva. O gato foi então levado ao seu estado de putremo em um hospital. A história da doença foi retratada na série animada da Nickelodeon, "The Fantag
```

**Impacto:** ⚠️ **Diferença de Execução**
- Resultados diferentes devido à natureza estocástica do modelo
- Ambos demonstram comportamento "alucinatório" do modelo
- Corrigido é ligeiramente mais mórbido

### 🚀 5. GPT-2 Large (Células 80-83)

**Original:**
```python
# Células 80-83 contêm código e resultados
text_en = "The cat climbed onto the"
# Resultado: texto sobre o gato no chão olhando para o narrador
```

**Corrigido:**
```python
# Mesmo código, resultados ligeiramente diferentes
# Resultado: texto similar mas com pequenas variações
```

**Impacto:** ⚠️ **Variação Normal**
- Pequenas diferenças na geração são normais em LLMs
- Ambos demonstram capacidade superior do modelo larger

## 📊 Análise de Impacto

### ✨ Melhorias Implementadas

1. **Clareza do Código:** Comentários mais descritivos
2. **Organização:** Melhor separação de conceitos
3. **Didática:** Explicações mais detalhadas em alguns pontos

### ⚡ Diferenças Comportamentais

1. **Geração Estocástica:** Resultados diferentes são normais em LLMs
2. **Consistência:** Ambos os notebooks demonstram os mesmos conceitos fundamentais
3. **Comportamento do Modelo:** Ambos mostram limitações e características dos modelos

### 🎯 Qualidade Técnica

| Aspecto | Original | Corrigido | Avaliação |
|---------|----------|-----------|-----------|
| **Precisão Técnica** | ✅ Excelente | ✅ Excelente | Mantida |
| **Clareza Didática** | ✅ Boa | ✅ Melhor | Leve melhoria |
| **Organização** | ✅ Boa | ✅ Melhor | Leve melhoria |
| **Completude** | ✅ Completo | ✅ Completo | Mantida |

## 🎓 Impacto Educacional

### 📚 Conceitos Mantidos em Ambos:

1. **Tokenização:** Explicação clara de como textos viram tokens
2. **Embeddings:** Demonstração de representação vetorial
3. **Mecanismo de Atenção:** Matriz de similaridade bem explicada
4. **Geração de Texto:** Exemplos práticos com diferentes parâmetros
5. **Limitações:** Demonstração de alucinações e repetições

### 🌟 Melhorias na Versão Corrigida:

1. **Fluxo Mais Lógico:** Separação melhor entre setup e execução
2. **Comentários Descritivos:** Explicações mais detalhadas
3. **Consistência:** Pequenos ajustes para melhor compreensão

## 💡 Recomendações de Uso

### 🎓 Para Estudantes Iniciantes:
- **Use a versão corrigida** - melhor organização e clareza
- Execute ambas para ver variações na geração
- Foque nos conceitos, não nos resultados exatos

### 👨‍🏫 Para Professores:
- **Versão corrigida** é melhor para apresentação
- Use diferenças de resultados para explicar natureza estocástica
- Destaque que ambos demonstram os mesmos princípios

### 💻 Para Desenvolvedores:
- Ambos servem como referência técnica
- Código é funcional em ambas as versões
- Considere as melhorias organizacionais da versão corrigida

## 🏁 Conclusão

A versão corrigida pelo professor representa uma **evolução incremental** do notebook original, com melhorias significativas em:

- **Organização do conteúdo**
- **Clareza das explicações**
- **Fluxo didático**

No entanto, **ambos os notebooks são excelentes recursos educacionais** que demonstram eficazmente o funcionamento interno de LLMs. As diferenças nos resultados de geração são esperadas e até desejáveis, pois ilustram a natureza probabilística desses modelos.

**Recomendação final:** Utilize a versão corrigida como principal, mas mantenha o original como referência para entender variações de comportamento dos modelos.

---

## 📄 Informações do Documento

*Este tutorial compara notebooks de LLMs para a Capacitação em Gêmeos Digitais, pertencente ao projeto ArvoreDosSaberes e organização ArvoreDosSaberes.*

**Repositório:** [Capacitacao_GemeosDigitais](https://github.com/ArvoreDosSaberes/Capacitacao_GemeosDigitais)  
**Organização:** [ArvoreDosSaberes](https://github.com/ArvoreDosSaberes)  
**Data de criação:** 2026  
**Licença:** CC BY-SA 4.0

![footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer&animation=twinkling)
