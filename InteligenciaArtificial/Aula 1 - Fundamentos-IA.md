# Aula 1 — Fundamentos da Inteligência Artificial

**Resumo didático** da transcrição da aula ministrada no curso de Residência Tecnológica em Gêmeo Digital e 5G.

---

## 1. Contexto e Motivação

A aula apresenta os fundamentos conceituais de Inteligência Artificial e Machine Learning, partindo de exemplos práticos e acessíveis para construir uma base teórica sólida antes de entrar na parte prática (notebook Colab).

---

## 2. Dados e Atributos — O Combustível da IA

- Todo modelo de IA depende de **dados de entrada** (datasets).
- Atributos como **gênero, idade, renda e custos fixos de vida** influenciam diretamente modelos de risco de crédito.
- A **diversidade e representatividade** da amostra são essenciais: se um banco é feito para brasileiros, os dados devem refletir a população brasileira.

*O professor enfatiza que não adianta ter um modelo sofisticado se os dados são pobres, enviesados ou insuficientes. "Lixo entra, lixo sai" é o princípio implícito.*

### 2.1 Qualidade dos Dados

- A qualidade dos dados impacta diretamente a performance do modelo.
- Exemplo humorístico: reconhecer Barack Obama a partir de uma foto borrada — **dados ruins geram previsões ruins**.
- Analogia da criança: se você mostra foto de boi e diz que é ovelha, a criança (e a máquina) vai aprender errado.

*A mensagem central: entender o fenômeno antes de jogar dados no modelo. A preparação dos dados é a etapa mais trabalhosa e mais importante de qualquer pipeline de data science.*

---

## 3. Tipos de Aprendizado de Máquina

### 3.1 Aprendizado Supervisionado

- É como **estudar com gabarito**: o modelo recebe exemplos com respostas conhecidas (rótulos).
- Dois tipos principais de problemas:
  - **Classificação**: categorizar (ex.: spam/não spam, risco alto/baixo).
  - **Regressão**: prever valores contínuos (ex.: preço de imóvel com base em área, bairro, amenidades).
- Modelo linear simples: **y = ax + b** — o modelo ajusta os parâmetros *a* e *b* com base nos dados conhecidos.
- **Séries temporais**: usar dados históricos para projetar tendências futuras, reconhecendo que a margem de erro cresce com o horizonte de previsão.

*O supervisionado é o tipo mais utilizado na prática e o ponto de partida para quem está aprendendo ML.*

### 3.2 Aprendizado Não-Supervisionado

- O modelo recebe dados **sem rótulos** e precisa encontrar padrões por conta própria.
- Aplicações:
  - **Redução de dimensionalidade** (ex.: PCA — Principal Component Analysis).
  - **Detecção de anomalias**: identificar pontos que desviam do padrão "normal" dos dados.
  - **Clusterização (agrupamento)**: agrupar dados semelhantes sem categorias pré-definidas.

#### Exemplo real — Reabilitação de áreas de mineração na Amazônia

- Utilizou-se **clusterização hierárquica** com **distância Euclidiana** sobre **14 variáveis** para classificar áreas mineradas reabilitadas.
- Objetivo: verificar se as áreas se assemelhavam à vegetação natural (floresta).
- Resultado: algumas áreas ainda eram distintas da floresta, auxiliando o IBAMA a definir expectativas realistas para as mineradoras.

*Este exemplo mostra como a IA pode ter impacto ambiental positivo e como o não-supervisionado é valioso quando não temos categorias pré-definidas.*

### 3.3 Aprendizado por Reforço

- O agente aprende por **tentativa e erro**, recebendo **recompensas** (acertos) e **punições** (erros).
- Exemplo do **Mario Kart**: o carrinho bate (função de custo/punição); quando acerta o caminho, recebe recompensa. Os algoritmos com melhor performance se propagam.
- Analogia militar: o exército usa recompensa e punição para treinar soldados — "aprendizado por reforço há muito tempo".
- **Paralelo com o ciclo PDCA** (Plan-Do-Check-Act): planejar, executar, checar, agir/ajustar — pipeline semelhante ao de um modelo que ajusta pesos iterativamente.
- O **ChatGPT** foi treinado com aprendizado por reforço com feedback humano (RLHF), incluindo interações com humanos para corrigir "alucinações".

*O professor destaca que o aprendizado por reforço foi fundamental para as tecnologias que temos hoje, incluindo os grandes modelos de linguagem.*

