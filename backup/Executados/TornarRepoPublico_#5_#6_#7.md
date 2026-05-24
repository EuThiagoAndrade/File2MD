# Plano de Implementação — Tornar Repositório Público

> **Status:** Executado
> **Data de criação:** 2026-05-24
> **Última atualização:** 2026-05-24
> **Autor:** Thiago Andrade
> **Tipo:** chore
> **Prioridade:** 🟡 P3
> **Prioridade de Execução:** Item 1 → Item 2 → Item 3 → Item 4

---

## 1. Rastreabilidade (Preenchido automaticamente)
- **Issues do GitHub:** #XX, #YY
- **Pull Request (PR):** #ZZ

---

## 2. Objetivo e Escopo

### 2.1 Objetivo
Preparar o repositório File2MD para receber contribuições da comunidade de forma padronizada e segura, através da criação de guias de contribuição, código de conduta, templates de PR e automação de testes via CI/CD.

### 2.2 Escopo
* **✅ Dentro do Escopo:**
  - Criação de documento de diretrizes de contribuição (`CONTRIBUTING.md`).
  - Criação do Código de Conduta (`CODE_OF_CONDUCT.md`) usando o padrão Contributor Covenant v2.1.
  - Criação de template padronizado para Pull Requests.
  - Adição de workflow do GitHub Actions para testar PRs automaticamente usando `unittest`.
* **❌ Fora do Escopo:**
  - Refatoração de código existente do repositório.
  - Configuração manual das regras de proteção de branch (Branch Protection rules) diretamente na plataforma do GitHub (necessita de acesso Admin na interface web).

---

## 3. Arquivos Afetados (Consolidado)

| Arquivo | Ação | Camada | Item(ns) |
|---|---|---|---|
| `CONTRIBUTING.md` | Criar | Docs | Item 1 |
| `CODE_OF_CONDUCT.md` | Criar | Docs | Item 2 |
| `.github/PULL_REQUEST_TEMPLATE.md` | Criar | Docs | Item 3 |
| `.github/workflows/python-app.yml` | Criar | Config | Item 4 |

---

## 4. Detalhamento Técnico por Item

### 4.1 Item 1 — Documentação CONTRIBUTING.md

**Contexto:**
Para viabilizar a colaboração externa de forma fluida, a comunidade precisa de diretrizes de como configurar o ambiente local (`venv`), instalar as dependências (`requirements.txt`) e validar suas alterações rodando a suíte de testes (`test_file2md.py`) antes de abrir um PR.

**Ação Técnica:**
- Arquivo afetado: `CONTRIBUTING.md`
- Criar o documento detalhando o fluxo "Fork and Pull Request".
  ```markdown
  # Como Contribuir
  
  Obrigado pelo interesse em contribuir com o File2MD! Por favor, siga as instruções abaixo:
  
  1. Faça um Fork do repositório.
  2. Crie uma branch para suas alterações (`git checkout -b minha-feature`).
  3. Crie um ambiente virtual: `python -m venv venv`
  4. Ative o ambiente virtual e instale as dependências: `pip install -r requirements.txt`
  5. Para rodar os testes localmente antes de enviar um PR, execute:
     `python -m unittest discover -s Tests`
  6. Abra o Pull Request apontando para a branch `main`.
  ```
- **Nota:** Documento estritamente de texto; não afeta a lógica do script ou regras do console.

**Arquivos afetados:** `CONTRIBUTING.md` (1 alteração, ~30 linhas)

**Critério de Aceite:**
- [ ] O arquivo existe na raiz do repositório.
- [ ] O texto documenta claramente os comandos de criação de virtualenv, instalação de `requirements.txt` e execução de testes via `unittest`.

---

### 4.2 Item 2 — Código de Conduta

**Contexto:**
Para manter uma comunidade saudável e protegida de comportamentos inadequados, projetos públicos devem adotar um Código de Conduta. O padrão de mercado é o Contributor Covenant.

**Ação Técnica:**
- Arquivo afetado: `CODE_OF_CONDUCT.md`
- Criar o arquivo base utilizando o template Contributor Covenant v2.1.
- Configurar o e-mail oficial para denúncias.
  ```markdown
  # Código de Conduta do Contributor Covenant
  ...
  Instâncias de comportamento abusivo, de assédio, ou inaceitável de outra forma poderão
  ser reportadas à equipe do projeto em contato@euthiagoandrade.com.br.
  ...
  ```
- **Nota:** Não expor endereços de e-mail pessoais de terceiros sem autorização no arquivo.

**Arquivos afetados:** `CODE_OF_CONDUCT.md` (1 alteração, ~80 linhas)

**Critério de Aceite:**
- [ ] O arquivo contém o texto integral do Contributor Covenant.
- [ ] O e-mail de contato aponta exatamente para `contato@euthiagoandrade.com.br`.

---

### 4.3 Item 3 — Template de Pull Request

**Contexto:**
Necessitamos guiar os usuários para que preencham informações mínimas (como o resumo das alterações e o checklist de testes executados) toda vez que submeterem uma contribuição via Pull Request, padronizando a revisão de código.

