# TinyTimeMixer (TTM) - Guia de Instalação e Uso

![TinyTimeMixer](https://img.shields.io/badge/TTM-IBM%20Granite-purple)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red)

## 📋 Visão Geral

O TinyTimeMixer (TTM) é uma família de modelos de séries temporais pré-treinados desenvolvidos pela IBM Research. Este guia ajuda você a configurar e usar o TTM no contexto do módulo de Séries Temporais.

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Git
- Ambiente virtual recomendado

### Passo 1: Configurar o Submódulo

O submódulo `granite-tsfm` já foi adicionado ao projeto. Para inicializá-lo:

```bash
# Se ainda não foi inicializado
git submodule update --init --recursive

# Para atualizar para a versão mais recente
git submodule update --remote granite-tsfm
```

### Passo 2: Instalar Dependências do TTM

```bash
# Instalar dependências básicas
pip install -r requirement-ttm.txt

# Navegar para o diretório do TTM
cd granite-tsfm

# Instalar o pacote TTM com suporte a notebooks
pip install ".[notebooks]"

# Instalar demos e exemplos adicionais
pip install ".[demos]"

# Voltar ao diretório principal
cd ..
```

### Passo 3: Verificar Instalação

```python
# Testar se a instalação foi bem-sucedida
from tsfm_public.toolkit.time_series_forecasting import TimeSeriesForecastingPipeline
from tsfm_public.toolkit.get_model import get_model

print("✅ TinyTimeMixer instalado com sucesso!")
```

## 📁 Estrutura dos Arquivos

```
SeriesTemporais/
├── README-TTM.md                    # Este arquivo
├── requirement-ttm.txt              # Dependências TTM
├── granite-tsfm/                    # Submódulo TTM
│   ├── tsfm_public/                # Código principal
│   ├── notebooks/                  # Exemplos e tutoriais
│   ├── demos/                      # Demonstrações
│   └── examples/                   # Casos de uso
├── ttm_getting_started.ipynb        # Notebook principal do curso
└── requirements.txt                # Dependências gerais do módulo
```

## 🎯 Como Usar o TTM

### 1. Zero-Shot Forecasting

Previsão sem treinamento específico no seu dataset:

```python
from tsfm_public.toolkit.get_model import get_model
from tsfm_public.toolkit.time_series_forecasting import TimeSeriesForecastingPipeline

# Obter modelo pré-treinado
model = get_model(
    context_length=512,
    prediction_length=96,
    model_family="ttm",
)

# Criar pipeline de forecasting
pipeline = TimeSeriesForecastingPipeline(
    model=model,
    timestamp_column="timestamp",
    target_columns=["value"],
)

# Fazer previsões (zero-shot)
forecast = pipeline.forecast(
    data=train_data,
    prediction_length=96,
)
```

### 2. Few-Shot Learning

Fine-tuning rápido com poucos dados:

```python
# Fine-tuning com 5% dos dados
pipeline.fit(
    train_data=train_data,
    fine_tuning_mode="few-shot",
    fine_tuning_fraction=0.05,
)

# Fazer previsões após fine-tuning
forecast = pipeline.forecast(
    data=train_data,
    prediction_length=96,
)
```

### 3. Configurações Avançadas

```python
# Configurar modelo específico
model = get_model(
    context_length=1024,  # Mais contexto
    prediction_length=168, # Mais previsões
    model_family="ttm-r2", # Versão mais recente
    freq="h",             # Frequência horária
)

# Pipeline com configurações personalizadas
pipeline = TimeSeriesForecastingPipeline(
    model=model,
    timestamp_column="timestamp",
    target_columns=["value"],
    id_columns=["series_id"], # Para múltiplas séries
    prediction_length=96,
)
```

## 📚 Modelos Disponíveis

### TTM-R1 (Versão 1)
- **TTM-512-96**: Contexto 512, previsão 96
- **TTM-1024-96**: Contexto 1024, previsão 96
- **TTM-512-168**: Contexto 512, previsão 168

### TTM-R2 (Versão 2 - Recomendado)
- **Melhor performance**: Mais preciso e eficiente
- **Mais context lengths**: Opções 512, 1024, 2048
- **Melhor generalização**: Funciona bem em diversos domínios

### Modelos de Pesquisa
- **ttm-research-r2**: Para uso acadêmico
- **Licença não-comercial**: Apenas para pesquisa

## 💡 Dicas de Uso

### 1. Preparação de Dados

```python
# Formato esperado pelo TTM
import pandas as pd

# Dados devem ter colunas: timestamp, target
data = pd.DataFrame({
    "timestamp": pd.date_range(start="2020-01-01", periods=1000, freq="H"),
    "value": np.random.randn(1000).cumsum(),
    "series_id": ["series_1"] * 1000,  # Opcional, para múltiplas séries
})
```

### 2. Validação de Modelos

```python
# Usar validação temporal
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, val_idx in tscv.split(data):
    train_data = data.iloc[train_idx]
    val_data = data.iloc[val_idx]
    
    # Treinar e avaliar
    pipeline.fit(train_data)
    forecast = pipeline.forecast(val_data, prediction_length=96)
    # Calcular métricas...
```

### 3. Métricas de Avaliação

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Métricas comuns para séries temporais
mae = mean_absolute_error(actual, predicted)
rmse = np.sqrt(mean_squared_error(actual, predicted))
mape = np.mean(np.abs((actual - predicted) / actual)) * 100
```

## 🔧 Troubleshooting

### Problemas Comuns

1. **CUDA out of memory**
   ```python
   # Reduzir batch size ou usar CPU
   pipeline = TimeSeriesForecastingPipeline(
       model=model,
       device="cpu",  # Forçar uso de CPU
   )
   ```

2. **Dados no formato incorreto**
   ```python
   # Verificar formato dos dados
   print(data.head())
   print(data.dtypes)
   
   # Converter timestamp se necessário
   data["timestamp"] = pd.to_datetime(data["timestamp"])
   ```

3. **Modelo não encontrado**
   ```python
   # Verificar modelos disponíveis
   from tsfm_public.toolkit.get_model import list_available_models
   print(list_available_models())
   ```

### Performance Tips

1. **Usar GPU se disponível**
   ```python
   import torch
   device = "cuda" if torch.cuda.is_available() else "cpu"
   pipeline = TimeSeriesForecastingPipeline(model=model, device=device)
   ```

2. **Batch processing para grandes datasets**
   ```python
   # Processar em batches
   forecasts = []
   for batch in np.array_split(large_data, 10):
       forecast = pipeline.forecast(batch, prediction_length=96)
       forecasts.append(forecast)
   ```

## 📖 Recursos Adicionais

### Documentação Oficial
- [TTM Repository](https://github.com/ibm-granite/granite-tsfm)
- [IBM Granite Docs - Fine-tune Time Series](https://www.ibm.com/granite/docs/fine-tune/time-series)
- [TTM Paper](https://arxiv.org/abs/2401.03955)
- [Hugging Face Models](https://huggingface.co/ibm-granite)

### Tutoriais e Exemplos
- `granite-tsfm/notebooks/` - Tutoriais oficiais
- `granite-tsfm/demos/` - Demonstrações práticas
- [TTM Getting Started - Google Colab](https://colab.research.google.com/github/ibm-granite/granite-tsfm/blob/main/notebooks/hfdemo/ttm_getting_started.ipynb)
- `ttm_getting_started.ipynb` - Nosso notebook do curso

### Comunidade
- [Issues no GitHub](https://github.com/ibm-granite/granite-tsfm/issues)
- [Discussions](https://github.com/ibm-granite/granite-tsfm/discussions)

## 🚀 Próximos Passos

1. **Experimentar com seus dados**: Substitua os dados de exemplo pelos seus próprios
2. **Comparar com modelos tradicionais**: ARIMA, Prophet, etc.
3. **Explorar configurações**: Diferentes context lengths e prediction lengths
4. **Fine-tuning avançado**: Experimente com diferentes frações de fine-tuning
5. **Deploy**: Coloque o modelo em produção para previsões em tempo real

---

## 📝 Resumo Rápido

```bash
# Setup completo em uma linha
git submodule update --init --recursive && \
cd granite-tsfm && \
pip install ".[notebooks]" && \
pip install ".[demos]" && \
cd .. && \
pip install -r requirement-ttm.txt
```

---

*Este guia foi criado para facilitar o uso do TinyTimeMixer no contexto do módulo de Séries Temporais. Para informações mais detalhadas, consulte a documentação oficial do projeto.*
