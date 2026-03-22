# Engines Avançadas de Séries Temporais

Lista de engines e bibliotecas avançadas para previsão e análise de séries temporais.

---

## 1. IBM Granite Time Series (granite-tsfm)

- **Site:** <https://research.ibm.com/blog/granite-code-models-702>
- **GitHub:** <https://github.com/ibm-granite/granite-tsfm>
- **Descrição:** Família de modelos foundation pré-treinados da IBM para séries temporais, baseados na arquitetura Transformer (Tiny Time Mixer – TTM). Suporta previsão (forecasting), detecção de anomalias e classificação de séries temporais com fine-tuning eficiente em poucos dados. Parte do ecossistema Granite da IBM, com integração ao Hugging Face.

---

## 2. Prophet (Meta / Facebook)

- **Site:** <https://facebook.github.io/prophet/>
- **GitHub:** <https://github.com/facebook/prophet>
- **Descrição:** Biblioteca open-source desenvolvida pela Meta para previsão de séries temporais com sazonalidade forte e múltiplos efeitos de feriados. Baseada em modelo aditivo decomponível (tendência + sazonalidade + feriados), é fácil de usar e robusta a dados faltantes e mudanças de tendência. Disponível em Python e R.

---

## 3. NeuralProphet

- **Site:** <https://neuralprophet.com/>
- **GitHub:** <https://github.com/ourownstory/neural_prophet>
- **Descrição:** Evolução do Prophet que combina modelos clássicos de decomposição com redes neurais (PyTorch). Suporta auto-regressão, covariáveis externas (lagged regressors), sazonalidade aprendida e efeitos de eventos. Mantém a interface simples do Prophet com maior flexibilidade e precisão.

---

## 4. Nixtla (TimeGPT / StatsForecast / NeuralForecast)

- **Site:** <https://nixtla.io/>
- **GitHub (StatsForecast):** <https://github.com/Nixtla/statsforecast>
- **GitHub (NeuralForecast):** <https://github.com/Nixtla/neuralforecast>
- **GitHub (TimeGPT):** <https://github.com/Nixtla/nixtla>
- **Descrição:** Ecossistema completo de previsão de séries temporais. **StatsForecast** oferece modelos estatísticos clássicos otimizados (ARIMA, ETS, Theta). **NeuralForecast** fornece modelos de deep learning (N-BEATS, N-HiTS, PatchTST, TimesNet). **TimeGPT** é um modelo foundation pré-treinado acessível via API, capaz de previsão zero-shot.

---

## 5. Darts (Unit8)

- **Site:** <https://unit8co.github.io/darts/>
- **GitHub:** <https://github.com/unit8co/darts>
- **Descrição:** Biblioteca Python que unifica modelos clássicos (ARIMA, Exponential Smoothing) e de deep learning (Transformer, TCN, N-BEATS) em uma API consistente. Suporta séries multivariadas, covariáveis, backtesting, ensembles e pipelines de previsão probabilística.

---

## 6. GluonTS (Amazon)

- **Site:** <https://ts.gluon.ai/>
- **GitHub:** <https://github.com/awslabs/gluonts>
- **Descrição:** Toolkit da Amazon para modelagem probabilística de séries temporais usando deep learning. Inclui modelos como DeepAR, Temporal Fusion Transformer (TFT) e WaveNet. Foco em previsão probabilística com quantis e distribuições, com integração ao PyTorch e MXNet.

---

## 7. TSAI (Time Series AI)

- **Site:** <https://timeseriesai.github.io/tsai/>
- **GitHub:** <https://github.com/timeseriesAI/tsai>
- **Descrição:** Biblioteca baseada em fastai e PyTorch para classificação, regressão e previsão de séries temporais. Inclui implementações de InceptionTime, ROCKET, TST (Time Series Transformer), MiniRocket e outros modelos state-of-the-art. Boa documentação com tutoriais e exemplos.

---

## 8. Kats (Meta / Facebook)

- **Site:** <https://facebookresearch.github.io/Kats/>
- **GitHub:** <https://github.com/facebookresearch/Kats>
- **Descrição:** Kit de análise de séries temporais da Meta que oferece detecção de pontos de mudança, detecção de anomalias, previsão e extração de features. Integra múltiplos modelos (Prophet, ARIMA, Holt-Winters, SARIMA) em uma API unificada com ferramentas de avaliação.

---

## 9. Chronos (Amazon)

- **Site:** <https://auto.gluon.ai/stable/tutorials/timeseries/forecasting-chronos.html>
- **GitHub:** <https://github.com/amazon-science/chronos-forecasting>
- **Descrição:** Modelos foundation pré-treinados da Amazon para previsão de séries temporais, baseados em arquitetura de language model (T5). Tokeniza valores numéricos e trata a previsão como um problema de geração de sequência. Suporta previsão zero-shot e fine-tuning, com modelos de diferentes tamanhos disponíveis no Hugging Face.

---

## 10. Merlion (Salesforce)

- **Site:** <https://opensource.salesforce.com/Merlion/>
- **GitHub:** <https://github.com/salesforce/Merlion>
- **Descrição:** Framework da Salesforce para inteligência de séries temporais com foco em previsão e detecção de anomalias. Oferece interface unificada para múltiplos modelos, seleção automática de modelo (AutoML), pós-processamento de anomalias e pipelines de avaliação padronizados.

---

## Comparativo Rápido

| Engine         | Tipo              | Previsão | Anomalia | Zero-shot | Linguagem    |
|----------------|-------------------|:--------:|:--------:|:---------:|:------------:|
| Granite (TTM)  | Foundation Model  | ✅       | ✅       | ✅        | Python       |
| Prophet        | Estatístico       | ✅       | ❌       | ❌        | Python / R   |
| NeuralProphet  | Híbrido (NN)      | ✅       | ❌       | ❌        | Python       |
| Nixtla         | Ecossistema       | ✅       | ✅       | ✅        | Python       |
| Darts          | Unificado         | ✅       | ✅       | ❌        | Python       |
| GluonTS        | Deep Learning     | ✅       | ❌       | ❌        | Python       |
| TSAI           | Deep Learning     | ✅       | ❌       | ❌        | Python       |
| Kats           | Toolkit           | ✅       | ✅       | ❌        | Python       |
| Chronos        | Foundation Model  | ✅       | ❌       | ✅        | Python       |
| Merlion        | Framework         | ✅       | ✅       | ❌        | Python       |