**Ação Técnica:**
- Arquivo afetado: `.github/PULL_REQUEST_TEMPLATE.md`
- Criar o template padrão lido pelo GitHub ao abrir novos PRs.
  ```markdown
  ## Resumo das Mudanças
  [Descreva o que mudou e o impacto técnico das alterações]
  
  ## Issue Relacionada
  Fixes #
  
  ## Checklist
  - [ ] Testes locais rodaram com sucesso (`python -m unittest discover -s Tests`)
  - [ ] Documentação foi atualizada (se aplicável)
  ```
- **Nota:** Manter a compatibilidade com a pasta de templates de issue existente (`.github/ISSUE_TEMPLATE/`), sem alterar ou deletar os arquivos YAML existentes.

**Arquivos afetados:** `.github/PULL_REQUEST_TEMPLATE.md` (1 alteração, ~15 linhas)

**Critério de Aceite:**
- [ ] O arquivo encontra-se exatamente em `.github/PULL_REQUEST_TEMPLATE.md`.
- [ ] Possui seções estruturadas para Resumo, Issue e Checklist de conformidade.

---

### 4.4 Item 4 — Integração Contínua (GitHub Actions)

**Contexto:**
Garantir que a branch principal nunca seja quebrada por Pull Requests de terceiros. A suite de testes local (`Tests/test_file2md.py`) atualmente usa `unittest`. O pipeline rodará os testes a cada commit enviado para PR.

**Ação Técnica:**
- Arquivo afetado: `.github/workflows/python-app.yml`
- Implementar o YAML de workflow do GitHub Actions rodando nos eventos de `push` para `main` e em qualquer `pull_request` para `main`.
  ```yaml
  name: CI - File2MD Test Suite
  on:
    push:
      branches: [ "main" ]
    pull_request:
      branches: [ "main" ]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Test with unittest
        run: python -m unittest discover -s Tests
  ```
- **Nota:** O runner de CI do GitHub rodará em ambiente headless (Linux Ubuntu). Como a dependência `pyperclip` requer uma área de transferência do sistema, novos testes no futuro que chamem funções de clipboard devem implementar mocks ou instalar dependências X11 (`xclip` / `xsel`) para não quebrarem o pipeline. Atualmente, os testes de `test_file2md.py` não cobrem lógica de clipboard, portanto o teste passará limpo.

**Arquivos afetados:** `.github/workflows/python-app.yml` (1 alteração, ~25 linhas)

**Critério de Aceite:**
- [ ] O arquivo possui sintaxe YAML válida para o GitHub Actions.
- [ ] O pipeline executa com sucesso em testes manuais simulados (ambiente Python com instalação de dependências e unittest).

---

## 5. Governança e Roteiro de Entrega

### 5.1 Decomposição em Issues

| # | Título da Issue | Tipo | Prioridade | Depende de | Item(ns) do Plano |
|---|---|---|---|---|---|
| 1 | `[CHORE] Adicionar guia de contribuição e código de conduta` | chore | 🟡 P3 | Nenhuma | Item 1, Item 2 |
| 2 | `[CHORE] Criar template de Pull Request` | chore | 🟡 P3 | Nenhuma | Item 3 |
| 3 | `[CHORE] Configurar testes automatizados via GitHub Actions` | chore | 🟡 P3 | Nenhuma | Item 4 |

### 5.2 Dependências e Blockers
Nenhuma dependência identificada.

### 5.3 Sequência de Implementação Recomendada
1. **Passo 1:** Criar a documentação comunitária (`CONTRIBUTING.md` e `CODE_OF_CONDUCT.md`).
2. **Passo 2:** Configurar os templates da plataforma (`.github/PULL_REQUEST_TEMPLATE.md`).
3. **Passo 3:** Adicionar infraestrutura CI/CD (`.github/workflows/python-app.yml`).
4. **Passo 4:** Realizar simulação manual: Validar sintaxe local do GitHub actions e rodar os comandos localmente para verificar a estrutura de pastas.

### 5.4 Riscos e Suposições
* **Risco:** O framework de testes encontrar conflito de dependências caso o `requirements.txt` esteja defasado no futuro. -> **Mitigação:** Os contribuidores deverão seguir a recomendação de criação de ambiente virtual indicada no documento e o CI falhará alertando a incompatibilidade.

### 5.5 Alternativas Consideradas
* **Alternativa A:** Utilizar framework `pytest` e ignorar o `unittest`. Descartada, pois a suite de testes local (`Tests/test_file2md.py`) atualmente herda e usa primariamente o módulo `unittest` nativo. Manteremos a ferramenta nativa por simplicidade no workflow.

### 5.6 Referências
- Arquivo do Code of Conduct inspirado no [Contributor Covenant v2.1](https://www.contributor-covenant.org/).

---

## 6. Pós-Mortem (Preenchido progressivamente)
> *(Nota para o Agente: Cada PR associado a este plano deve adicionar um novo tópico principal aqui. Não sobrescreva PRs anteriores e NÃO concatene blocos inteiros novos com "## 6. Pós-Mortem" no fim do arquivo. Edite esta seção.)*

* **PR #8 (Issues #5, #6, #7):**
  - **Data de conclusão**: 2026-05-24
  - **Desvios do plano**: Nenhum. Os guias, templates e o CI/CD foram criados conforme planejado.
  - **Issues imprevistas**: Apenas a necessidade de obter o texto do Código de Conduta (Contributor Covenant v2.1) pt-br que deu 404 no download via bot. O arquivo foi fornecido pelo usuário e renomeado corretamente para caixa alta.
