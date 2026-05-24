# Task Tracking — Tornar Repositório Público

> **Workflow:** `@[/implementar_issue]`
> **Iniciado em:** 2026-05-24 19:10
> **Issue relacionada:** #5, #6, #7

---

## Etapas

- [x] Passo 0 — Diagnóstico Inicial Obrigatório
- [x] Passo 1 — Planejamento Executável (Checklist de arquivos-alvo)
- [x] Passo 2 — Preparação do Ambiente (Branch e dependências)
- [x] Passo 3 — Implementação Condicional por Camada
  - [x] Item 1 — CONTRIBUTING.md e CODE_OF_CONDUCT.md
  - [x] Item 2 — PULL_REQUEST_TEMPLATE.md
  - [x] Item 3 — python-app.yml (CI/CD)
- [x] Passo 4 — Auditoria Obrigatória (Governance Check)
- [x] Passo 5 — Commit e Pull Request (Abertura de PR)
- [x] Passo 6 — Barreira de Aprovação do PR (Hard Stop)
- [x] Passo 7 — Manutenção de Planos (Finalização e Pós-Mortem)

---

## Notas

### Diagnóstico Inicial Obrigatório (Passo 0)

* **Issue #5**: `[CHORE] Adicionar guia de contribuição e código de conduta`
  - **Tipo**: `chore`
  - **Labels**: `chore`
  - **Link**: https://github.com/EuThiagoAndrade/File2MD/issues/5
  - **Critérios de Aceite**: 
    * Criar `CONTRIBUTING.md` na raiz com guia de ambiente virtual, instalação de dependências e execução de testes.
    * Criar `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1) com e-mail de denúncia `contato@euthiagoandrade.com.br`.
  - **Blockers/Dependências**: Nenhuma.

* **Issue #6**: `[CHORE] Criar template de Pull Request`
  - **Tipo**: `chore`
  - **Labels**: `chore`
  - **Link**: https://github.com/EuThiagoAndrade/File2MD/issues/6
  - **Critérios de Aceite**:
    * Criar `.github/PULL_REQUEST_TEMPLATE.md` com seções de Resumo, Issue relacionada (Fixes #) e checklist de testes e documentação.
  - **Blockers/Dependências**: Nenhuma.

* **Issue #7**: `[CHORE] Configurar testes automatizados via GitHub Actions`
  - **Tipo**: `chore`
  - **Labels**: `chore`
  - **Link**: https://github.com/EuThiagoAndrade/File2MD/issues/7
  - **Critérios de Aceite**:
    * Criar `.github/workflows/python-app.yml` configurando CI via GitHub Actions para rodar a suíte `unittest` no push/PR para a branch `main`.
  - **Blockers/Dependências**: Nenhuma.

### Planejamento Executável (Passo 1)

* **Arquivos-alvo e Camadas**:
  - `CONTRIBUTING.md` (Camada: Docs)
  - `CODE_OF_CONDUCT.md` (Camada: Docs)
  - `.github/PULL_REQUEST_TEMPLATE.md` (Camada: Docs)
  - `.github/workflows/python-app.yml` (Camada: Config / CI/CD)
* **Itens Obrigatórios (Escopo)**:
  - Guia de contribuição na raiz.
  - Código de conduta usando Contributor Covenant v2.1 com e-mail de denúncia `contato@euthiagoandrade.com.br`.
  - Template de PR para o GitHub.
  - Workflow GitHub Actions rodando `unittest` em pushes e PRs para a branch `main`.
* **Itens Fora de Escopo**:
  - Alterações no código Python do File2MD.
  - Testes do TUI no pipeline CI Headless.
  - Alteração ou exclusão dos templates de issue pré-existentes.

### Preparação do Ambiente (Passo 2)

* **Branch Criada**: `chore/issue-5` (a partir da branch padrão `main`).
* **Verificação de dependências**: Dependências em `requirements.txt` válidas e intocadas.

### Implementação por Camada (Passo 3)

* **Documentação**:
  - `CONTRIBUTING.md` criado na raiz com fluxo de fork, venv, dependências e `unittest`.
  - `CODE_OF_CONDUCT.md` criado na raiz com e-mail de contato `contato@euthiagoandrade.com.br`.
  - `.github/PULL_REQUEST_TEMPLATE.md` criado com campos de resumo e checklists.
* **Configuração / CI-CD**:
  - `.github/workflows/python-app.yml` criado contendo pipeline de testes automatizados com Python 3.x e `unittest` sob Ubuntu-latest.

### Auditoria Obrigatória (Passo 4)

* **Escopo Declarado**: Alterações efetuadas nas camadas de documentação (`Docs`) e CI/CD (`Config`).
* **Validações Efetuadas**:
  - Execução de testes locais: executado `python -m unittest discover -s Tests` com sucesso (**8 testes executados - OK**).
  - Validação de e-mails/links: e-mail de denúncia `contato@euthiagoandrade.com.br` verificado em `CODE_OF_CONDUCT.md`.
  - Validação sintática do pipeline: sintaxe do workflow `.github/workflows/python-app.yml` validada com sucesso.
* **Resultado da Auditoria**: **APROVADO**.

### Commit e Pull Request (Passo 5)

* **Commit Efetuado**: `chore(issue-5): adiciona guias de contribuicao, conduta, templates de PR e workflow de CI` (hash `0d81f6b`).
* **Pull Request Criado**: PR #8.
  - **Link**: https://github.com/EuThiagoAndrade/File2MD/pull/8
  - **Issues Fechadas**: #5, #6, #7

---

## Resultado

> _Preenchido ao final da execução._
> **Status:** Concluído
> **Resumo:** Implementação completa da preparação do repositório para abertura pública. Foram criados os arquivos CONTRIBUTING.md, CODE_OF_CONDUCT.md (v2.1 em português), .github/PULL_REQUEST_TEMPLATE.md e o workflow .github/workflows/python-app.yml. O Pull Request #8 foi gerado, aprovado pelo usuário, e fundido (squash merge) fechando as issues #5, #6 e #7. O plano de implementação local foi atualizado com o pós-mortem e movido para a pasta de executados.