---

## 4. Treino e Teste — Evitando o "Decoreba"

- **Nunca usar 100% dos dados para treinar**. Sempre reservar uma parcela para teste (ex.: 80% treino / 20% teste).
- Analogia: decorar exercícios de matemática vs. entender o conceito. Na prova, se cair um exercício diferente, quem decorou vai errar.
- O objetivo é que o modelo **aprenda o padrão**, não decore os dados.

### 4.1 Overfitting (Sobreajuste)

- O modelo **memoriza** os dados de treino em vez de aprender o padrão geral.
- Exemplo visual: em vez de traçar uma reta de tendência, o modelo tenta passar por **todos os pontos**, capturando micro-variações irrelevantes.
- Exemplo do gato e leopardo: se o modelo só viu gatos com olho amarelo e leopardos com olho azul, ele classifica **pela cor do olho** — e erra quando encontra um gato de olho azul.
- Analogia financeira: é como operar Bitcoin olhando micro-variações diárias em vez da tendência de longo prazo.
- Um **R² = 1** (coeficiente de determinação perfeito) pode ser indicativo de overfitting.

### 4.2 Underfitting (Subajuste)

- O modelo **aprende de menos** e não consegue capturar nem o padrão básico dos dados.
- Hoje é mais raro, dada a capacidade computacional disponível, mas pode ocorrer com datasets insuficientes ou poucas iterações de treinamento.

*A busca é pelo equilíbrio: um modelo que generaliza bem — nem memoriza demais (overfitting) nem aprende de menos (underfitting).*

---

## 5. Métricas de Avaliação de Modelos

### 5.1 Para Classificação

| Métrica | Descrição |
|---|---|
| **Acurácia** | Proporção geral de acertos (ex.: 92 de 100 = 92%). |
| **Precisão** | Quando o modelo disse "sim", estava certo? (acurácia geral por predição positiva). |
| **Recall** (Sensibilidade) | De todos os casos que realmente eram "sim", quantos o modelo acertou? (acurácia por classe real). |
| **F1 Score** | Média harmônica entre Precisão e Recall — integra ambas em uma única métrica. |

### 5.2 Para Regressão

| Métrica | Descrição |
|---|---|
| **MAE** (Mean Absolute Error) | Em média, quanto o modelo erra em valor absoluto. |
| **RMSE** (Root Mean Square Error) | Raiz do erro quadrático médio — atenua diferenças de magnitude. |
| **R²** (R-quadrado) | Varia de 0 a 1; indica quanto o modelo está ajustado aos dados. R² muito alto pode indicar overfitting; muito baixo, modelo inadequado. |

### 5.3 Matriz de Confusão

- Compara **predições do modelo** com os **valores reais**.
- Quatro quadrantes:
  - **Verdadeiro Positivo (VP)**: previu "sai" e realmente saiu.
  - **Verdadeiro Negativo (VN)**: previu "fica" e realmente ficou.
  - **Falso Positivo (FP)**: previu "sai" mas ficou.
  - **Falso Negativo (FN)**: previu "fica" mas saiu.

*Os falsos negativos e positivos são os "perigos" — é onde o modelo erra e onde decisões de negócio podem ser comprometidas.*

---

## 6. Seleção e Ajuste de Modelos

- Se os resultados são ruins com dados bons, o problema pode ser a **escolha do modelo**.
- Estratégias quando o modelo não performa:
  - Voltar a entender o fenômeno.
  - Trocar de modelo (ex.: de regressão logística para modelo **fuzzy**, **probabilístico** ou **híbrido com regras**).
  - Ajustar hiperparâmetros ou o threshold de classificação.

*Não existe modelo universal. A escolha depende do fenômeno, dos dados disponíveis e do nível de incerteza do problema.*

---

## 7. Limitações e Ética da IA

### 7.1 Dados enviesados → Modelos enviesados

- Exemplo do "GPT deprimido": se treinado apenas com textos de pessoas deprimidas, as respostas serão pessimistas.
- Caso real: governos africanos processando a OpenAI por danos emocionais aos operadores que rotularam conteúdo pesado durante o treinamento.

### 7.2 Correlação ≠ Causalidade

- **Vendas de sorvete × afogamentos**: correlação existe (ambos sobem no verão), mas sorvete não causa afogamento — a variável oculta é a **estação do ano**.
- **Piratas × aquecimento global**: menos piratas no mundo coincide com aumento de temperatura, mas a causa real é a **Revolução Industrial** e emissões de CO₂.

