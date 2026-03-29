# 📚 Glossário - Gêmeos Digitais e IA

![visitors](https://visitor-badge.laobi.icu/badge?page_id=ArvoreDosSaberes.Capacitacao_GemeosDigitais.Glossario)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
![Educational](https://img.shields.io/badge/Type-Educational-green)
![Glossary](https://img.shields.io/badge/Content-Glossary-blue)
![Status](https://img.shields.io/badge/Status-Comprehensive-brightgreen)

## 🎯 Objetivo do Glossário

Este glossário reúne os termos técnicos e conceitos mais comuns utilizados em cada módulo de estudo do curso de **Capacitação em Gêmeos Digitais e 5G**. Organizado por áreas de conhecimento, serve como referência rápida para consulta durante os estudos e prática com os notebooks e projetos.

---

## 🤖 Inteligência Artificial e Machine Learning

### Fundamentos de IA
- **Aprendizado Supervisionado**: Treinamento de modelos com dados rotulados (com gabarito), onde o algoritmo aprende padrões a partir de exemplos conhecidos.
- **Aprendizado Não-Supervisionado**: Processo onde o modelo identifica padrões em dados sem rótulos pré-definidos, incluindo clusterização e redução de dimensionalidade.
- **Aprendizado por Reforço**: Método onde um agente aprende através de tentativa e erro, recebendo recompensas por acertos e punições por erros.
- **LLMs (Large Language Models)**: Modelos de linguagem com grande capacidade computacional como ChatGPT, Gemini, Grok, treinados em vastos corpos de texto.

### Dados e Atributos
- **Dataset**: Conjunto de dados de entrada usado para treinar e testar modelos de IA.
- **Atributos**: Características ou variáveis dos dados (ex: gênero, idade, renda).
- **Representatividade**: Qualidade dos dados em refletir adequadamente a população ou fenômeno estudado.
- **Dados Enviesados**: Dados que contêm vieses sistemáticos que podem levar a modelos discriminatórios.

### Métricas e Avaliação
- **Overfitting**: Quando o modelo memoriza os dados de treino em vez de aprender o padrão geral, não generalizando para novos dados.
- **Underfitting**: Quando o modelo aprende de menos e não consegue capturar nem o padrão básico dos dados.
- **Acurácia**: Proporção geral de acertos do modelo em relação ao total de previsões.
- **Precisão**: Dos casos que o modelo previu como positivos, quantos realmente eram positivos.
- **Recall (Sensibilidade)**: Dos casos que realmente eram positivos, quantos o modelo acertou.
- **F1 Score**: Média harmônica entre Precisão e Recall, balanceando ambas as métricas.
- **MAE (Mean Absolute Error)**: Erro médio absoluto para modelos de regressão.
- **RMSE (Root Mean Square Error)**: Raiz do erro quadrático médio, penalizando erros maiores.
- **R² (R-quadrado)**: Coeficiente de determinação que varia de 0 a 1, indicando o ajuste do modelo aos dados.
- **Matriz de Confusão**: Tabela que compara predições com valores reais, contendo VP, VN, FP, FN.

### Algoritmos e Técnicas
- **Regressão Linear**: Modelo que encontra relação linear entre variáveis independentes e dependentes.
- **Regressão Logística**: Algoritmo de classificação binária que estima probabilidades.
- **Random Forest**: Ensemble de árvores de decisão para melhorar a precisão e reduzir overfitting.
- **Gradient Boosting**: Técnica ensemble que constrói modelos sequencialmente, corrigindo erros anteriores.
- **SVM (Support Vector Machine)**: Algoritmo que encontra o hiperplano ótimo para separar classes.
- **PCA (Principal Component Analysis)**: Técnica de redução de dimensionalidade que preserva a maior variância dos dados.
- **Clusterização**: Agrupamento de dados similares sem categorias pré-definidas.
- **Redes Neurais**: Modelos inspirados no cérebro humano, compostos por camadas de neurônios interconectados.
- **Lookahead**: Estratégia onde o modelo considera informações futuras para tomar decisões presentes, comum em sequências temporais e jogos.

### Ética e Interpretabilidade
- **Interpretabilidade**: Capacidade de entender e explicar as decisões de um modelo.
- **SHAP (SHapley Additive exPlanations)**: Método para explicar a contribuição de cada variável na previsão.
- **LIME (Local Interpretable Model-agnostic Explanations)**: Técnica para explicar predições individuais.
- **RLHF (Reinforcement Learning from Human Feedback)**: Técnica de treinamento que usa feedback humano para alinhar modelos.
- **Correlação vs Causalidade**: Diferença fundamental entre relação estatística e relação de causa e efeito.

---

## 📈 Séries Temporais

### Conceitos Fundamentais
- **Série Temporal**: Sequência de dados coletados ao longo do tempo, onde a ordem temporal é relevante.
- **Tendência**: Movimento geral de longo prazo dos dados (crescente, decrescente ou estacionário).
- **Sazonalidade**: Padrões que se repetem em períodos fixos (diários, mensais, anuais).
- **Ciclo**: Padrões que se repetem em períodos não fixos, geralmente associados a ciclos econômicos.
- **Resíduos**: Componente restante após remover tendência e sazonalidade, representando ruído aleatório.
- **Estacionariedade**: Propriedade de uma série cujas estatísticas (média, variância) não mudam ao longo do tempo.
- **Cutoff**: Ponto de divisão temporal que separa dados de treino e teste, definindo o limite temporal para análise.

### Modelos Estatísticos
- **ARIMA (AutoRegressive Integrated Moving Average)**: Modelo clássico que combina componentes autorregressivos e de média móvel.
- **SARIMA (Seasonal ARIMA)**: Extensão do ARIMA que incorpora componente sazonal.
- **Prophet**: Biblioteca Facebook para previsão de séries temporais com componentes de tendência e sazonalidade.
- **VAR (Vector Autoregression)**: Modelo multivariado que captura relações entre múltiplas séries.
- **State-Space Models**: Framework geral para modelar séries temporais com estados latentes.

### Modelos de Machine Learning
- **LSTM (Long Short-Term Memory)**: Tipo de rede neural recorrente capaz de aprender dependências de longo prazo.
- **GRU (Gated Recurrent Unit)**: Variante simplificada do LSTM com menos parâmetros.
- **Transformers**: Arquitetura baseada em mecanismo de atenção, revolucionou processamento de sequências.
- **TinyTimeMixer (TTM)**: Modelo pré-treinado da IBM para previsão de séries temporais.
- **Zero-shot Forecasting**: Previsão sem treinamento específico no dataset de destino.
- **Few-shot Learning**: Aprendizado com poucos exemplos de treinamento.

### Processamento e Preparação
- **Downsampling**: Redução da frequência dos dados através de agregação (ex: dados horários para diários).
- **Dropping**: Remoção de pontos de dados ou períodos específicos da série temporal.
- **Meaningful**: Característica de dados que contêm informação relevante e não apenas ruído para análise.

### Métricas e Validação
- **Forecast Horizon**: Período futuro para o qual se deseja fazer previsões.
- **Context Length**: Número de pontos históricos usados para fazer cada previsão.
- **Backtesting**: Validação do modelo usando dados históricos em ordem cronológica.
- **Cross-validation temporal**: Técnica de validação que respeita a ordem temporal dos dados.
- **Drift Detection**: Identificação de mudanças na distribuição dos dados ao longo do tempo.
- **Lookahead**: Técnica que incorpora informações futuras no processo de decisão presente, usada para melhorar precisão em previsões e planejamento.
- **Downstream**: Processos ou etapas que ocorrem após a análise inicial da série temporal, como aplicação de modelos ou tomada de decisão.

---

## 🔤 Large Language Models (LLMs)

### Arquiteturas e Componentes
- **Transformers**: Arquitetura de redes neurais baseada em mecanismo de atenção, base da maioria dos LLMs modernos.
- **BERT (Bidirectional Encoder Representations from Transformers)**: Modelo Google que entende contexto bidirecionalmente.
- **GPT (Generative Pre-trained Transformer)**: Família de modelos generativos da OpenAI.
- **IBM Granite**: Família de modelos da IBM otimizados para aplicações empresariais.
- **Encoder-Decoder**: Arquitetura com componente codificador e decodificador para tarefas sequência-para-sequência.

### Mecanismos Internos
- **Tokenização**: Processo de dividir texto em unidades menores (tokens) para processamento.
- **Embeddings**: Representações vetoriais densas que capturam significado semântico.
- **Mecanismo de Atenção**: Sistema que permite ao modelo focar em partes relevantes da entrada.
- **Query, Key, Value**: Componentes do mecanismo de atenção que calculam relevância contextual.
- **Positional Encoding**: Informação sobre a posição dos tokens na sequência.
- **Multi-head Attention**: Múltiplos mecanismos de atenção operando em paralelo.

### Treinamento e Adaptação
- **Pre-training**: Fase inicial de treinamento em grandes corpos de texto não supervisionado.
- **Fine-tuning**: Adaptação de modelo pré-treinado para tarefas específicas.
- **Instruction-tuning**: Treinamento para seguir instruções e comandos.
- **Transfer Learning**: Uso de conhecimento de uma tarefa para ajudar em outra.
- **Temperature**: Parâmetro que controla a aleatoriedade na geração de texto.
- **Top-k Sampling**: Estratégia de geração que considera os k tokens mais prováveis.
- **Top-p (Nucleus) Sampling**: Estratégia que considera tokens até atingir probabilidade acumulada p.

### Aplicações e Técnicas
- **Zero-shot Learning**: Capacidade de realizar tarefas sem exemplos específicos de treinamento.
- **Few-shot Learning**: Aprendizado com poucos exemplos no contexto.
- **Chain-of-Thought**: Técnica que faz o modelo "pensar passo a passo".
- **Prompt Engineering**: Arte de projetar instruções eficazes para LLMs.
- **Hallucination**: Geração de informações falsas ou incorretas pelo modelo.
- **Context Window**: Limite de tokens que o modelo pode processar simultaneamente.

---

## 🏭 Gêmeos Digitais e IoT

### Conceitos Fundamentais
- **Gêmeo Digital**: Réplica virtual de um ativo, processo ou sistema do mundo real, atualizada em tempo real.
- **Digital Twin**: Termo em inglês para Gêmeo Digital.
- **Sistema Ciberfísico**: Integração de componentes computacionais com processos físicos.
- **IoT (Internet of Things)**: Rede de dispositivos conectados que coletam e transmitem dados.
- **IIoT (Industrial IoT)**: Aplicação de IoT em ambientes industriais.
- **Sensoriamento**: Coleta de dados através de sensores físicos.

### Componentes e Arquiteturas
- **Ativo Digital**: Representação digital de um equipamento ou sistema físico.
- **Modelo de Simulação**: Modelo matemático que replica comportamento do sistema real.
- **Data Pipeline**: Fluxo de dados desde a coleta até o processamento e análise.
- **Edge Computing**: Processamento de dados próximo à fonte de geração.
- **Cloud Computing**: Processamento de dados em servidores remotos na nuvem.
- **Fog Computing**: Camada intermediária entre edge e cloud computing.

### Aplicações Industriais
- **Manutenção Preditiva**: Previsão de falhas antes que ocorram, baseada em dados de sensores.
- **Monitoramento em Tempo Real**: Acompanhamento contínuo do estado de sistemas e equipamentos.
- **Otimização de Processos**: Melhoria de eficiência através de análise de dados operacionais.
- **Simulação de Cenários**: Teste de diferentes condições e estratégias em ambiente virtual.
- **Digital Thread**: Conexão digital que acompanha o ciclo de vida completo de um produto.

---

## 📊 Análise de Dados e Visualização

### Ferramentas e Bibliotecas
- **pandas**: Biblioteca Python para manipulação e análise de dados tabulares.
- **NumPy**: Biblioteca para computação numérica em Python.
- **Matplotlib**: Biblioteca fundamental para visualização de dados em Python.
- **Seaborn**: Biblioteca baseada em Matplotlib para visualizações estatísticas.
- **Plotly**: Biblioteca para visualizações interativas.
- **scikit-learn**: Biblioteca principal para Machine Learning em Python.

### Estruturas de Dados
- **DataFrame**: Estrutura bidimensional de dados, similar a uma tabela.
- **Series**: Estrutura unidimensional de dados, similar a uma coluna.
- **Array**: Estrutura multidimensional para dados numéricos.
- **Tensor**: Estrutura multidimensional usada em deep learning.

### Técnicas de Análise
- **Análise Exploratória de Dados (EDA)**: Investigação inicial dos dados para entender padrões.
- **Data Cleaning**: Processo de identificação e correção de erros nos dados.
- **Feature Engineering**: Criação de novas variáveis a partir das existentes.
- **Normalization**: Escalonamento de dados para um intervalo padrão.
- **Standardization**: Transformação para média zero e desvio padrão unitário.

---

## 🔧 Engenharia e Operações (MLOps)

### Pipeline e Deploy
- **MLOps**: Práticas de DevOps aplicadas a Machine Learning.
- **Pipeline de ML**: Sequência automatizada de etapas de processamento de dados.
- **ETL (Extract, Transform, Load)**: Processo de extração, transformação e carga de dados.
- **Model Deployment**: Processo de colocar modelos em produção.
- **API (Application Programming Interface)**: Interface para comunicação entre sistemas.
- **Containerização**: Empacotamento de aplicações em contêineres isolados.

### Monitoramento e Manutenção
- **Model Monitoring**: Acompanhamento contínuo da performance do modelo em produção.
- **Drift Detection**: Identificação de mudanças nos padrões dos dados.
- **Performance Tracking**: Medição contínua de métricas do modelo.
- **Retraining**: Retreinamento periódico do modelo com novos dados.
- **A/B Testing**: Comparação experimental entre diferentes versões de modelos.

### Infraestrutura
- **GPU (Graphics Processing Unit)**: Hardware acelerador para processamento paralelo.
- **TPU (Tensor Processing Unit)**: Hardware especializado para operações de tensor.
- **Docker**: Plataforma para containerização de aplicações.
- **Kubernetes**: Sistema de orquestração de contêineres.
- **MLflow**: Plataforma open source para gerenciamento do ciclo de vida de ML.

---

## 📐 Fundamentos Matemáticos

### Álgebra Linear
- **Vetor**: Array unidimensional de números.
- **Matriz**: Array bidimensional de números.
- **Tensor**: Generalização de matrizes para múltiplas dimensões.
- **Autovalor e Autovetor**: Valores especiais que caracterizam transformações lineares.
- **Produto Escalar**: Operação que retorna um número a partir de dois vetores.
- **Transposição de Matriz**: Operação que inverte linhas e colunas de uma matriz.

### Estatística e Probabilidade
- **Distribuição de Probabilidade**: Função que descreve a probabilidade de diferentes valores.
- **Média Aritmética**: Soma dos valores dividida pelo número de observações.
- **Mediana**: Valor central quando os dados estão ordenados.
- **Desvio Padrão**: Medida de dispersão dos dados em relação à média.
- **Variância**: Quadrado do desvio padrão.
- **Correlação**: Medida de relação linear entre duas variáveis.
- **Inferência Estatística**: Processo de tirar conclusões sobre populações a partir de amostras.

### Cálculo e Otimização
- **Derivada**: Taxa de variação instantânea.
- **Gradiente**: Vetor de derivadas parciais.
- **Gradient Descent**: Algoritmo de otimização que usa gradientes para encontrar mínimos.
- **Função de Custo**: Função que mede o erro do modelo.
- **Backpropagation**: Algoritmo para treinar redes neurais usando gradientes.
- **Learning Rate**: Taxa de aprendizado que controla o tamanho dos passos de otimização.

---

## 🌐 Redes e Comunicação

### 5G e Conectividade
- **5G**: Quinta geração de tecnologia de comunicação móvel.
- **Latência**: Tempo de atraso na transmissão de dados.
- **Bandwidth**: Capacidade de transmissão de dados.
- **Edge Computing**: Processamento próximo à fonte de dados.
- **Network Slicing**: Divisão virtual de redes para diferentes aplicações.
- **Massive IoT**: Conexão de um grande número de dispositivos IoT.

### Protocolos e Padrões
- **HTTP/HTTPS**: Protocolos para comunicação web.
- **MQTT**: Protocolo leve para comunicação IoT.
- **REST API**: Estilo arquitetural para APIs web.
- **WebSocket**: Protocolo para comunicação bidirecional em tempo real.
- **JSON**: Formato leve de intercâmbio de dados.

---

## 📚 Referências Cruzadas

### Conceitos Relacionados
- **Deep Learning**: Subcampo de ML baseado em redes neurais profundas.
- **Neural Networks**: Modelos inspirados no funcionamento do cérebro.
- **Computer Vision**: Campo que trata do processamento de imagens por computador.
- **NLP (Natural Language Processing)**: Processamento de linguagem natural.
- **Reinforcement Learning**: Aprendizado por reforço (ver Aprendizado por Reforço).
- **Ensemble Methods**: Técnicas que combinam múltiplos modelos.

### Acrônimos Comuns
- **AI**: Artificial Intelligence (Inteligência Artificial)
- **ML**: Machine Learning (Aprendizado de Máquina)
- **DL**: Deep Learning (Aprendizado Profundo)
- **IoT**: Internet of Things (Internet das Coisas)
- **IIoT**: Industrial Internet of Things (Internet Industrial das Coisas)
- **API**: Application Programming Interface (Interface de Programação de Aplicações)
- **GPU**: Graphics Processing Unit (Unidade de Processamento Gráfico)
- **CPU**: Central Processing Unit (Unidade Central de Processamento)
- **RAM**: Random Access Memory (Memória de Acesso Aleatório)
- **GUI**: Graphical User Interface (Interface Gráfica do Usuário)

---

## 💡 Dicas de Uso

### Como Consultar
1. **Por Módulo**: Navegue pela seção correspondente ao módulo que está estudando.
2. **Por Termo**: Use a função de busca do seu editor para encontrar termos específicos.
3. **Por Contexto**: Consulte as referências cruzadas para entender conceitos relacionados.

### Estudo Eficiente
- **Termos em Negrito**: Conceitos mais importantes e frequentemente usados.
- **Exemplos Práticos**: Muitos termos incluem exemplos de aplicação real.
- **Conexões entre Módulos**: Note como conceitos de um módulo se aplicam a outros.

---

## 🔄 Atualizações e Expansão

Este glossário é um documento vivo que será atualizado conforme novos módulos e conceitos forem adicionados ao curso. Contribuições e sugestões são bem-vindas para enriquecer este recurso de referência.

### Próximas Adições Planejadas
- [ ] Termos de Computer Vision
- [ ] Conceitos de Edge AI
- [ ] Terminologia de Blockchain e Web3
- [ ] Vocabulário de Quantum Computing

---

*Última atualização: Março 2026*  
*Versão: 1.0 - Glossário Completo dos Módulos Atuais*