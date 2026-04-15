![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=Softwares%20para%20An%C3%A1lise%20e%20Visualiza%C3%A7%C3%A3o%20de%20Dados%20-%20Linguagens&fontSize=40&fontAlignY=35&animation=twinkling)

# # Softwares para Análise e Visualização de Dados - Linguagens

![visitors](https://visitor-badge.laobi.icu/badge?page_id=ArvoreDosSaberes.Capacitacao_GemeosDigitais.LLMs.Softwares_Linguagens)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
![Educational](https://img.shields.io/badge/Type-Educational-green)
![Programming](https://img.shields.io/badge/Content-Programming%20Languages-orange)
![Status](https://img.shields.io/badge/Status-Reference-yellow)

Linguagens de programação e query sugeridas na aula de **Análise Exploratória (AED)** para análise, manipulação e visualização de dados.

---

## # 1. Python

**Descrição:** Linguagem de programação versátil e poderosa para análise de dados. Oferece ecossistema robusto com bibliotecas especializadas como NumPy (computação numérica), Pandas (manipulação de dados), Matplotlib/Seaborn (visualização), Scikit-learn (machine learning) e muitas outras. Sintaxe clara e intuitiva, ideal tanto para iniciantes quanto para especialistas.

- **Desenvolvedor:** Python Software Foundation
- **Plataforma:** Windows, macOS, Linux
- **Licença:** Open Source (Python Software Foundation License)
- **Site oficial:** <https://www.python.org/>
- **Download:** <https://www.python.org/downloads/>

### Bibliotecas Principais para Análise de Dados

| Biblioteca | Função | Link |
| --- | --- | --- |
| **NumPy** | Computação numérica | <https://numpy.org/> |
| **Pandas** | Manipulação de dados | <https://pandas.pydata.org/> |
| **Matplotlib** | Visualização básica | <https://matplotlib.org/> |
| **Seaborn** | Visualização estatística | <https://seaborn.pydata.org/> |
| **Plotly** | Visualização interativa | <https://plotly.com/python/> |
| **Scikit-learn** | Machine learning | <https://scikit-learn.org/> |
| **Jupyter** | Notebooks interativos | <https://jupyter.org/> |

### Instalação Rápida

```bash
# Instalar Python (recomendado usar Anaconda)
conda install numpy pandas matplotlib seaborn scikit-learn jupyter

# Ou com pip
pip install numpy pandas matplotlib seaborn scikit-learn jupyter
```

---

## # 2. R

**Descrição:** Linguagem estatística por excelência, desenvolvida especificamente para análise de dados e computação estatística. Oferece vasto conjunto de pacotes para praticamente todas as áreas da estatística, desde análise descritiva até modelagem complexa. Comunidade acadêmica muito ativa com milhares de pacotes disponíveis no CRAN.

- **Desenvolvedor:** R Core Team
- **Plataforma:** Windows, macOS, Linux
- **Licença:** Open Source (GPL)
- **Site oficial:** <https://www.r-project.org/>
- **Download (CRAN):** <https://cran.r-project.org/>

### Pacotes Principais para Análise de Dados

| Pacote | Função | Link |
| --- | --- | --- |
| **dplyr** | Manipulação de dados | <https://dplyr.tidyverse.org/> |
| **ggplot2** | Visualização | <https://ggplot2.tidyverse.org/> |
| **tidyr** | Organização de dados | <https://tidyr.tidyverse.org/> |
| **readr** | Importação de dados | <https://readr.tidyverse.org/> |
| **shiny** | Aplicações web interativas | <https://shiny.rstudio.com/> |
| **caret** | Machine learning | <https://topepo.github.io/caret/> |
| **knitr** | Documentos dinâmicos | <https://yihui.org/knitr/> |

### Instalação Rápida

```r
# Instalar pacotes básicos do tidyverse
install.packages("tidyverse")

# Ou pacotes individuais
install.packages(c("dplyr", "ggplot2", "tidyr", "readr"))
```

---

## # 3. SQL

**Descrição:** Linguagem de consulta estruturada para gerenciamento e análise de dados em bancos de dados relacionais. Fundamental para extração, filtragem, agregação e transformação de dados em larga escala. Suportada pela maioria dos sistemas de banco de dados, permitindo análise direta nos dados sem necessidade de exportação.

- **Desenvolvedor:** ISO/IEC (padrão internacional)
- **Plataforma:** Multiplataforma (depende do SGBD)
- **Licença:** Padrão aberto (implementações variam)
- **Documentação oficial:** <https://iso.org/standard/63555.html>

### Sistemas de Banco de Dados Populares

| Sistema | Tipo | Licença | Link |
| --- | --- | --- | --- |
| **PostgreSQL** | Relacional | Open Source | <https://www.postgresql.org/> |
| **MySQL** | Relacional | Open Source | <https://www.mysql.com/> |
| **SQLite** | Relacional (file-based) | Open Source | <https://www.sqlite.org/> |
| **Microsoft SQL Server** | Relacional | Comercial | <https://www.microsoft.com/sql-server> |
| **Oracle Database** | Relacional | Comercial | <https://www.oracle.com/database/> |

### Comandos SQL Essenciais para Análise

```sql
-- Seleção básica
SELECT coluna1, coluna2 FROM tabela WHERE condição;

-- Agregação
SELECT categoria, COUNT(*) as total, AVG(valor) as media 
FROM tabela 
GROUP BY categoria;

-- Junções
SELECT t1.coluna, t2.coluna 
FROM tabela1 t1 
JOIN tabela2 t2 ON t1.id = t2.id;

-- Subconsultas
SELECT * FROM tabela 
WHERE id IN (SELECT id FROM outra_tabela WHERE valor > 100);
```

---

## # Resumo Comparativo

| Linguagem | Tipo | Licença | Foco Principal | Ecossistema |
| --- | --- | --- | --- | --- |
| **Python** | Programação geral | Open Source | Versatilidade, ML | PyPI, Conda |
| **R** | Estatística | Open Source | Análise estatística | CRAN, Bioconductor |
| **SQL** | Query de banco | Padrão aberto | Manipulação de dados | Vários SGBDs |

---

## # Recomendações de Uso

### Para Iniciantes
- **Python** - Sintaxe mais amigável e vasta documentação
- **SQLite** - Banco de dados leve para começar com SQL

### Para Análise Estatística Avançada
- **R** - Ferramentas estatísticas mais completas
- **Python + Scikit-learn** - Machine learning moderno

### Para Grandes Volumes de Dados
- **SQL** - Processamento direto no banco
- **Python + Pandas** - Manipulação eficiente em memória

---

## # Informações do Documento

*Este documento apresenta linguagens de programação para análise e visualização de dados para a Capacitação em Gêmeos Digitais e 5G, pertencente ao repositório **Capacitacao_GemeosDigitais** da organização **ArvoreDosSaberes**.

**Repositório:** [Capacitacao_GemeosDigitais](https://github.com/ArvoreDosSaberes/Capacitacao_GemeosDigitais)  
**Organização:** [ArvoreDosSaberes](https://github.com/ArvoreDosSaberes)  
**Data de criação:** 2026  
**Licença:** CC BY-SA 4.0

![footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer&animation=twinkling)
