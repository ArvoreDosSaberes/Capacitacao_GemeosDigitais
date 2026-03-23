# Módulo de Análise de Séries Temporais

![visitors](https://visitor-badge.laobi.icu/badge?page_id=ArvoreDosSaberes.Capacitacao_GemeosDigitais.SeriesTemporais)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![Time Series](https://img.shields.io/badge/Time%20Series-Forecasting-green)
![TinyTimeMixer](https://img.shields.io/badge/TTM-IBM%20Granite-purple)
![Statsmodels](https://img.shields.io/badge/Statsmodels-Econometrics-blue)
![Status](https://img.shields.io/badge/Status-Educa%C3%A7%C3%A3o-brightgreen)
![Level](https://img.shields.io/badge/Level-Intermediate%20to%20Advanced-yellow)

## 📋 Visão Geral

Este módulo oferece capacitação completa em Análise de Séries Temporais, combinando técnicas estatísticas tradicionais com abordagens modernas de Machine Learning. O material está organizado para proporcionar um aprendizado progressivo, desde conceitos fundamentais até modelos state-of-the-art como TinyTimeMixer.

### 🎯 Objetivos de Aprendizagem

- Compreender os fundamentos de séries temporais e padrões temporais
- Dominar técnicas de decomposição e análise exploratória
- Implementar modelos estatísticos clássicos (ARIMA, SARIMA)
- Aplicar modelos de Machine Learning para previsão
- Utilizar modelos pré-treinados (TinyTimeMixer) para forecasting
- Avaliar desempenho de previsões com métricas adequadas
- Aplicar técnicas de validação temporal e backtesting

## 🚀 Configuração do Ambiente

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Ambiente virtual recomendado
- Conhecimento básico de Python e estatística

### Instalação das Dependências

```bash
# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências básicas
pip install pandas numpy matplotlib seaborn
pip install scikit-learn statsmodels

# Para TinyTimeMixer (opcional)
pip install tsfm-public

# Para datasets e utilitários
pip install kagglehub
```

### Dependências Principais

- **pandas**: Manipulação e análise de dados temporais
- **numpy**: Computação numérica e arrays
- **matplotlib**: Visualização de séries temporais
- **seaborn**: Visualizações estatísticas avançadas
- **statsmodels**: Modelos estatísticos e econometria
- **scikit-learn**: Machine Learning para séries temporais
- **tsfm-public**: TinyTimeMixer e modelos pré-treinados

## 📁 Estrutura do Módulo

```text
SeriesTemporais/
├── README.md                                                    # Este arquivo - documentação completa
├── Aula_2_Séries_temporais_Fundamentos_de_IA.ipynb            # Notebook principal de fundamentos
├── ttm_getting_started.ipynb                                  # Notebook TinyTimeMixer
├── Modelos-Estatisticos-e-Autorregressivos.pdf                # Material teórico de modelos
└── Preparacao-e-Modelagem-de-Series-Temporais.pdf             # Guia prático de preparação
```

## 📚 Material Didático

### 📖 Material Teórico

#### PDF: Modelos Estatísticos e Autorregressivos

- Fundamentos de séries temporais
- Componentes: tendência, sazonalidade, ciclo e resíduos
- Modelos ARIMA, SARIMA e variantes
- Testes de estacionariedade (ADF, KPSS)
- Funções de autocorrelação (ACF, PACF)
- Modelos de volatilidade (GARCH)
- Previsão e intervalos de confiança

### 🛠️ Material Prático

#### PDF: Preparação e Modelagem de Séries Temporais

- Checklist de pré-processamento
- Tratamento de valores ausentes
- Detecção de outliers e anomalias
- Feature engineering para séries temporais
- Validação cruzada temporal
- Métricas de avaliação (MAE, RMSE, MAPE, SMAPE)
- Backtesting e validação de modelos
- Deploy de modelos de forecasting

---

## 🎯 Tutoriais Práticos

### 📊 Tutorial 1: Fundamentos de Séries Temporais com IA

**Notebook**: `Aula_2_Séries_temporais_Fundamentos_de_IA.ipynb`

Este tutorial aborda o ciclo completo de análise de séries temporais:

1. **Análise Exploratória**
   - Visualização de séries temporais
   - Identificação de padrões e tendências
   - Análise de sazonalidade

2. **Decomposição de Séries**
   - Separação de componentes
   - Análise de resíduos
   - Verificação de estacionariedade

3. **Modelos Estatísticos**
   - ARIMA e suas variantes
   - Seleção automática de parâmetros
   - Diagnóstico de modelos

4. **Machine Learning para Séries Temporais**
   - Features baseadas em tempo
   - Modelos de árvore e ensemble
   - Redes neurais simples

5. **Validação e Avaliação**
   - Divisão temporal de dados
   - Backtesting
   - Comparação de modelos

### 🤖 Tutorial 2: TinyTimeMixer - Modelos Pré-treinados

**Notebook**: `ttm_getting_started.ipynb`

Este tutorial demonstra o uso de modelos state-of-the-art:

1. **Introdução ao TinyTimeMixer**
   - Arquitetura e conceitos
   - Modelos pré-treinados IBM Granite
   - Context length e forecast horizon

2. **Zero-shot Forecasting**
   - Previsão sem treinamento específico
   - Configuração de parâmetros
   - Avaliação de desempenho

3. **Few-shot Learning**
   - Fine-tuning rápido
   - Otimização de hiperparâmetros
   - Transfer learning

4. **Comparação de Abordagens**
   - TTM vs modelos tradicionais
   - Análise de trade-offs
   - Casos de uso recomendados

## 🎯 Como Usar Este Módulo

### 📋 Rota de Aprendizagem Sugerida

1. **📖 Estudar o Material Teórico**
   - Leia o PDF "Modelos Estatísticos e Autorregressivos"
   - Foque em entender os fundamentos matemáticos

2. **🛠️ Consultar o Guia Prático**
   - Revise o PDF "Preparação e Modelagem de Séries Temporais"
   - Use como referência durante a implementação

3. **💻 Executar os Notebooks**
   - Comece com `Aula_2_Séries_temporais_Fundamentos_de_IA.ipynb`
   - Depois explore `ttm_getting_started.ipynb`
   - Experimente com seus próprios dados

4. **🧪 Praticar com Dados Reais**
   - Aplique as técnicas em datasets diferentes
   - Compare abordagens estatísticas vs ML
   - Documente seus resultados

### 💡 Dicas de Estudo

- **Aprendizado Progressivo**: Comece com modelos simples antes de avançar para TTM
- **Visualização**: Sempre visualize seus dados e resultados
- **Validação Temporal**: Nunca use dados futuros para treinar modelos
- **Experimentação**: Teste diferentes configurações e parâmetros
- **Documentação**: Mantenha registro de experimentos e conclusões

### 🎓 Projetos Sugeridos

1. **Previsão de Vendas**: Use dados históricos de vendas
2. **Previsão de Demanda**: Preveja demanda de produtos
3. **Análise de Estoque**: Otimize níveis de estoque
4. **Previsão Financeira**: Analise séries financeiras
5. **Monitoramento**: Detecção de anomalias em tempo real

---

## 🚀 Próximos Passos

### Para Continuar Sua Jornada em Séries Temporais

1. **Deep Learning**: LSTM, GRU e Transformers para séries temporais
2. **Multivariate Forecasting**: Séries com múltiplas variáveis
3. **Streaming Anomaly Detection**: Detecção em tempo real
4. **Probabilistic Forecasting**: Previsões com intervalos de confiança
5. **MLOps for Time Series**: Operacionalização de modelos

### Módulos Relacionados

- **🤖 Inteligência Artificial**: Fundamentos de Machine Learning
- **🔢 Análise de Dados**: Técnicas de exploração e visualização
- **☁️ Cloud Computing**: Deploy de modelos escaláveis
- **📊 Estatística**: Fundamentos matemáticos avançados

---

---

## 📓 Material Complementar - UniFacens

### ⚠️ Aviso Importante sobre PDFs

Os materiais em formato PDF disponibilizados neste módulo são **propriedade intelectual da UniFacens** e foram compartilhados exclusivamente para facilitar o acesso dos alunos da **Capacitação Gêmeos Digitais**.

### 📋 Direitos de Uso

- ✅ **Permitido**: Acesso e uso pelos alunos matriculados na capacitação
- ✅ **Permitido**: Download para estudo pessoal
- ❌ **Proibido**: Reprodução e distribuição não autorizada
- ❌ **Proibido**: Uso comercial ou compartilhamento externo
- ❌ **Proibido**: Alteração ou modificação do conteúdo

### 🎓 Finalidade Educacional

Estes materiais foram compartilhados com propósito estritamente educacional para apoiar o aprendizado dos participantes do programa de capacitação. O uso indevido pode violar direitos autorais e as políticas institucionais da UniFacens.

---

## 📚 Recursos Adicionais

### Documentação Oficial
- [Statsmodels Documentation](https://www.statsmodels.org/)
- [TinyTimeMixer Documentation](https://github.com/ibm-granite/granite-tsfm)
- [Pandas Time Series](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html)
- [Scikit-learn Time Series](https://scikit-learn.org/stable/auto_examples/index.html#time-series)

### Datasets para Prática
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets.php)
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Time Series Data Library](https://datamarket.com/data/list/?q=provider:tsdl)


### Comunidade e Suporte
- Participe de competições de forecasting
- Contribua com projetos open source
- Compartilhe suas análises e descobertas

---

## 📊 Métricas e Avaliação

### Principais Métricas de Forecasting

- **MAE (Mean Absolute Error)**: Erro médio absoluto
- **RMSE (Root Mean Square Error)**: Raiz do erro quadrático médio
- **MAPE (Mean Absolute Percentage Error)**: Erro percentual médio absoluto
- **SMAPE (Symmetric MAPE)**: MAPE simétrico
- **MASE (Mean Absolute Scaled Error)**: Erro escalonado

### Técnicas de Validação

- **Time Series Split**: Divisão temporal
- **Walk-forward Validation**: Validação progressiva
- **Rolling Forecast Origin**: Origem móvel de previsão

---

*Este módulo foi criado para fins educacionais, demonstrando técnicas modernas de análise e previsão de séries temporais, desde modelos estatísticos clássicos até abordagens de deep learning.*
