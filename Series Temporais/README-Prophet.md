# Prophet - Guia de Instalação e Uso

![visitors](https://visitor-badge.laobi.icu/badge?page_id=ArvoreDosSaberes.Capacitacao_GemeosDigitais.SeriesTemporais.Prophet)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
![Prophet](https://img.shields.io/badge/Prophet-Meta%20%2F%20Facebook-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Time Series](https://img.shields.io/badge/Time%20Series-Forecasting-orange)
![Level](https://img.shields.io/badge/Level-Intermediate-yellow)

## 📋 Visão Geral

O Prophet é uma biblioteca open-source desenvolvida pela Meta (Facebook) para previsão de séries temporais. Baseado em um modelo aditivo decomponível (tendência + sazonalidade + feriados), é robusto a dados faltantes, mudanças de tendência e outliers. Este guia ajuda você a configurar e usar o Prophet no contexto do módulo de Séries Temporais.

## 🚀 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- Git
- Compiladores C/C++ (gcc, g++, build-essential) no Linux
- Ambiente virtual recomendado

### Passo 1: Configurar o Submódulo

O submódulo `prophet` já foi adicionado ao projeto. Para inicializá-lo:

```bash
# Se ainda não foi inicializado
git submodule update --init --recursive

# Para atualizar para a versão mais recente
git submodule update --remote prophet
```

### Passo 2: Instalar Dependências do Prophet

```bash
# Instalar o Prophet via PyPI (recomendado)
pip install prophet

# OU instalar a partir do submódulo local
cd prophet/python
pip install -e .
cd ../..

# Instalar dependências extras para notebooks e visualização
pip install -r requirement-prophet.txt
```

### Passo 3: Verificar Instalação

```python
# Testar se a instalação foi bem-sucedida
from prophet import Prophet
import pandas as pd

print("✅ Prophet instalado com sucesso!")
print(f"   Versão do Pandas: {pd.__version__}")
```

## 📁 Estrutura dos Arquivos

```text
SeriesTemporais/
├── README-Prophet.md                # Este arquivo
├── requirement-prophet.txt          # Dependências Prophet
├── prophet/                         # Submódulo Prophet
│   ├── python/                     # Código Python principal
│   ├── notebooks/                  # Tutoriais oficiais
│   │   ├── quick_start.ipynb
│   │   ├── diagnostics.ipynb
│   │   ├── trend_changepoints.ipynb
│   │   ├── seasonality,_holiday_effects,_and_regressors.ipynb
│   │   ├── multiplicative_seasonality.ipynb
│   │   ├── uncertainty_intervals.ipynb
│   │   ├── outliers.ipynb
│   │   ├── non-daily_data.ipynb
│   │   ├── additional_topics.ipynb
│   │   └── handling_shocks.ipynb
│   ├── examples/                   # Datasets de exemplo
│   │   ├── example_wp_log_peyton_manning.csv
│   │   ├── example_air_passengers.csv
│   │   ├── example_retail_sales.csv
│   │   └── ...
│   └── docs/                       # Documentação oficial
└── requirements.txt                # Dependências gerais do módulo
```

## 🎯 Como Usar o Prophet

### 1. Previsão Básica (Quick Start)

Previsão simples com dados históricos:

```python
from prophet import Prophet
import pandas as pd

# Carregar dados (formato obrigatório: colunas 'ds' e 'y')
df = pd.read_csv('prophet/examples/example_wp_log_peyton_manning.csv')
print(df.head())
#           ds      y
# 0  2007-12-10  9.5908
# 1  2007-12-11  8.5196
# 2  2007-12-12  8.1837
# ...

# Criar e treinar o modelo
model = Prophet()
model.fit(df)

# Criar dataframe com datas futuras (365 dias)
future = model.make_future_dataframe(periods=365)

# Fazer previsões
forecast = model.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# Visualizar resultados
fig1 = model.plot(forecast)
fig2 = model.plot_components(forecast)
```

### 2. Sazonalidade e Feriados

Adicionando efeitos de feriados e sazonalidade personalizada:

```python
from prophet import Prophet
import pandas as pd

# Definir feriados brasileiros manualmente
feriados_br = pd.DataFrame({
    'holiday': 'feriado_nacional',
    'ds': pd.to_datetime([
        '2023-01-01', '2023-04-21', '2023-05-01',
        '2023-09-07', '2023-10-12', '2023-11-02',
        '2023-11-15', '2023-12-25',
        '2024-01-01', '2024-04-21', '2024-05-01',
        '2024-09-07', '2024-10-12', '2024-11-02',
        '2024-11-15', '2024-12-25',
    ]),
    'lower_window': 0,
    'upper_window': 1,  # efeito no dia seguinte também
})

# OU usar feriados embutidos por país
model = Prophet(holidays=feriados_br)

# Também é possível usar o suporte nativo a países
model.add_country_holidays(country_name='BR')

model.fit(df)
forecast = model.predict(future)

# Visualizar componentes (tendência, sazonalidade, feriados)
fig = model.plot_components(forecast)
```

### 3. Tendência com Saturação (Logistic Growth)

Para séries com limites superiores e/ou inferiores:

```python
from prophet import Prophet
import pandas as pd

df = pd.read_csv('prophet/examples/example_wp_log_peyton_manning.csv')

# Definir capacidade máxima e piso
df['cap'] = 8.5    # limite superior (carrying capacity)
df['floor'] = 1.5  # limite inferior

# Usar crescimento logístico
model = Prophet(growth='logistic')
model.fit(df)

# Futuro também precisa de cap e floor
future = model.make_future_dataframe(periods=365)
future['cap'] = 8.5
future['floor'] = 1.5

forecast = model.predict(future)
fig = model.plot(forecast)
```

### 4. Changepoints (Pontos de Mudança de Tendência)

```python
from prophet import Prophet

# Ajustar sensibilidade a mudanças de tendência
model = Prophet(
    changepoint_prior_scale=0.05,  # default=0.05; maior = mais flexível
    n_changepoints=25,             # número de changepoints potenciais
)
model.fit(df)

forecast = model.predict(future)

# Visualizar os changepoints detectados
fig = model.plot(forecast)
from prophet.plot import add_changepoints_to_plot
a = add_changepoints_to_plot(fig.gca(), model, forecast)
```

### 5. Regressores Externos (Extra Regressors)

```python
from prophet import Prophet
import pandas as pd

# Adicionar variáveis externas que influenciam a série
model = Prophet()
model.add_regressor('temperatura')
model.add_regressor('promocao')

# Dados de treino devem conter as colunas extras
df['temperatura'] = [...]  # valores de temperatura
df['promocao'] = [...]     # 0 ou 1 indicando promoção

model.fit(df)

# Futuro também precisa das colunas extras preenchidas
future = model.make_future_dataframe(periods=30)
future['temperatura'] = [...]  # previsão de temperatura
future['promocao'] = [...]     # planejamento de promoções

forecast = model.predict(future)
```

### 6. Sazonalidade Multiplicativa

```python
from prophet import Prophet

# Para séries onde a amplitude da sazonalidade cresce com a tendência
model = Prophet(seasonality_mode='multiplicative')
model.fit(df)

forecast = model.predict(future)
fig = model.plot_components(forecast)
```

## 📚 Parâmetros Importantes

### Crescimento (Growth)

- **`linear`** (padrão): Tendência linear com changepoints
- **`logistic`**: Crescimento logístico com saturação (requer `cap` e opcionalmente `floor`)
- **`flat`**: Tendência constante (sem crescimento)

### Sazonalidade

- **`yearly_seasonality`**: Sazonalidade anual (auto-detectada)
- **`weekly_seasonality`**: Sazonalidade semanal (auto-detectada)
- **`daily_seasonality`**: Sazonalidade diária (auto-detectada para dados sub-diários)
- **`seasonality_mode`**: `'additive'` (padrão) ou `'multiplicative'`

### Ajuste Fino

- **`changepoint_prior_scale`**: Flexibilidade da tendência (default 0.05)
- **`seasonality_prior_scale`**: Força da sazonalidade (default 10)
- **`holidays_prior_scale`**: Força do efeito de feriados (default 10)
- **`interval_width`**: Largura do intervalo de incerteza (default 0.80)

## 💡 Dicas de Uso

### 1. Preparação de Dados

```python
import pandas as pd

# IMPORTANTE: Prophet exige colunas nomeadas 'ds' (data) e 'y' (valor)
data = pd.DataFrame({
    'ds': pd.date_range(start='2020-01-01', periods=1000, freq='D'),
    'y': [...]  # seus valores aqui
})

# Verificar e converter tipos
data['ds'] = pd.to_datetime(data['ds'])
data['y'] = data['y'].astype(float)
```

### 2. Validação Cruzada Temporal

```python
from prophet.diagnostics import cross_validation, performance_metrics

# Validação cruzada com Prophet
df_cv = cross_validation(
    model,
    initial='730 days',   # dados iniciais de treino
    period='180 days',    # espaçamento entre cutoffs
    horizon='365 days',   # horizonte de previsão
)

# Calcular métricas de performance
df_metrics = performance_metrics(df_cv)
print(df_metrics.head())
#   horizon       mse      rmse       mae      mape     mdape  smape  coverage
# ...

# Visualizar métricas
from prophet.plot import plot_cross_validation_metric
fig = plot_cross_validation_metric(df_cv, metric='mape')
```

### 3. Métricas de Avaliação

```python
from prophet.diagnostics import performance_metrics
import numpy as np

# Métricas automáticas do Prophet
metrics = performance_metrics(df_cv)

# Métricas disponíveis:
# - MSE  (Mean Squared Error)
# - RMSE (Root Mean Squared Error)
# - MAE  (Mean Absolute Error)
# - MAPE (Mean Absolute Percentage Error)
# - MDAPE (Median Absolute Percentage Error)
# - SMAPE (Symmetric Mean Absolute Percentage Error)
# - Coverage (cobertura do intervalo de confiança)

print(f"MAPE médio: {metrics['mape'].mean():.2%}")
print(f"RMSE médio: {metrics['rmse'].mean():.4f}")
```

### 4. Serialização do Modelo

```python
import json
from prophet.serialize import model_to_json, model_from_json

# Salvar modelo treinado
with open('prophet_model.json', 'w') as f:
    json.dump(model_to_json(model), f)

# Carregar modelo salvo
with open('prophet_model.json', 'r') as f:
    model_carregado = model_from_json(json.load(f))

# Usar modelo carregado para previsões
forecast = model_carregado.predict(future)
```

## 🔧 Troubleshooting

### Problemas Comuns

1. **Erro de instalação do cmdstanpy**
   ```bash
   # Instalar compiladores necessários (Linux/Ubuntu)
   sudo apt-get install build-essential

   # Se cmdstan não for encontrado, instalar manualmente
   python -c "import cmdstanpy; cmdstanpy.install_cmdstan()"
   ```

2. **Dados no formato incorreto**
   ```python
   # Prophet exige colunas 'ds' e 'y'
   # Renomear colunas se necessário
   df = df.rename(columns={'data': 'ds', 'valor': 'y'})

   # Verificar formato
   print(df.dtypes)
   print(df.head())

   # Converter timestamp se necessário
   df['ds'] = pd.to_datetime(df['ds'])
   ```

3. **Previsões ruins / overfitting**
   ```python
   # Reduzir flexibilidade da tendência
   model = Prophet(changepoint_prior_scale=0.01)

   # Ou aumentar regularização da sazonalidade
   model = Prophet(seasonality_prior_scale=0.1)
   ```

4. **Outliers afetando o modelo**
   ```python
   # Remover outliers definindo como NaN (Prophet ignora NaN em 'y')
   df.loc[df['y'] > limite_superior, 'y'] = None
   df.loc[df['y'] < limite_inferior, 'y'] = None
   ```

### Performance Tips

1. **Desabilitar sazonalidades desnecessárias**
   ```python
   # Acelerar treinamento removendo componentes não relevantes
   model = Prophet(
       weekly_seasonality=False,  # dados mensais não precisam disso
       daily_seasonality=False,
   )
   ```

2. **Paralelizar cross-validation**
   ```python
   # Instalar dependências de paralelização
   # pip install "prophet[parallel]"
   from prophet.diagnostics import cross_validation

   df_cv = cross_validation(
       model,
       initial='730 days',
       period='180 days',
       horizon='365 days',
       parallel='dask',  # ou 'processes'
   )
   ```

## 📖 Recursos Adicionais

### Documentação Oficial
- [Prophet Homepage](https://facebook.github.io/prophet/)
- [Quick Start Guide](https://facebook.github.io/prophet/docs/quick_start.html)
- [Prophet GitHub](https://github.com/facebook/prophet)
- [Prophet Paper](https://peerj.com/preprints/3190.pdf) - Sean J. Taylor, Benjamin Letham (2018)

### 📚 Bibliografia Recomendada

- **[Machine Learning for Time Series](../Livros e Apostilas/Machine Learning for Time Series - Ben Auffarth.pdf)** - Ben Auffarth
  - Fundamentos de ML aplicados a séries temporais
  - Cobre Prophet e outras técnicas de forecasting

- **[Practical Time Series Analysis](../Livros e Apostilas/Practical Time Series Analysis - Aileen Nielsen.pdf)** - Aileen Nielsen
  - Técnicas práticas com Python
  - Implementações que complementam o Prophet

- **[Análise de Séries Temporais](../Livros e Apostilas/Analise de Series Temporais - Pedro A. Morettin & Clelia M. C. Toloi.pdf)** - Pedro A. Morettin & Clelia M. C. Toloi
  - Fundamentos teóricos de séries temporais em português
  - Base estatística para compreender modelos aditivos

### Tutoriais e Exemplos
- `prophet/notebooks/` - Tutoriais oficiais do Prophet
  - `quick_start.ipynb` - Início rápido
  - `diagnostics.ipynb` - Validação cruzada e diagnósticos
  - `trend_changepoints.ipynb` - Pontos de mudança de tendência
  - `seasonality,_holiday_effects,_and_regressors.ipynb` - Sazonalidade e feriados
  - `handling_shocks.ipynb` - Lidando com choques (ex: COVID-19)
- `prophet/examples/` - Datasets de exemplo para prática
- [Prophet Quick Start - Documentação](https://facebook.github.io/prophet/docs/quick_start.html)

### Comunidade
- [Issues no GitHub](https://github.com/facebook/prophet/issues)
- [Blog Post: Prophet in 2023 and beyond](https://medium.com/@cuongduong_35162/facebook-prophet-in-2023-and-beyond-c5086151c138)

## 🚀 Próximos Passos

1. **Experimentar com seus dados**: Substitua os dados de exemplo pelos seus próprios
2. **Explorar sazonalidades**: Teste sazonalidade aditiva vs multiplicativa
3. **Adicionar feriados**: Configure feriados brasileiros para melhorar previsões
4. **Validação cruzada**: Use `cross_validation()` para avaliar a qualidade do modelo
5. **Comparar com outros modelos**: TTM, NeuralProphet, ARIMA, etc.
6. **Regressores externos**: Adicione variáveis exógenas para enriquecer o modelo

---

---

## 📓 Material Complementar - UniFacens

### ⚠️ Aviso Importante sobre PDFs

Os materiais em formato PDF disponibilizados no módulo de Séries Temporais são **propriedade intelectual da UniFacens** e foram compartilhados exclusivamente para facilitar o acesso dos alunos da **Capacitação Gêmeos Digitais**.

### 📋 Direitos de Uso

- ✅ **Permitido**: Acesso e uso pelos alunos matriculados na capacitação
- ✅ **Permitido**: Download para estudo pessoal
- ❌ **Proibido**: Reprodução e distribuição não autorizada
- ❌ **Proibido**: Uso comercial ou compartilhamento externo
- ❌ **Proibido**: Alteração ou modificação do conteúdo

### 🎓 Finalidade Educacional

Estes materiais foram compartilhados com propósito estritamente educacional para apoiar o aprendizado dos participantes do programa de capacitação. O uso indevido pode violar direitos autorais e as políticas institucionais da UniFacens.

---

## 📝 Resumo Rápido

```bash
# Setup completo em uma linha
git submodule update --init --recursive && \
pip install prophet && \
pip install -r requirement-prophet.txt
```

---

*Este guia foi criado para facilitar o uso do Prophet no contexto do módulo de Séries Temporais. Para informações mais detalhadas, consulte a [documentação oficial do projeto](https://facebook.github.io/prophet/).*