*Cuidado extremo ao interpretar correlações estatísticas como relações de causa e efeito. Sempre buscar a variável confundidora.*

### 7.3 Interpretabilidade

- Modelos muito complexos (redes neurais profundas / deep learning) são **caixas-pretas**: impossível rastrear perfeitamente o que acontece internamente.
- Em áreas críticas (saúde, justiça, sistemas econômicos), a falta de interpretabilidade é perigosa.
- Exemplo: um classificador de imagens pode estar usando o **fundo da foto** (e não o animal) para classificar — e sem interpretabilidade, não sabemos.

### 7.4 Supervisão Humana

- A IA "não quer saber de mais nada" — faz o que foi treinada para fazer, sem senso de consequência.
- **Decisões críticas ainda requerem supervisão humana**: a variável humana não pode ser removida do processo decisório.
- LLMs possuem travas para evitar comportamentos perigosos, mas a vigilância é contínua.

*O professor conclui a parte ética reforçando: a IA não é um oráculo. É uma ferramenta que exige validação, testes de hipótese e responsabilidade de quem a utiliza.*

---

## 8. Prática — Predição de Churn de Clientes (Telecom)

### 8.1 O Problema de Negócio

- **Churn** = cliente que cancela ou deixa de consumir o serviço.
- Objetivo: prever quais clientes têm maior probabilidade de cancelar para agir preventivamente (desconto, atendimento personalizado, produto sob medida).
- Pergunta-chave: *"Quais clientes têm a maior probabilidade de cancelar nos próximos meses?"*

### 8.2 O Dataset

- Cada linha = um cliente.
- Variáveis:
  - **Tempo de contrato** (há quanto tempo é cliente).
  - **Tipo de internet** (ou se não usa).
  - **Valor da mensalidade**.
  - **Tipo de contrato** (mensal, anual, bianual).
  - **Forma de pagamento** (boleto, cartão de crédito, débito automático).

### 8.3 Pipeline do Modelo

1. **Preparação dos dados**: converter variáveis categóricas para numéricas.
2. **Treino do modelo**: regressão logística com 80% dos dados.
3. **Teste**: avaliar performance com os 20% restantes.
4. **Saída**: probabilidade entre 0 e 1 (ex.: 0,82 = 82% de chance de cancelar).
5. **Threshold**: acima de 0,5 → classificado como provável cancelamento.
6. **Avaliação**: matriz de confusão, acurácia, precisão, recall, F1.

*A lógica fundamental: não gastar recursos de retenção com todos os clientes, mas focar naqueles identificados como alto risco de saída. Isso é eficiência orientada por dados.*

### 8.4 Ferramentas

- **Google Colab**: ambiente online para rodar notebooks Python (`.ipynb`) sem instalação local.
- **Kaggle**: fonte do dataset de telecom.
- Tarefa para os alunos: rodar o notebook por conta própria e trazer dúvidas na próxima aula.

---

## 9. Conceitos-Chave para Revisão

| Conceito | Definição rápida |
|---|---|
| **Aprendizado Supervisionado** | Treinamento com dados rotulados (gabarito). |
| **Aprendizado Não-Supervisionado** | Busca por padrões em dados sem rótulos. |
| **Aprendizado por Reforço** | Aprendizado por tentativa, erro, recompensa e punição. |
| **Overfitting** | Modelo memoriza dados; não generaliza. |
| **Underfitting** | Modelo aprende de menos; não captura o padrão. |
| **Acurácia** | % geral de acertos. |
| **Precisão** | Dos que o modelo disse "sim", quantos eram realmente "sim". |
| **Recall** | Dos que realmente eram "sim", quantos o modelo acertou. |
| **F1 Score** | Média harmônica de Precisão e Recall. |
| **MAE / RMSE / R²** | Métricas de erro e ajuste para regressão. |
| **Matriz de Confusão** | Tabela VP/VN/FP/FN comparando predição vs. realidade. |
| **Churn** | Cancelamento ou abandono de serviço por parte do cliente. |
| **Threshold** | Limiar de decisão para classificação (ex.: 0,5). |
| **RLHF** | Reinforcement Learning from Human Feedback. |

---

*Resumo gerado a partir da transcrição VTT da Aula 1 — Fundamentos da Inteligência Artificial, curso de Residência Tecnológica em Gêmeo Digital e 5G.*
