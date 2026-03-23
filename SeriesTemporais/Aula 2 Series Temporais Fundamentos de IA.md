# Aula 2 — Séries Temporais e Fundamentos de IA

**Resumo didático** da transcrição da aula ministrada no curso de Residência Tecnológica em Gêmeo Digital e 5G.

---

## 1. Contexto e Revisão

A aula consolida conceitos de machine learning da aula anterior e introduz modelos estatísticos e auto-regressivos para análise de séries temporais. Iniciou com problemas técnicos (compartilhamento de áudio/vídeo), demonstrando adaptabilidade no ensino remoto.

---

## 2. Problema de Churn — Revisão Prática

### 2.1 Cenário de Negócio

- **Empresa de telecomunicações** com alto custo de aquisição de clientes
- **Problema**: clientes cancelando após descobrir "propaganda enganosa"
- **Objetivo**: prever probabilidade de cancelamento para ações preventivas

### 2.2 Dataset — Análise Exploratória

- **7.043 clientes** e **20 variáveis**
- **Variáveis demográficas**: gênero, senioridade, estado civil
- **Variáveis de serviço**: tipo de internet, telefonia, linhas múltiplas
- **Variáveis de segurança**: antivírus, online security
- **Variáveis de cobrança**: valor mensal, tempo como cliente

*O professor enfatiza: "entender o fenômeno antes de jogar dados no modelo". Pesquisar no Kaggle o significado de cada variável é prática essencial.*

---

## 3. Desafios Técnicos Identificados

### 3.1 Desbalanceamento de Dados

- **Variável resposta churn**: muito mais "Não" (ficam) do que "Sim" (saem)
- **Impacto**: pode afetar desempenho do modelo
- **Necessidade**: técnicas específicas para tratamento

### 3.2 Variáveis Categóricas

- **Problema**: modelos matemáticos só processam números
- **Solução**: converter categorias para representações numéricas
- **Princípio**: "computadores adoram números binários"

---

## 4. Pré-processamento de Dados

### 4.1 Limpeza de Features

- **Remoção de Customer ID**: não contribui para modelo preditivo atual
- **Prática**: eliminar colunas irrelevantes para reduzir ruído

### 4.2 Binarização da Variável Resposta

- **Transformação**: "Sim" → 1, "Não" → 0
- **Objetivo**: tornar a variável compatível com modelos matemáticos

### 4.3 One-Hot Encoding

Para variáveis categóricas com múltiplas categorias (ex: Internet Service):

| Categoria Original | Coluna DSL | Coluna Fiber | Coluna No |
|---|---|---|---|
| DSL | 1 | 0 | 0 |
| Fiber Optic | 0 | 1 | 0 |
| No | 0 | 0 | 1 |

*Vantagem sobre codificação numérica (1, 2, 3): não cria falsa hierarquia entre categorias.*

---

## 5. Fundamentos Matemáticos dos Modelos

### 5.1 Estrutura Geral do Modelo

**Y = a₁X₁ + a₂X₂ + a₃X₃ + ... + aₙXₙ**

Onde:
- **Y**: variável dependente (resposta)
- **X₁, X₂, ..., Xₙ**: variáveis independentes (features)
- **a₁, a₂, ..., aₙ**: coeficientes ajustados durante treinamento

### 5.2 Função de Transformação

- **Modelos de classificação**: aplicam função adicional (ex: logística)
- **Objetivo**: transformar resultado linear em probabilidades (0 a 1)
- **Trabalho do modelo**: encontrar coeficientes que minimizem erro

*O professor destaca: "o trabalho principal do modelo é encontrar os coeficientes ideais".*

---

## 6. Divisão e Validação de Dados

### 6.1 Conjuntos Treino/Teste

- **Divisão típica**: 80% treino / 20% teste
- **Objetivo**: avaliar capacidade de generalização
- **Prevenção**: evitar overfitting (memorização vs. aprendizado)

### 6.2 Pipeline Completo

1. **Preparação**: converter categóricas para numéricas
2. **Treino**: ajustar modelo com 80% dos dados
3. **Teste**: avaliar performance com 20% restantes
4. **Validação**: matriz de confusão, métricas de classificação

---

## 7. Séries Temporais — Conceitos Fundamentais

### 7.1 Definição

- **Dados distribuídos no tempo**
- **Abordagens especializadas** para análise e previsão
- **Diferença fundamental**: dependência temporal das observações

