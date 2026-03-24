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

Este repositório é dedicado à **capacitação profissional** em Gemeos Digitais e 5G, oferecendo material educacional estruturado e prático. O objetivo principal é fornecer um caminho de aprendizado completo, desde conceitos fundamentais até aplicações avançadas.

As aulas são disponibilizadas via AVA no link: [https://gemeodigital.unicorporativa.com/](https://gemeodigital.unicorporativa.com/)

### 📚 Áreas de Capacitação

- **Inteligência Artificial e Machine Learning**: Exemplos práticos e implementações didáticas
- **Análise de Séries Temporais**: Previsão e modelagem de dados temporais com técnicas avançadas
- **Análise de Dados**: Exploração e visualização de conjuntos de dados
- **Desenvolvimento de Software**: Boas práticas e padrões modernos
- **Ciência de Dados**: Fluxos completos de trabalho e estudos de caso

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

   # Para o módulo de Séries Temporais
   cd SeriesTemporais
   pip install -r requirements.txt
   cd ..
   ```

### Configuração do VSCode/Windsurf

1. **Instale as extensões recomendadas:**

   - Python (Microsoft)
   - Jupyter (Microsoft)
   - Python Docstring Generator (Nils Werner)
   - GitLens (GitKraken)
   - EPubReader (Epubside)
   - Office Reader (Cweijan)
   - Mrkdownlint (DavidAnson)
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

## � Como Usar com Obsidian

### O que é o Obsidian?

O **Obsidian** é uma aplicação de notas poderosa baseada em Markdown que funciona com arquivos locais. É ideal para organizar conhecimento, criar mapas mentais conectados e manter uma base de conhecimento pessoal estruturada.

### 📥 Download e Instalação

#### 🔗 Link Oficial

Baixe o Obsidian diretamente do site oficial: [https://obsidian.md/](https://obsidian.md/)

#### 🐧 Instalação no Linux

**Método 1: Download Direto (Recomendado)**

1. Acesse [https://obsidian.md/download](https://obsidian.md/download)
2. Baixe o arquivo `.AppImage` para Linux
3. Torne o arquivo executável:
   ```bash
   chmod +x Obsidian-*.AppImage
   ```
4. Execute o aplicativo:
   ```bash
   ./Obsidian-*.AppImage
   ```

**Método 2: Via Snap (Alternativa)**

```bash
sudo snap install obsidian --classic
```

**Método 3: Via Flatpak (Alternativa)**

```bash
flatpak install flathub md.obsidian.Obsidian
```

#### 🪟 Instalação no Windows

**Método 1: Download Direto (Recomendado)**

1. Acesse [https://obsidian.md/download](https://obsidian.md/download)
2. Baixe o instalador `.exe` para Windows
3. Execute o arquivo baixado
4. Siga o assistente de instalação (Next → Install → Finish)

**Método 2: Via Microsoft Store**

1. Abra a Microsoft Store
2. Pesquise por "Obsidian"
3. Clique em "Get" ou "Install"

**Método 3: Via Chocolatey**

```powershell
choco install obsidian
```

**Método 4: Via Winget**

```powershell
winget install Obsidian.Obsidian
```

### ⚙️ Configuração Inicial

1. **Abra o Vault Existente**: Ao abrir o Obsidian pela primeira vez, escolha "Open folder as vault"
2. **Selecione este Repositório**: Navegue até a pasta raiz deste projeto (`GemeosDigitais`)
3. **Escolha o Tema**: Selecione entre tema claro ou escuro
4. **Explore Plugins**: Acesse Settings → Community plugins para instalar extensões

### 🚀 Dicas para Uso com Este Projeto

- **Abra este repositório como vault**: Use a pasta raiz do projeto como seu vault
- **Aproveite os links**: Navegue facilmente entre os arquivos markdown
- **Use o Graph View**: Visualize as conexões entre os diferentes módulos
- **Plugins recomendados**:
  - `Kanban` para organização de tarefas
  - `Calendar` para planejamento
  - `Dataview` para consultas avançadas

## �📁 Estrutura do Projeto

```text
GemeosDigitais/
├── README.md                    # Este arquivo - visão geral da capacitação
├── .gitignore                   # Arquivos ignorados pelo Git
├── .venv/                      # Ambiente virtual (não commitado)
├── InteligenciaArtificial/      # 🤖 Módulo de IA e Machine Learning
│   ├── README.md               # Documentação específica do módulo
│   ├── requirements.txt        # Dependências Python para IA
│   ├── Aula_1_notebook_ml_churn_colab.ipynb  # Notebook principal
│   ├── Pratica-construindo-um-modelo-de-aprendizado-de-maquina.pdf  # Material prático
│   ├── Teoria-Aprendizado-de-Maquina-Conceitos-Fundamentais-e-Tipos-de-Modelos.pdf  # Material teórico
│   └── test_notebook.py        # Scripts de teste
├── SeriesTemporais/             # 📈 Módulo de Análise de Séries Temporais
│   ├── Aula_2_Séries_temporais_Fundamentos_de_IA.ipynb  # Notebook principal de séries temporais
│   ├── ttm_getting_started.ipynb  # Notebook TinyTimeMixer
│   ├── Modelos-Estatisticos-e-Autorregressivos.pdf  # Material teórico de modelos
│   └── Preparacao-e-Modelagem-de-Series-Temporais.pdf  # Guia de preparação
└── [outras_pastas]/             # 📚 Outros módulos de capacitação (em desenvolvimento)
    └── README.md               # Documentação específica de cada módulo
```

### 🎯 Navegando pelos Módulos

Cada pasta representa uma área de capacitação específica:

- **`InteligenciaArtificial/`**: Foco em Machine Learning, análise de dados e IA
- **`SeriesTemporais/`**: Análise e previsão de séries temporais com modelos estatísticos e de IA
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
- **TinyTimeMixer (TTM)**: Modelos pré-treinados para séries temporais
- **Statsmodels**: Modelos estatísticos para séries temporais

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

## 📈 Exemplo de Uso - Módulo de Séries Temporais

O módulo de Séries Temporais oferece duas abordagens complementares:

### 1. Fundamentos de Séries Temporais com IA

Notebook: `Aula_2_Séries_temporais_Fundamentos_de_IA.ipynb`

- **Conceitos Fundamentais**: Entendendo padrões temporais
- **Decomposição**: Tendência, sazonalidade e resíduos
- **Modelos Estatísticos**: ARIMA, SARIMA e variantes
- **Previsão com Machine Learning**: Redes neurais e ensemble methods
- **Validação de Modelos**: Backtesting e métricas de precisão

### 2. TinyTimeMixer (TTM) - Modelos Pré-treinados

Notebook: `ttm_getting_started.ipynb`

- **Zero-shot Forecasting**: Previsões sem treinamento específico
- **Few-shot Learning**: Fine-tuning rápido com poucos dados
- **Modelos IBM Granite**: Acesso a modelos state-of-the-art
- **Context Length Flexível**: Configurações de 512 a 1024 pontos
- **Forecast Horizon**: Previsões de até 96 períodos futuros

### 🚀 Acesso ao Módulo de Séries Temporais

```bash
# Entre no diretório do módulo
cd SeriesTemporais

# Para fundamentos de séries temporais
code Aula_2_Séries_temporais_Fundamentos_de_IA.ipynb

# Para TinyTimeMixer
code ttm_getting_started.ipynb
```

### 📚 Bibliografia Recomendada

Consulte a **[Bibliografia Completa](./Livros%20e%20Apostilas/README.md.md)** com todos os livros organizados por área de conhecimento, incluindo resumos detalhados de cada obra.

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

---

## 📓 Material Complementar - UniFacens

### ⚠️ Aviso Importante sobre PDFs

Os materiais em formato PDF disponibilizados neste repositório são **propriedade intelectual da UniFacens** e foram compartilhados exclusivamente para facilitar o acesso dos alunos da **Capacitação Gêmeos Digitais**.

### 📋 Direitos de Uso

- ✅ **Permitido**: Acesso e uso pelos alunos matriculados na capacitação
- ✅ **Permitido**: Download para estudo pessoal
- ❌ **Proibido**: Reprodução e distribuição não autorizada
- ❌ **Proibido**: Uso comercial ou compartilhamento externo
- ❌ **Proibido**: Alteração ou modificação do conteúdo

### 🎓 Finalidade Educacional

Estes materiais foram compartilhados com propósito estritamente educacional para apoiar o aprendizado dos participantes do programa de capacitação. O uso indevido pode violar direitos autorais e as políticas institucionais da UniFacens.

---

## 📄 Licença

Este projeto está licenciado sob Creative Commons Attribution-ShareAlike 4.0 International License.

---

## 🚀 Aprendizado Contínuo

Este repositório está em constante evolução, acompanhando as tendências e melhores práticas do mercado de tecnologia. A metodologia de aprendizado é baseada em:

### 🎓 Metodologia de Ensino

- **Aprendizado Prático**: Cada conceito é acompanhado de implementações reais
- **Progressão Estruturada**: Do básico ao avançado, com solidificação gradual do conhecimento
- **Casos de Uso Reais**: Exemplos aplicáveis a cenários do mundo real
- **Documentação Completa**: Material teórico e prático integrados

### 🔄 Atualizações Recentes

- **✨ Novo Módulo de Séries Temporais**: Técnicas avançadas de previsão com TinyTimeMixer
- **📚 Material Complementar**: PDFs teóricos e guias práticos para cada módulo
- **🔧 Ferramentas Modernas**: Integração com modelos pré-treinados e frameworks atualizados

### 📈 Roadmap de Desenvolvimento

- [ ] **Deep Learning**: Redes neurais profundas para visão computacional
- [ ] **NLP**: Processamento de linguagem natural com transformers
- [ ] **MLOps**: Operacionalização de modelos de machine learning
- [ ] **Data Engineering**: Pipelines e arquitetura de dados
- [ ] **Cloud Computing**: Deploy em nuvem e serverless

### 💡 Dicas de Estudo

1. **Siga a ordem recomendada**: Comece pelos fundamentos antes de avançar
2. **Pratique com os notebooks**: Modifique parâmetros e experimente variações
3. **Consulte o material teórico**: Use os PDFs para aprofundar conceitos
4. **Crie seus próprios projetos**: Aplique o conhecimento em novos problemas
5. **Compartilhe suas descobertas**: Contribua com melhorias e exemplos

---

## Comunidade e Suporte

Este projeto faz parte de uma iniciativa maior de educação em tecnologia. Para dúvidas, sugestões e contribuições:

- **Issues**: Reporte problemas ou sugira melhorias
- **Pull Requests**: Contribua diretamente com o conteúdo
- **Discussões**: Participe de conversas sobre os temas abordados

---

*Última atualização: Março 2026*
*Versão: 2.0 - Com novo módulo de Séries Temporais*
