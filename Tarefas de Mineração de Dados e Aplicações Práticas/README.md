![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=Minera%C3%A7%C3%A3o%20de%20Dados%20e%20Aplica%C3%A7%C3%B5es%20Pr%C3%A1ticas&fontSize=35&fontAlignY=35&animation=twinkling)

# ⛏️ Tarefas de Mineração de Dados e Aplicações Práticas

![visitors](https://visitor-badge.laobi.icu/badge?page_id=ArvoreDosSaberes.Capacitacao_GemeosDigitais.TarefasMineracaoDados)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
![Video Content](https://img.shields.io/badge/Content-Video%20Lessons-red)
![Educational](https://img.shields.io/badge/Type-Educational-green)
![Status](https://img.shields.io/badge/Status-Ongoing-yellow)

## 🎯 Objetivo da Aula

Identificar e compreender as principais tarefas da mineração de dados, relacionando-as a problemas reais e ao apoio à tomada de decisão. A aula parte da Análise Exploratória de Dados (EDA) univariada em direção à análise multivariada com PCA (Análise de Componentes Principais), culminando na detecção e interpretação de anomalias em sistemas reais.

## 🔗 Links

- **Link da Aula:** [Reunião Microsoft Teams](https://teams.microsoft.com/meet/28506812334240?p=8H0AqQPFK8js7QcyD4)
- **Link da Gravação:** [Gravação da Aula - SharePoint](https://facens-my.sharepoint.com/:v:/g/personal/felipe_fengler_facens_br/IQBTyybXoXhxSb8SbPCQggQSAcbWgDpZ-MJDqo7AvfD0jqk?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=RLYyhD)
- **Link complementar:** [PCA in Python with DataGy](https://datagy.io/python-pca/)

## 📁 Material de Apoio

| # | Arquivo | Tema |
|---|---------|------|
| 1 | [1.Anomalia-Erro-ou-Comportamento-Esperado.pdf](1.Anomalia-Erro-ou-Comportamento-Esperado.pdf) | Da EDA à visão multivariada e PCA |
| 2 | [2.Tornando-a-Analise-Multivariada-Aplicavel.pdf](2.Tornando-a-Analise-Multivariada-Aplicavel.pdf) | PCA aplicada, anomalias e conexão com ML |

---

## 📖 Descrição da Aula

### 🔍 Parte 1 — Anomalia, Erro ou Comportamento Esperado?

A primeira apresentação estabelece a transição da Análise Exploratória de Dados (EDA) para a detecção de anomalias, introduzindo a necessidade de uma visão multivariada.

#### 🧭 Após a EDA, para onde ir?

Após a análise exploratória (distribuições, valores ausentes, correlações), surgem caminhos possíveis: **classificação**, **regressão**, **segmentação** — ou um caminho menos óbvio: **identificar o que foge do padrão**. Modelos preditivos respondem *o que vai acontecer*; detecção de anomalias responde *o que não deveria estar aqui*.

#### ❓ O que é uma anomalia?

Um valor extremo pode ser erro de digitação, evento genuinamente raro, comportamento fraudulento ou variação natural de alta magnitude. A definição de "anômalo" depende do **modelo de normalidade** adotado como referência. Três tipos são diferenciados:

- **Erro de dado** — falha na coleta, digitação ou integração; deve ser corrigido/removido.
- **Evento raro (real)** — estatisticamente incomum mas legítimo (ex.: pico de Black Friday); carrega informação valiosa.
- **Comportamento suspeito** — dado aparentemente válido mas com padrão incomum para o contexto (fraude, abuso); requer investigação com domínio do negócio.

#### ⚠️ Limitação da análise univariada

A EDA univariada (histogramas, boxplots, estatísticas descritivas) inspeciona cada variável isoladamente. Porém, um ponto pode ser perfeitamente normal em cada variável individualmente e completamente anômalo quando todas as dimensões são consideradas juntas. A anomalia pode estar no **padrão combinado**, não nos valores individuais.

#### 🌐 Visão multivariada — o dataset como sistema

A abordagem multivariada trata o conjunto de dados como um **sistema integrado**, revelando:

- **Relações emergentes** — padrões que só existem com múltiplas variáveis simultâneas.
- **Estrutura latente** — direções de maior variabilidade que revelam a organização real dos dados.
- **Anomalias contextuais** — pontos que só se mostram anômalos no espaço multidimensional.

#### 📐 Introdução à PCA

A **Análise de Componentes Principais (PCA)** é uma técnica de redução de dimensionalidade que transforma variáveis correlacionadas em componentes não correlacionados, preservando o máximo da variância original. PC1 captura a maior variância, PC2 a segunda maior (ortogonal a PC1), e assim por diante. PCA não é um modelo preditivo — é uma **lente de inspeção e preparação**.

#### 📊 Visualização no espaço PCA

- **Scatter PC1 vs PC2** — janela para a estrutura global; pontos próximos compartilham padrão em todas as variáveis originais.
- **Regiões densas** — comportamento normal e recorrente do sistema.
- **Regiões esparsas** — candidatos naturais a anomalias.
- **Separações e lacunas** — populações distintas nos dados, possíveis segmentos naturais.
- **Coloração por grupo** — revela estrutura latente: grupos separados, sobreposições, pontos isolados, gradientes.

#### 🔀 Grupos homogêneos vs. mistos

O PCA pode revelar **grupos homogêneos** (baixa variância interna, fronteiras bem definidas) e **grupos mistos** (alta variância interna, fronteiras difusas). Grupos mistos são sinal de alerta: podem conter subpopulações não identificadas, anomalias contextuais ou transições de regime temporal.

#### 🕵️ Investigação dos pontos atípicos

A apresentação encerra propondo um pipeline formal de investigação:

1. **Identificar** — localizar pontos candidatos a anomalia no espaço multivariado.
2. **Quantificar** — medir o grau de anomalia com métricas formais (distância de Mahalanobis, scores de isolamento).
3. **Interpretar** — cruzar com domínio do negócio (erro, evento raro ou comportamento suspeito).
4. **Agir** — remover, corrigir, sinalizar ou investigar conforme o tipo de anomalia.

---

### 🛠️ Parte 2 — Tornando a Análise Multivariada Aplicável

A segunda apresentação aprofunda a PCA com técnicas práticas, interpretação de resultados e conexão com Machine Learning.

#### 🎻 Da análise univariada à multivariada

Reforça que analisar uma variável por vez é como ouvir cada instrumento de uma orquestra separadamente — perde-se a sinfonia. Ferramentas iniciais para a visão multivariada: **correlograma** (correlações lineares entre pares) e **scatter plots** (agrupamentos e outliers bivariados).

#### 🔬 PCA em detalhe

- **Variância explicada** — cada componente captura uma fração da variabilidade total.
- **Critério de Kaiser** — manter componentes com autovalor > 1.
- **Coordenadas** — direção de cada componente no espaço original.
- **Contribuições** — quanto cada variável original pesa em cada componente.
- **Factor loadings** — intensidade da relação entre variável original e componente.

#### 💰 Interpretação prática (caso de remuneração)

- **PC1 (Magnitude)** — diferencia quem ganha mais de quem ganha menos; todas as variáveis carregam no mesmo sentido.
- **PC2 (Composição)** — diferencia *como* a remuneração é estruturada (mais variável via bônus/PLR vs. mais fixa via salário-base).

Dois funcionários com remuneração total idêntica podem ter perfis completamente distintos — a PCA torna isso visível.

#### 🗺️ Biplot — visualizando o sistema

Combina em um único gráfico a estrutura das variáveis (vetores) e o posicionamento das amostras (pontos):

1. **Vetores** — para onde cada variável "puxa" o espaço; vetores próximos indicam variáveis correlacionadas.
2. **Amostras** — cada ponto é uma observação; pontos próximos têm perfis similares.
3. **Extremos** — pontos distantes do centro são candidatos a anomalias.

#### 💥 Impacto de outliers na PCA

Outliers têm variância alta e podem distorcer os componentes. O processo ideal é **iterativo**: aplique PCA → identifique extremos → investigue → trate → reaplique.

#### 🔄 PCA com rotação

A rotação não muda os dados nem a variância total explicada — muda apenas a forma de olhar para a estrutura:

- **Sem rotação** — responde "onde está a variância?" (compressão, feature engineering).
- **Com rotação** — responde "como o sistema se organiza em dimensões interpretáveis?" (análise fatorial, construção de índices).

#### 🧩 Raciocínio completo da aula (camadas)

1. **Análise univariada** — variáveis isoladas, base descritiva.
2. **Correlações** — relações entre pares, primeiros padrões.
3. **PCA** — estrutura multidimensional, componentes.
4. **Biplot** — variáveis + amostras, mapa do sistema.
5. **Anomalias** — desvios do padrão, investigação.

Cada camada adiciona profundidade analítica sem substituir a anterior.

#### 🚀 Aplicações práticas

- **Detecção de anomalias** — base para sistemas de alerta em tempo real.
- **Comparação de grupos** — comparar perfis de equipes, departamentos ou períodos.
- **Análise temporal** — monitorar evolução dos componentes ao longo do tempo.

#### 🤖 Conexão com Machine Learning

- **Redução de dimensionalidade** — elimina ruído e multicolinearidade, melhora generalização.
- **Detecção de outliers não-supervisionada** — Isolation Forest e Autoencoder operam no espaço reduzido.
- **Feature engineering** — componentes principais como features em modelos supervisionados.

#### ✅ Checklist do analista multivariado

1. Verificar correlações entre variáveis antes da PCA
2. Padronizar as variáveis (Z-score)
3. Escolher número de componentes (scree plot + Kaiser)
4. Interpretar loadings e contribuições
5. Avaliar necessidade de rotação
6. Identificar e investigar outliers no biplot
7. Validar estrutura com e sem outliers
8. Documentar insights substantivos

> Os primeiros 4 itens são sempre obrigatórios. Os últimos 4 dependem do contexto e dos objetivos.

#### ⚡ Armadilhas comuns

- **Não padronizar** — PCA captura escala em vez de estrutura.
- **Reter componentes demais** — PCA é útil pela redução, não pela expansão.
- **Forçar interpretação** — nem todo componente tem nome óbvio.
- **Remover outliers sem investigar** — a anomalia pode ser o dado mais valioso.

#### ➡️ Próximos passos

- **Clustering** — K-Means, DBSCAN e métodos hierárquicos para segmentar o espaço PCA.
- **Autoencoders** — PCA não-linear com redes neurais para detecção de anomalias em alta dimensionalidade.

---

## 💭 Reflexão Final

> *"A análise multivariada não revela verdades ocultas nos dados. Ela revela estruturas que você ainda não sabia que estavam lá — e te dá linguagem para descrevê-las."*

A PCA é uma **lente**, não uma receita. O objetivo não é apenas executar etapas, mas desenvolver uma **estrutura de raciocínio** para enfrentar dados complexos: identificar padrões, nomear dimensões, detectar desvios e conectar tudo a decisões reais.

---

## ⚠️ Material Complementar - UniFacens

Os materiais em formato PDF disponibilizados neste módulo são **propriedade intelectual da UniFacens** e foram compartilhados exclusivamente para facilitar o acesso dos alunos da **Capacitação Gêmeos Digitais**.

- ✅ **Permitido**: Acesso e uso pelos alunos matriculados na capacitação
- ✅ **Permitido**: Download para estudo pessoal
- ❌ **Proibido**: Reprodução e distribuição não autorizada
- ❌ **Proibido**: Uso comercial ou compartilhamento externo

---

## 📊 Informações do Módulo

*Este módulo apresenta o estudo de Tarefas de Mineração de Dados e Aplicações Práticas — da EDA à PCA e detecção de anomalias — para a Capacitação em Gêmeos Digitais e 5G, pertencente ao repositório **Capacitacao_GemeosDigitais** da organização **ArvoreDosSaberes**.*

**Repositório:** [Capacitacao_GemeosDigitais](https://github.com/ArvoreDosSaberes/Capacitacao_GemeosDigitais)
**Organização:** [ArvoreDosSaberes](https://github.com/ArvoreDosSaberes)
**Data de criação:** 2026
**Licença:** CC BY-SA 4.0

![footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer&animation=twinkling)