### 7.2 Modelo Prophet (Facebook)

- **Superior a modelos tradicionais** para séries temporais
- **Capacidades**: detecção automática de mudanças de tendência
- **Adaptação**: ajusta previsões quando padrões mudam

---

## 8. Estudo de Caso — Magazine Luiza (MGLU3)

### 8.1 Setup do Ambiente

- **Instalação**: biblioteca Prophet
- **Desafios técnicos**: problemas com instalação em ambiente virtual
- **Configuração**: modelo linear aditivo com parâmetros específicos

### 8.2 Padrões Identificados

| Padrão | Descrição | Causa Provável |
|---|---|---|
| **Sazonalidade semanal** | Preços mais altos segundas, mais baixas sextas | Investidores fecham posições no fim de semana |
| **Tendência de queda** | Queda acentuada nos preços | Fatores macroeconômicos e específicos da empresa |

### 8.3 Comportamento dos Investidores

- **Sexta-feira**: fechamento de posições para evitar riscos de fim de semana
- **Segunda-feira**: reabertura de posições, preços mais altos
- **Lógica**: não carregar ativos durante períodos de incerteza

*Insight prático: "perdemos dinheiro a semana inteira, chegou sexta-feira fecha posição, gasta no bar, segunda-feira compra na alta de novo".*

---

## 9. Validação Prática das Previsões

### 9.1 Previsão vs. Realidade

| Período | Previsão do Modelo | Valor Real | Acerto |
|---|---|---|---|
| **Fevereiro/2024** | ~R\$ 20 | R\$ 20 | ✓ |
| **Março/2024** | Queda | < R\$ 20 | ✓ |
| **Período posterior** | Tendência de queda | ~R\$ 8 | ✓ |

### 9.2 Impacto Econômico

- **Modelo previu queda** em maio/2024
- **Realidade**: ações despencaram de R\$ 20 para R\$ 8
- **Aplicação**: vendas antecipadas poderiam gerar lucros significativos

*Demonstração prática do valor econômico de previsões acuradas.*

---

## 10. Capacidades Avançadas do Prophet

### 10.1 Detecção de Mudança de Tendência

- **Identificação automática** de pontos de inflexão
- **Rastreabilidade**: possível controlar e verificar pontos detectados
- **Adaptação**: modelo ajusta previsões quando identifica novas tendências

### 10.2 Overfitting em Séries Temporais

- **Risco**: modelo pode se ajustar excessivamente ao histórico
- **Objetivo**: não modelar passado perfeitamente, mas prever futuro
- **Equilíbrio**: generalização vs. especialização

---

## 11. Ferramentas e Ambiente

### 11.1 Google Colab

- **Máquina virtual** com recursos limitados
- **Armazenamento**: vinculado ao Google Drive
- **Desafios**: limitações de memória e espaço

### 11.2 Bibliotecas Utilizadas

- **Prophet**: modelagem de séries temporais
- **Pandas**: manipulação de dataframes
- **Scikit-learn**: pré-processamento e divisão de dados

---

## 12. Encerramento e Próximos Passos

### 12.1 Encerramento da Aula

- **Realização da chamada** oficial
- **Problemas técnicos**: alguns alunos sem acesso à plataforma
- **Comunicação**: materiais disponíveis no grupo e plataforma oficial

### 12.2 Próxima Aula

- **Tópico**: Large Language Models (LLMs)
- **Foco**: geração de texto e aplicações profissionais
- **Continuidade**: programa com várias etapas planejadas

---

## 13. Conceitos-Chave para Revisão

| Conceito | Definição rápida |
|---|---|
| **Churn** | Cancelamento ou abandono de serviço |
| **One-Hot Encoding** | Transformação de categóricas em colunas binárias |
| **Desbalanceamento** | Distribuição desigual entre classes |
| **Série Temporal** | Dados com dependência temporal |
| **Prophet** | Modelo Facebook para séries temporais |
| **Sazonalidade** | Padrões que se repetem em períodos regulares |
| **Tendência** | Direção geral de movimento dos dados |
| **Overfitting Temporal** | Memorização de padrões históricos |
| **Ponto de Mudança** | Momento onde a tendência se altera |
| **Validação Prática** | Comparação de previsões com valores reais |

---

*Resumo gerado a partir da transcrição VTT da Aula 2 — Séries Temporais e Fundamentos de IA, curso de Residência Tecnológica em Gêmeo Digital e 5G.*
