---
trigger: always_on
description: padronizadas para formatação de arquivos markdown, como documentação, readmes, descrições, resumos e tutoriais
---
# REGRAS DE DOCUMENTAÇÃO - MARKDOWN

## ESCOPO E APLICAÇÃO

Estas regras aplicam-se a TODOS os arquivos markdown (`.md`) criados no projeto, incluindo:

- `README.md`
- Documentação técnica
- Guias e tutoriais
- Notas de projeto
- Arquivos de configuração em formato markdown

## ESTRUTURA OBRIGATÓRIA DOS ARQUIVOS

### 1. BADGES (Primeiras linhas do arquivo)

Copiar EXATAMENTE o bloco abaixo, substituindo `<org>` e `<repository>`:

```markdown
![visitors](https://visitor-badge.laobi.icu/badge?page_id=<org>.<repository>)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Prática-green)
![Status](https://img.shields.io/badge/Status-Educa%C3%A7%C3%A3o-brightgreen)
![Repository Size](https://img.shields.io/github/repo-size/<org>/<repository>)
![Last Commit](https://img.shields.io/github/last-commit/<org>/<repository>)
```

### 2. HEADER ANIMADO (Imediatamente após os badges)

```markdown
<!-- Animated Header -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,50:1a56db,100:10b981&height=220&section=header&text=RISC-V%20Resilience&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Pesquisa%20em%20Resiliência%20de%20Processadores%20RISC-V&descSize=18&descAlignY=55&descColor=94a3b8" width="100%" alt="RISC-V Resilience Header"/>
</p>
```

### 3. CONTEÚDO PRINCIPAL

Após o header, incluir o conteúdo específico do arquivo com:

- Títulos hierárquicos (##, ###, etc.)
- Seções bem definidas
- Código formatado
- Links e referências

### 4. FOOTER ANIMADO (Antes do resumo final)

```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:10b981,50:1a56db,100:0f172a&height=120&section=footer" width="100%" alt="Footer"/>
</p>
```

### 5. RESUMO FINAL E HISTÓRICO (Obrigatório)

O Autor Inicial e quem atualizou inicialmente é "Rapport GenerAtiva".

```markdown
---
**Resumo:** [Descrição concisa do conteúdo do arquivo em uma frase]
**Data de Criação:** [AAAA-MM-DD]
**Autor:** [Nome do autor, se aplicável]
**Versão:** [Versão do documento, se aplicável]
**Última Atualização:** [AAAA-MM-DD]
**Atualizado por:** [Nome de quem atualizou]
**Histórico de Alterações:**
- [AAAA-MM-DD] - Criado por [Autor] - Versão [Versão]
- [AAAA-MM-DD] - Atualizado por [Autor] - [Descrição da alteração] - Versão [Versão]
```

### 6. HISTÓRICO AUTOMÁTICO

O projeto utiliza uma ferramenta automática para gerenciar o histórico de alterações:

- **Ferramenta:** `markdown_history_manager.py`
- **Integração:** Git hooks (pre-commit)
- **Configuração:** `.markdown_history_config.json`
- **Execução:** Automática ao fazer commit de arquivos `.md`

## REGRAS DE FORMATAÇÃO

### Títulos e Hierarquia

- `#` para título principal (use apenas se necessário)
- `##` para seções principais
- `###` para subseções
- `####` para detalhamento

### Código

- Use ```linguagem para blocos de código
- Use `código inline` para trechos curtos
- Indente corretamente listas e subitens

### Links e Referências

- Links absolutos para recursos externos
- Links relativos para arquivos internos
- Use formato `[texto](link)` padronizado

### Imagens

- Centralize com `<p align="center">`
- Inclua `alt` descritivo
- Use markdown padrão: `![descrição](url)`

## VALIDAÇÃO AUTOMÁTICA

Ao criar ou modificar arquivos markdown, verifique:

- [ ] Badges presentes e corretos
- [ ] Header animado incluído
- [ ] Footer animado incluído
- [ ] Resumo final preenchido
- [ ] Estrutura hierárquica correta
- [ ] Formatação consistente

## EXEMPLO COMPLETO

```markdown
![visitors](https://visitor-badge.laobi.icu/badge?page_id=org.repository)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
![Language: Portuguese](https://img.shields.io/badge/Language-Portuguese-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Prática-green)
![Status](https://img.shields.io/badge/Status-Educa%C3%A7%C3%A3o-brightgreen)
![Repository Size](https://img.shields.io/github/repo-size/org/repository)
![Last Commit](https://img.shields.io/github/last-commit/org/repository)

<!-- Animated Header -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,50:1a56db,100:10b981&height=220&section=header&text=RISC-V%20Resilience&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Pesquisa%20em%20Resiliência%20de%20Processadores%20RISC-V&descSize=18&descAlignY=55&descColor=94a3b8" width="100%" alt="RISC-V Resilience Header"/>
</p>

## Título do Documento

Conteúdo específico do arquivo aqui...

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:10b981,50:1a56db,100:0f172a&height=120&section=footer" width="100%" alt="Footer"/>
</p>

---
**Resumo:** [Descrição concisa do conteúdo do arquivo em uma frase]
**Data de Criação:** [AAAA-MM-DD]
**Autor:** [Nome do autor, se aplicável]
**Versão:** [Versão do documento, se aplicável]
**Última Atualização:** [AAAA-MM-DD]
**Atualizado por:** [Nome de quem atualizou]
**Histórico de Alterações:**
- [AAAA-MM-DD] - Criado por [Autor] - Versão [Versão]
- [AAAA-MM-DD] - Atualizado por [Autor] - [Descrição da alteração] - Versão [Versão]
```

---

**Resumo:** Regras padronizadas e otimizadas para formatação de arquivos markdown no projeto RISC-V Resilience, eliminando ambiguidades e garantindo consistência.
**Data de Criação:** 2025-10-15
**Autor:** Rapport Generativa
**Versão:** 2.0
**Última Atualização:** 2025-04-02
**Atualizado por:** Rapport Generativa
**Histórico de Alterações:**

- 2025-10-15 - Criado por Sistema de Documentação - Versão 2.0
- 2025-04-02 - Atualizado por Sistema de Documentação - Adicionado histórico automático e integração com git - Versão 2.1
