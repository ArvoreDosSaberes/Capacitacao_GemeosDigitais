# Gêmeos Digitais - Capacitação em Tecnologia

![visitors](https://visitor-badge.laobi.icu/badge?page_id=ArvoreDosSaberes.Capacitacao_GemeosDigitais)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Prática-green)
![Status](https://img.shields.io/badge/Status-Educa%C3%A7%C3%A3o-brightgreen)
![Repository Size](https://img.shields.io/github/repo-size/ArvoreDosSaberes/Capacitacao_GemeosDigitais)
![Last Commit](https://img.shields.io/github/last-commit/ArvoreDosSaberes/Capacitacao_GemeosDigitais)

## 🎯 Foco do Repositório

Este repositório é dedicado à **capacitação profissional** em diversas áreas da tecnologia, oferecendo material educacional estruturado e prático. O objetivo principal é fornecer um caminho de aprendizado completo, desde conceitos fundamentais até aplicações avançadas.

### 📚 Áreas de Capacitação

- **Inteligência Artificial e Machine Learning**: Exemplos práticos e implementações didáticas
- **Análise de Dados**: Exploração e visualização de conjuntos de dados
- **Desenvolvimento de Software**: Boas práticas e padrões modernos
- **Ciência de Dados**: Fluxos completos de trabalho e estudos de caso

Cada área de capacitação está organizada em sua própria pasta, com material específico e exemplos práticos.

## 🚀 Como Usar com VSCode/Windsurf

### Pré-requisitos

- Python 3.8 ou superior
- Git instalado
- VSCode ou Windsurf

### Configuração do Ambiente

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/ArvoreDosSaberes/Capacitacao_GemeosDigitais.git
   cd Capacitacao_GemeosDigitais
   ```

2. **Crie e ative o ambiente virtual:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências (para cada módulo):**

   ```bash
   # Para o módulo de Inteligência Artificial
   cd InteligenciaArtificial
   pip install -r requirements.txt
   cd ..
   ```

### Configuração do VSCode/Windsurf

1. **Instale as extensões recomendadas:**
   - Python (Microsoft)
   - Jupyter (Microsoft)
   - Python Docstring Generator (Nils Werner)
   - GitLens (GitKraken)

2. **Selecione o interpretador Python:**
   - Abra a paleta de comandos (`Ctrl+Shift+P`)
   - Digite "Python: Select Interpreter"
   - Escolha o interpretador do ambiente virtual (`.venv`)

3. **Trabalhe com os notebooks:**
   - Navegue até o módulo desejado (ex: `cd InteligenciaArtificial`)
   - Abra o notebook correspondente (ex: `Aula_1_notebook_ml_churn_colab.ipynb`)
   - Execute as células interativamente
   - Use o modo de depuração para entender o fluxo

### Dicas para Windsurf

- **Autocomplete inteligente**: O Windsurf oferece sugestões contextuais para código ML
- **Chat integrado**: Use o chat para tirar dúvidas sobre os conceitos
- **Debug visual**: Aproveite as ferramentas de visualização de dados integradas

## 📁 Estrutura do Projeto

```text
GemeosDigitais/
├── README.md                    # Este arquivo - visão geral da capacitação
├── .gitignore                   # Arquivos ignorados pelo Git
├── .venv/                      # Ambiente virtual (não commitado)
├── InteligenciaArtificial/      # 🤖 Módulo de IA e Machine Learning
│   ├── README.md               # Documentação específica do módulo
│   ├── requirements.txt        # Dependências Python para IA
│   ├── Aula_1_notebook_ml_churn_colab.ipynb  # Notebook principal
│   └── test_notebook.py        # Scripts de teste
└── [outras_pastas]/             # 📚 Outros módulos de capacitação (em desenvolvimento)
    └── README.md               # Documentação específica de cada módulo
```

### 🎯 Navegando pelos Módulos

Cada pasta representa uma área de capacitação específica:

- **`InteligenciaArtificial/`**: Foco em Machine Learning, análise de dados e IA
- **[Outras pastas]**: Demais áreas tecnológicas (a serem adicionadas)

Dentro de cada módulo você encontrará:

- Material didático específico da área
- Exemplos práticos e exercícios
- Ambiente configurado com dependências adequadas
- Documentação detalhada do conteúdo

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal
- **Pandas**: Manipulação de dados
- **NumPy**: Computação numérica
- **Matplotlib/Seaborn**: Visualização de dados
- **Scikit-learn**: Machine Learning
- **KaggleHub**: Acesso a datasets
- **Jupyter**: Notebooks interativos

## 📖 Exemplo de Uso - Módulo de Inteligência Artificial

O notebook principal do módulo de IA demonstra um fluxo completo de Machine Learning:

1. **Exploração de Dados**: Análise inicial do dataset
2. **Preparação**: Limpeza e transformação
3. **Treinamento**: Construção do modelo
4. **Avaliação**: Métricas de desempenho

### Dataset Utilizado

- **Fonte**: [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- **Tamanho**: 7.043 clientes
- **Objetivo**: Prever cancelamento de serviços

### 🎯 Como Acessar

```bash
# Entre no diretório do módulo
cd InteligenciaArtificial

# Abra o notebook no VSCode/Windsurf
code Aula_1_notebook_ml_churn_colab.ipynb
```

## 🤝 Contribuição

Este é um projeto educacional com estrutura modular. Contribuições são bem-vindas nos seguintes formatos:

- **Novos módulos**: Crie novas pastas para outras áreas de capacitação
- **Exemplos práticos**: Adicione casos de uso e exercícios aos módulos existentes
- **Melhorias na documentação**: Aprimore READMEs e materiais didáticos
- **Correções pedagógicas**: Sugestões para melhorar o aprendizado
- **Cases de uso**: Exemplos reais e aplicações práticas

### 📝 Guia para Novos Módulos

1. Crie uma nova pasta com nome descritivo
2. Adicione um README.md específico do módulo
3. Inclua exemplos práticos e exercícios
4. Documente as dependências necessárias
5. Siga a estrutura estabelecida

## 📄 Licença

Este projeto está licenciado sob Creative Commons Attribution-ShareAlike 4.0 International License.

---

## 🚀 Aprendizado Contínuo
