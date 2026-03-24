# Módulo de Inteligência Artificial e Machine Learning

![visitors](https://visitor-badge.laobi.icu/badge?page_id=ArvoreDosSaberes.Capacitacao_GemeosDigitais.InteligenciaArtificial)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-green)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-blue)
![Status](https://img.shields.io/badge/Status-Educa%C3%A7%C3%A3o-brightgreen)
![Level](https://img.shields.io/badge/Level-Beginner%20to%20Intermediate-yellow)

## 📋 Visão Geral

Este módulo oferece uma capacitação completa em Inteligência Artificial e Machine Learning, combinando teoria fundamental com prática hands-on. O material está organizado para proporcionar um aprendizado progressivo, desde conceitos básicos até implementações avançadas.

### 🎯 Objetivos de Aprendizagem

- Compreender os fundamentos de Machine Learning
- Dominar técnicas de manipulação de dados com Pandas
- Implementar modelos de classificação do início ao fim
- Avaliar desempenho de modelos com métricas adequadas
- Aplicar boas práticas em projetos de IA

## � Configuração do Ambiente

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Ambiente virtual recomendado

### Instalação das Dependências

```bash
# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### Dependências Principais

- **pandas**: Manipulação e análise de dados
- **numpy**: Computação numérica
- **matplotlib**: Visualização de dados
- **seaborn**: Visualizações estatísticas
- **scikit-learn**: Biblioteca de Machine Learning
- **kagglehub**: Acesso a datasets do Kaggle

## � Estrutura do Módulo

```text
InteligenciaArtificial/
├── README.md                                    # Este arquivo - documentação completa
├── requirements.txt                             # Dependências Python
├── Aula_1_notebook_ml_churn_colab.ipynb       # Notebook prático principal
├── test_notebook.py                           # Scripts de teste e validação
├── Teoria-Aprendizado-de-Maquina-Conceitos-Fundamentais-e-Tipos-de-Modelos.pdf  # Material teórico
├── Pratica-construindo-um-modelo-de-aprendizado-de-maquina.pdf  # Guia prático
├── PRINCIPIOS FUNDAMENTAIS DA ETICA DA IA DA IBM.md  # Princípios éticos da IBM
├── PRINCIPAIS PRINCIPIOS PARA ETICA DA IA.md         # Princípios do Relatório Belmont
├── PRINCIPAIS PREOCUPAÇÕES DA IA HOJE.md              # Preocupações atuais em IA
├── ORGANIZAÇÕES QUE PROMOVEM ETICA EM IA.md           # Organizações de ética em IA
├── GOVERNANCA.md                                      # Governança de IA
└── CINCO PILARES PARA GUIAR A ADOÇÃO DE TECNOLOGIAS LIGADAS A IA DA IBM.md  # Pilares IBM
```

## 📚 Material Didático

### 📖 Material Teórico

#### PDF: Teoria - Aprendizado de Máquina: Conceitos Fundamentais e Tipos de Modelos

- Fundamentos de Machine Learning
- Tipos de aprendizado: supervisionado, não supervisionado, por reforço
- Algoritmos clássicos e modernos
- Métricas de avaliação
- Overfitting e underfitting
- Validação cruzada e regularização

### Material Prático

#### PDF: Prática - Construindo um Modelo de Aprendizado de Máquina

- Guia passo a passo para construção de modelos
- Checklist de pré-processamento
- Dicas para feature engineering
- Estratégias de validação
- Interpretação de resultados
- Deploy de modelos

---

## 🎯 Tutorial Prático: Previsão de Churn de Clientes

Este tutorial explica passo a passo o notebook `Aula_1_notebook_ml_churn_colab.ipynb`, que demonstra um fluxo completo de Machine Learning para prever cancelamento de clientes (churn) usando Pandas e Scikit-learn. Cada comando Pandas será explicado detalhadamente para que você compreenda não apenas o que faz, mas por que e como funciona.

## 📚 Estrutura do Tutorial

1. **Importação das Bibliotecas**
2. **Carregamento dos Dados**
3. **Exploração Inicial dos Dados**
4. **Visualização dos Dados**
5. **Preparação dos Dados**
6. **Divisão Treino/Teste**
7. **Normalização dos Dados**
8. **Treinamento do Modelo**
9. **Avaliação do Modelo**

---

## 🔧 1. Importação das Bibliotecas

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
```

### Explicação das Importações:

- **`pandas as pd`**: Biblioteca fundamental para manipulação e análise de dados. O apelido `pd` é uma convenção universal.
- **`numpy as np`**: Biblioteca para computação numérica, essencial para operações matemáticas eficientes.
- **`matplotlib.pyplot as plt`**: Biblioteca para criação de gráficos e visualizações.
- **`seaborn as sns`**: Biblioteca baseada em matplotlib para visualizações estatísticas mais atraentes.
- **Módulos sklearn**: Vários componentes do Scikit-learn para Machine Learning.

---

## 📥 2. Carregamento dos Dados

### Download do Dataset

```python
import kagglehub

# Download latest version
path = kagglehub.dataset_download("blastchar/telco-customer-churn")
print("Path to dataset files:", path)
```

**O que acontece aqui?**
- `kagglehub.dataset_download()` baixa automaticamente o dataset do Kaggle
- O dataset é salvo em um diretório temporário no seu computador
- O caminho é retornado para que possamos acessar os arquivos

### Carregamento com Pandas

```python
df = pd.read_csv(path + "/WA_Fn-UseC_-Telco-Customer-Churn.csv")
df.head()
```

### 🐼 **Comando Pandas Explicado: `pd.read_csv()`**

**O que faz?** Lê um arquivo CSV e o transforma em um DataFrame Pandas.

**Parâmetros importantes:**
- **Caminho do arquivo**: Local onde o CSV está armazenado
- **Sep**: Separador (padrão é vírgula)
- **Header**: Linha que contém os nomes das colunas (padrão é 0)
- **Encoding**: Codificação dos caracteres (ex: 'utf-8', 'latin-1')

**Por que usar?** Arquivos CSV são o formato mais comum para armazenar dados tabulares. O Pandas os converte automaticamente em estruturas manipuláveis.

### 🐼 **Comando Pandas Explicado: `df.head()`**

**O que faz?** Exibe as primeiras 5 linhas do DataFrame.

**Parâmetros:**
- **Sem parâmetros**: Mostra 5 linhas
- **n**: Número específico de linhas (ex: `df.head(10)`)

**Por que usar?** Para visualizar rapidamente a estrutura dos dados, verificar se o carregamento foi bem-sucedido e entender o formato das colunas.

---

## 🔍 3. Exploração Inicial dos Dados

### Dimensões e Informações

```python
df.shape
df.info()
```

### 🐼 **Comando Pandas Explicado: `df.shape`**

**O que faz?** Retorna uma tupla com (número de linhas, número de colunas).

**Exemplo de retorno:** `(7043, 21)`

**Por que usar?** Para entender o tamanho do seu dataset rapidamente. Essencial para planejar análises e estimar recursos computacionais necessários.

### 🐼 **Comando Pandas Explicado: `df.info()`**

**O que faz?** Exibe um resumo completo do DataFrame:
- Número total de entradas
- Índice inicial e final
- Nome de cada coluna
- Contagem de valores não nulos
- Tipo de dados de cada coluna
- Uso de memória

**Por que usar?** É o comando mais importante para diagnóstico inicial dos dados. Ajuda a identificar:
- Colunas com valores ausentes
- Tipos de dados incorretos
- Uso excessivo de memória
- Necessidade de limpeza

**Tipos de dados comuns:**
- **object**: Texto/string
- **int64**: Números inteiros
- **float64**: Números decimais
- **bool**: Verdadeiro/Falso
- **datetime64**: Datas e horas

---

## 📊 4. Visualização dos Dados

### Gráfico de Contagem

```python
sns.countplot(x='Churn', data=df)
plt.show()
```

**O que faz?** Cria um gráfico de barras mostrando a contagem de cada categoria na coluna 'Churn'.

**Por que usar?** Para entender o balanceamento das classes. Em problemas de classificação, é crucial saber se temos dados balanceados entre as classes.

**Interpretação:**
- Se uma classe tem muito mais exemplos que outra, o modelo pode ter viés
- Técnicas de balanceamento podem ser necessárias (oversampling, undersampling)

---

## 🧹 5. Preparação dos Dados

### Remoção de Coluna

```python
df = df.drop('customerID', axis=1)
```

### 🐼 **Comando Pandas Explicado: `df.drop()`**

**O que faz?** Remove linhas ou colunas do DataFrame.

**Parâmetros importantes:**
- **labels**: Nome da(s) linha(s)/coluna(s) a remover
- **axis**: 0 para linhas, 1 para colunas
- **inplace**: True para modificar o DataFrame original

**Exemplos:**
```python
# Remover coluna
df.drop('coluna', axis=1)

# Remover múltiplas colunas
df.drop(['coluna1', 'coluna2'], axis=1)

# Remover linhas
df.drop([0, 1, 2])  # remove linhas 0, 1, 2
```

**Por que usar?** Para remover informações irrelevantes que podem prejudicar o modelo ou consumir memória desnecessariamente.

### Mapeamento de Valores

```python
df['Churn'] = df['Churn'].map({'Yes':1,'No':0})
```

### 🐼 **Comando Pandas Explicado: `df['coluna'].map()`**

**O que faz?** Aplica uma função ou mapeamento a cada valor da coluna.

**Parâmetros:**
- **Dicionário**: Mapeamento chave-valor
- **Função**: Função a aplicar em cada elemento

**Exemplos:**
```python
# Mapeamento com dicionário
df['status'].map({'ativo': 1, 'inativo': 0})

# Mapeamento com função
df['preco'].map(lambda x: x * 2)
```

**Por que usar?** Para transformar dados categóricos em numéricos, essencial para algoritmos de Machine Learning.

### Conversão de Tipos

```python
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'] = df['TotalCharges'].fillna(0)
```

### 🐼 **Comando Pandas Explicado: `pd.to_numeric()`**

**O que faz?** Converte uma série para tipo numérico.

**Parâmetros importantes:**
- **errors='coerce'**: Transforma valores não conversíveis em NaN (Not a Number)
- **errors='raise'**: Levanta erro em valores não conversíveis (padrão)
- **errors='ignore'**: Mantém valores originais não conversíveis

**Por que usar?** Muitas vezes dados numéricos são lidos como texto devido a formatação ou valores inválidos. Esta função corrige o tipo.

### 🐼 **Comando Pandas Explicado: `df.fillna()`**

**O que faz?** Preenche valores NaN (ausentes) com um valor especificado.

**Parâmetros:**
- **value**: Valor para preencher os NaN
- **method**: 'ffill' (forward fill), 'bfill' (backward fill)
- **inplace**: True para modificar o DataFrame original

**Estratégias comuns:**
```python
# Preencher com zero
df.fillna(0)

# Preencher com média
df.fillna(df.mean())

# Preencher com mediana
df.fillna(df.median())
```

**Por que usar?** Valores ausentes quebram algoritmos de Machine Learning. Precisamos tratá-los adequadamente.

### One-Hot Encoding

```python
df = pd.get_dummies(df, drop_first=True)
```

### 🐼 **Comando Pandas Explicado: `pd.get_dummies()`**

**O que faz?** Transforma variáveis categóricas em colunas binárias (0/1).

**Parâmetros importantes:**
- **drop_first=True**: Remove a primeira categoria de cada variável para evitar multicolinearidade
- **prefix**: Prefixo para novas colunas
- **columns**: Colunas específicas para transformar

**Exemplo prático:**
```
Antes:
| Contract     |
|--------------|
| Month-to-month |
| One year     |
| Two year     |
| Month-to-month |

Depois (drop_first=True):
| Contract_One year | Contract_Two year |
|-------------------|-------------------|
| 0                 | 0                 |
| 1                 | 0                 |
| 0                 | 1                 |
| 0                 | 0                 |
```

**Por que usar?** Algoritmos de Machine Learning entendem apenas números, não texto. One-Hot encoding é a técnica padrão para converter categorias.

---

## ✂️ 6. Separação Features/Target

```python
X = df.drop('Churn', axis=1)
y = df['Churn']
```

### 🐼 **Comando Pandas Explicado: Separação Features e Target**

**O que faz?** Divide o DataFrame em:
- **X**: Features (variáveis explicativas)
- **y**: Target (variável a ser prevista)

**Por que usar?** Em aprendizado supervisionado, precisamos separar claramente o que queremos prever (target) das informações que usaremos para prever (features).

---

## 🎲 7. Divisão Treino/Teste

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

**O que faz?** Divide os dados em conjuntos de treino e teste.

**Parâmetros importantes:**
- **test_size=0.2**: 20% dos dados para teste, 80% para treino
- **random_state=42**: Semente para reprodutibilidade dos resultados
- **stratify**: Mantém proporção das classes (importante em dados desbalanceados)

**Por que usar?** Para avaliar o desempenho do modelo em dados nunca vistos, evitando overfitting.

---

## 📏 8. Normalização dos Dados

```python
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

**O que faz?** Padroniza as features para média 0 e desvio padrão 1.

**Por que usar?** Algoritmos sensíveis à escala (como regressão logística) funcionam melhor com dados normalizados.

---

## 🤖 9. Treinamento e Avaliação

### Treinamento do Modelo

```python
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
```

### Predições e Métricas

```python
y_pred = model.predict(X_test)
accuracy_score(y_test, y_pred)
```

### Matriz de Confusão

```python
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d')
plt.show()
```

### Relatório de Classificação

```python
print(classification_report(y_test, y_pred))
```

---

## 📊 Interpretação dos Resultados

### Métricas Explicadas:

- **Accuracy**: Proporção de acertos totais
- **Precision**: Dos que previmos como positivos, quantos realmente são
- **Recall**: Dos que realmente são positivos, quantos previmos corretamente
- **F1-Score**: Média harmônica entre precision e recall

### Por que o Churn (classe 1) tem desempenho menor?

1. **Dados desbalanceados**: Menos exemplos de churn
2. **Complexidade do fenômeno**: Cancelamento envolve múltiplos fatores
3. **Features insuficientes**: Podem faltar variáveis importantes
4. **Ruído nos dados**: Clientes cancelam por motivos não capturados

---

## 🎓 Lições Aprendidas

### Comandos Pandas Essenciais:

1. **`pd.read_csv()`**: Carregar dados de arquivos CSV
2. **`df.head()`**: Visualizar primeiras linhas
3. **`df.shape`**: Conhecer dimensões do dataset
4. **`df.info()`**: Diagnóstico completo dos dados
5. **`df.drop()`**: Remover colunas/linhas desnecessárias
6. **`df['coluna'].map()`**: Transformar valores categóricos
7. **`pd.to_numeric()`**: Converter para tipo numérico
8. **`df.fillna()`**: Tratar valores ausentes
9. **`pd.get_dummies()`**: One-Hot encoding

### Boas Práticas:

- Sempre visualize os dados antes de processar
- Verifique tipos de dados e valores ausentes
- Documente cada transformação realizada
- Use random_state para reprodutibilidade
- Avalie múltiplas métricas, não apenas accuracy

---

## 🎯 Como Usar Este Módulo

### 📋 Rota de Aprendizagem Sugerida

1. **📖 Estudar o Material Teórico**
   - Leia o PDF "Teoria - Aprendizado de Máquina: Conceitos Fundamentais"
   - Foque em entender os conceitos fundamentais antes de praticar

2. **🛠️ Consultar o Guia Prático**
   - Revise o PDF "Prática - Construindo um Modelo de Aprendizado de Máquina"
   - Use como referência durante a implementação

3. **💻 Executar o Notebook Principal**
   - Abra `Aula_1_notebook_ml_churn_colab.ipynb`
   - Siga o tutorial passo a passo
   - Experimente modificar parâmetros e testar diferentes abordagens

4. **🧪 Testar e Validar**
   - Execute os scripts em `test_notebook.py`
   - Verifique seu entendimento com os testes proporcionados

### 💡 Dicas de Estudo

- **Aprendizado Ativo**: Não apenas execute o código, mas modifique-o para ver o que acontece
- **Documentação**: Mantenha anotações sobre conceitos importantes
- **Experimentação**: Tente diferentes algoritmos e compare resultados
- **Repetição**: Refaça os exercícios sem consultar o material para solidificar conhecimento

---

## 🚀 Próximos Passos

### Para Continuar Sua Jornada em IA

1. **Feature Engineering**: Criar novas features a partir das existentes
2. **Hyperparameter Tuning**: Otimizar parâmetros do modelo
3. **Cross-Validation**: Validação mais robusta
4. **Ensemble Methods**: Combinar múltiplos modelos
5. **Deploy**: Colocar o modelo em produção

### Módulos Relacionados

- **📈 Séries Temporais**: Aplicar técnicas de IA para previsão de dados temporais
- **🔢 Análise de Dados**: Aprofundar técnicas de exploração e visualização
- **☁️ Cloud Computing**: Deploy de modelos em ambientes escaláveis

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

## ⚖️ Ética e Governança em IA

Este módulo inclui materiais complementares sobre ética, governança e responsabilidade no desenvolvimento e uso de Inteligência Artificial.

### Princípios Éticos

- **[Princípios Fundamentais da Ética da IA da IBM](PRINCIPIOS%20FUNDAMENTAIS%20DA%20ETICA%20DA%20IA%20DA%20IBM.md)** — Os três princípios que orientam a abordagem da IBM: ampliar a inteligência humana, propriedade dos dados e transparência dos sistemas.
- **[Principais Princípios para Ética da IA](PRINCIPAIS%20PRINCIPIOS%20PARA%20ETICA%20DA%20IA.md)** — Princípios derivados do Relatório Belmont: respeito pelas pessoas, beneficência e justiça.
- **[Cinco Pilares para Guiar a Adoção de Tecnologias Ligadas a IA da IBM](CINCO%20PILARES%20PARA%20GUIAR%20A%20ADO%C3%87%C3%83O%20DE%20TECNOLOGIAS%20LIGADAS%20A%20IA%20DA%20IBM.md)** — Explicabilidade, imparcialidade, robustez, transparência e privacidade.

### Preocupações e Desafios

- **[Principais Preocupações da IA Hoje](PRINCIPAIS%20PREOCUPA%C3%87%C3%95ES%20DA%20IA%20HOJE.md)** — IA generativa, singularidade tecnológica, impacto nos empregos, privacidade, preconceito e prestação de contas.

### Governança e Organizações

- **[Governança de IA](GOVERNANCA.md)** — Melhores práticas de governança: dashboards, métricas, monitoramento automatizado, alertas e trilhas de auditoria.
- **[Organizações que Promovem Ética em IA](ORGANIZA%C3%87%C3%95ES%20QUE%20PROMOVEM%20ETICA%20EM%20IA.md)** — AlgorithmWatch, AI Now Institute, DARPA, CHAI e NASCAI.

---

## 📚 Recursos Adicionais

### Documentação Oficial
- [Documentação Oficial Pandas](https://pandas.pydata.org/docs/)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Dataset Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

### Comunidade e Suporte
- Participe de fóruns de Machine Learning
- Contribua com projetos open source
- Compartilhe seus aprendizados

---

*Este módulo foi criado para fins educacionais, demonstrando um fluxo completo de análise de dados e Machine Learning usando Pandas e técnicas modernas de IA.*
