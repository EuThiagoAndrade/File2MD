# Plano de Implementação — Migrar Caminhos de Planos para backup/Plan/ e backup/Executados/

> **Status:** Rascunho
> **Data de criação:** 2026-05-19
> **Última atualização:** 2026-05-19
> **Autor:** Thiago Andrade
> **Tipo:** chore
> **Prioridade:** 🟠 P2
> **Prioridade de Execução:** Item 1 → Item 2 → Item 3 → Item 4

---

## 1. Rastreabilidade (Preenchido automaticamente)
- **Issues do GitHub:** #XX
- **Pull Request (PR):** #ZZ

---

## 2. Objetivo e Escopo

### 2.1 Objetivo
Migrar todas as referências de caminhos de planos de implementação de `.agent/plans/` e `.agent/plans/completed/` para `backup/Plan/` e `backup/Executados/` respectivamente, em toda a infraestrutura do agente inteligente (`.agent/`) e nos templates de issue (`.github/ISSUE_TEMPLATE/`), restaurando a organização de diretórios do projeto original (`Meus-Investimentos`).

### 2.2 Escopo
* **✅ Dentro do Escopo:**
  - Criação da pasta `backup/Executados/` no diretório raiz do projeto.
  - Atualização do arquivo `.agent/ai_behavior.md` para apontar para `backup/Plan/`.
  - Atualização de todos os 5 workflows em `.agent/workflows/` para usar os caminhos `backup/Plan/` e `backup/Executados/`.
  - Atualização da skill `.agent/skills/python-cli-architect/python-cli-architect.md` para referenciar `backup/Plan/`.
  - Atualização do template canônico `.agent/templates/plano_implementacao.md` para usar `backup/Plan/` nos exemplos.
  - Atualização de todos os 3 templates de issue em `.github/ISSUE_TEMPLATE/` para apontar o caminho do plano local para `backup/Plan/`.
* **❌ Fora do Escopo:**
  - Alterações nas regras ou lógica da ferramenta CLI/TUI (`Scripts/File2MD.py`).
  - Atualizações de documentação não relacionadas ao comportamento de IA e estrutura de planos.
  - Migração ou movimentação de planos já existentes na pasta `backup/Plan/`.
  - Alteração na estrutura ou campos do template canônico de plano (apenas os exemplos de caminho são atualizados).

---

## 3. Arquivos Afetados (Consolidado)

| Arquivo | Ação | Camada | Item(ns) | Ocorrências |
|---|---|---|---|---|
| `backup/Executados/` | Criar | Estrutura | Item 1 | — |
| `.agent/ai_behavior.md` | Modificar | Regras IA | Item 2 | 1 |
| `.agent/workflows/rascunhar_plano.md` | Modificar | Workflows | Item 3 | 6 |
| `.agent/workflows/revisar_plano.md` | Modificar | Workflows | Item 3 | 5 |
| `.agent/workflows/criar_issues.md` | Modificar | Workflows | Item 3 | 3 |
| `.agent/workflows/implementar_issue.md` | Modificar | Workflows | Item 3 | 5 |
| `.agent/workflows/health_check.md` | Modificar | Workflows | Item 3 | 6 |
| `.agent/skills/python-cli-architect/python-cli-architect.md` | Modificar | Skills | Item 3 | 2 |
| `.agent/templates/plano_implementacao.md` | Modificar | Templates | Item 3 | 0* |
| `.github/ISSUE_TEMPLATE/chore.yml` | Modificar | Templates | Item 4 | 1 |
| `.github/ISSUE_TEMPLATE/bug_report.yml` | Modificar | Templates | Item 4 | 1 |
| `.github/ISSUE_TEMPLATE/feature_request.yml` | Modificar | Templates | Item 4 | 1 |

> **Nota:** Coluna "Ocorrências" baseada em auditoria real do codebase (grep por `.agent/plans`). O template canônico (`plano_implementacao.md`) tem 0 ocorrências literais do path `.agent/plans/` mas seus exemplos de tabela devem ser verificados para coerência com o novo padrão.

---

## 4. Detalhamento Técnico por Item

### Item 1 — Criação da estrutura de pastas
**Contexto:**
A pasta `backup/` existe na raiz do workspace do File2MD mas contém apenas a subpasta `Plan/`. A subpasta `Executados/` está ausente e é necessária para que o workflow de implementação (`implementar_issue.md`, passo 7) arquive os planos concluídos.

**Ação Técnica:**
- Criar o diretório `backup/Executados/`.
- Garantir a presença de um arquivo marcador `.gitkeep` em `backup/Executados/.gitkeep` para que o Git versione o diretório vazio.
- **Nota:** NÃO criar subdiretórios adicionais dentro de `backup/`. NÃO mover ou renomear a pasta `backup/Plan/` existente.

**Arquivos afetados:**
- Novo diretório: `backup/Executados/`

**Critério de Aceite:**
- [ ] O diretório `backup/Executados/` existe na raiz do projeto.
- [ ] O arquivo `backup/Executados/.gitkeep` existe e é versionável pelo Git.

---

### Item 2 — Atualização do comportamento da IA
**Contexto:**
O arquivo `.agent/ai_behavior.md` é a base de comportamento estrito da IA e atualmente instrui o modelo a buscar o "Source of Truth" de planos locais em `.agent/plans/` (linha 59, seção §9).

**Ação Técnica:**
- Alterar a linha 59 de `.agent/ai_behavior.md`:
  - **De:** `O arquivo em .agent/plans/ é a autoridade máxima de implementação...`
  - **Para:** `O arquivo em backup/Plan/ é a autoridade máxima de implementação...`
- **Nota:** NÃO alterar nenhuma outra seção do `ai_behavior.md` (§1 a §8 e o restante de §9). Apenas a referência de path na linha 59 deve ser modificada.

**Arquivos afetados:** `.agent/ai_behavior.md` (1 alteração, ~1 linha)

**Critério de Aceite:**
- [ ] O arquivo `ai_behavior.md` não contém referências a `.agent/plans/`.
- [ ] A referência de rastreabilidade local aponta para `backup/Plan/`.
- [ ] O texto ao redor da alteração (sobre "autoridade máxima" e "plano Aprovado") permanece inalterado.

---

### Item 3 — Atualização de Workflows, Skills e Template Canônico
**Contexto:**
Os fluxos de trabalho (`rascunhar_plano.md`, `revisar_plano.md`, `criar_issues.md`, `implementar_issue.md` e `health_check.md`), a skill `python-cli-architect.md` e o template canônico `plano_implementacao.md` estão programados para ler, escrever e gerenciar arquivos de planos na pasta `.agent/plans/` e movê-los para `.agent/plans/completed/`. A auditoria identificou **28 ocorrências** do caminho legado distribuídas nesses 7 arquivos.

**Ação Técnica:**

**Regra de substituição (ordem obrigatória):**
1. **Primeiro**, substituir todas as ocorrências de `.agent/plans/completed/` por `backup/Executados/`.
2. **Depois**, substituir todas as ocorrências remanescentes de `.agent/plans/` por `backup/Plan/`.

> ⚠️ **ATENÇÃO:** A ordem é crítica: se a substituição de `.agent/plans/` for feita primeiro, o path `.agent/plans/completed/` será corrompido para `backup/Plan/completed/` ao invés de `backup/Executados/`.

**Detalhamento por arquivo:**

| Arquivo | Ocorrências `.agent/plans/` | Ocorrências `.agent/plans/completed/` |
|---|---|---|
| `rascunhar_plano.md` | 6 | 0 |
| `revisar_plano.md` | 5 | 0 |
| `criar_issues.md` | 3 | 0 |
| `implementar_issue.md` | 4 | 1 |
| `health_check.md` | 5 | 1 |
| `python-cli-architect.md` | 2 | 0 |
| `plano_implementacao.md` | 0* | 0 |

> *O template canônico não contém o path literal mas os exemplos na tabela de "Arquivos Afetados" referenciam caminhos genéricos. Para manter coerência, verificar se algum exemplo deveria ilustrar `backup/Plan/` como caminho padrão.

- **Nota:** NÃO alterar o conteúdo lógico, regras de negócio ou a ordem de passos de nenhum workflow ou skill. Apenas os caminhos de diretório devem ser atualizados. NÃO alterar instruções que mencionem `.agent/workflows/` ou `.agent/skills/` (esses diretórios continuam existindo).

**Arquivos afetados:**
- `.agent/workflows/rascunhar_plano.md` (6 substituições)
- `.agent/workflows/revisar_plano.md` (5 substituições)
- `.agent/workflows/criar_issues.md` (3 substituições)
- `.agent/workflows/implementar_issue.md` (5 substituições, incluindo 1 de `completed/`)
- `.agent/workflows/health_check.md` (6 substituições, incluindo 1 de `completed/`)
- `.agent/skills/python-cli-architect/python-cli-architect.md` (2 substituições)
- `.agent/templates/plano_implementacao.md` (verificação e ajuste se necessário)

**Critério de Aceite:**
- [ ] Nenhum arquivo do diretório `.agent` contém a string `.agent/plans/`.
- [ ] O workflow `health_check.md` valida a integridade da pasta `backup/Plan/` e `backup/Executados/` em vez de `.agent/plans/` e `.agent/plans/completed/`.
- [ ] O workflow `implementar_issue.md` (passo 7) instrui mover planos para `backup/Executados/` em vez de `.agent/plans/completed/`.
- [ ] O workflow `rascunhar_plano.md` instrui salvar novos planos em `backup/Plan/` em vez de `.agent/plans/`.
- [ ] O workflow `revisar_plano.md` instrui atualizar planos em `backup/Plan/` e referencia `backup/Plan/` no handoff para `criar_issues`.

---

### Item 4 — Atualização de Templates de Issue do GitHub
**Contexto:**
Os templates de issue `.github/ISSUE_TEMPLATE/chore.yml` (linha 50), `.github/ISSUE_TEMPLATE/bug_report.yml` (linha 45) e `.github/ISSUE_TEMPLATE/feature_request.yml` (linha 57) sugerem o caminho legado `.agent/plans/NomeDoPlano.md` como valor default para o campo `📋 Plano de Referência`.

**Ação Técnica:**
- Alterar o campo `value` da seção `reference_plan` em cada arquivo:
  - **De:** `Arquivo local: \`.agent/plans/NomeDoPlano.md\``
  - **Para:** `Arquivo local: \`backup/Plan/NomeDoPlano.md\``
- **Nota:** NÃO alterar nenhum outro campo dos templates (IDs, labels, validations, placeholders). Apenas o valor default do campo `reference_plan` deve ser modificado.

**Arquivos afetados:**
- `.github/ISSUE_TEMPLATE/chore.yml` (1 alteração, linha 50)
- `.github/ISSUE_TEMPLATE/bug_report.yml` (1 alteração, linha 45)
- `.github/ISSUE_TEMPLATE/feature_request.yml` (1 alteração, linha 57)

**Critério de Aceite:**
- [ ] Ao criar novas issues através dos templates do GitHub, o caminho sugerido por padrão para o plano de referência é `backup/Plan/NomeDoPlano.md`.
- [ ] Nenhum outro campo dos templates foi alterado (verificar via diff).

---

## 5. Governança e Roteiro de Entrega

### 5.1 Decomposição em Issues

| # | Título da Issue | Tipo | Prioridade | Depende de | Item(ns) do Plano |
|---|---|---|---|---|---|
| 1 | `[CHORE] Migrar caminhos de planos de .agent/plans/ para backup/Plan/ e backup/Executados/` | chore | 🟠 P2 | Nenhuma | Itens 1, 2, 3 e 4 |

### 5.2 Dependências e Blockers
Nenhuma dependência externa identificada.

### 5.3 Sequência de Implementação Recomendada
1. **Passo 1:** Criar a pasta `backup/Executados/` e o `.gitkeep` localmente.
2. **Passo 2:** Atualizar cirurgicamente o caminho de planos no `ai_behavior.md` (1 linha).
3. **Passo 3:** Realizar a substituição em lote dos paths nos workflows e skills, **respeitando a ordem**: primeiro `.agent/plans/completed/` → `backup/Executados/`, depois `.agent/plans/` → `backup/Plan/`.
4. **Passo 4:** Atualizar o caminho default de planos nos 3 templates de issue do GitHub em `.github/ISSUE_TEMPLATE/`.
5. **Passo 5 (Validação):** Executar busca global no workspace por `.agent/plans` para confirmar eliminação total do caminho legado. Apenas o plano `AdaptarFrameworkPlanos.md` em `backup/Plan/` deve conter essa string (como referência histórica).
6. **Passo 6 (Smoke Test):** Executar o workflow de health_check (`@[/health_check]`) para atestar o funcionamento correto do agente com a nova organização de planos.

### 5.4 Riscos e Suposições
* **Risco:** A substituição mecânica de `.agent/plans/` pode corromper o path `.agent/plans/completed/` se executada na ordem errada.
  * **Mitigação:** Substituir primeiro `.agent/plans/completed/` → `backup/Executados/`, depois `.agent/plans/` → `backup/Plan/`.
* **Risco:** Algum workflow externo ou customizado não coberto pelo plano pode falhar por ter o caminho codificado.
  * **Mitigação:** Auditoria pós-ajuste usando busca global por `.agent/plans` em todo o workspace.

### 5.5 Alternativas Consideradas
* **Alternativa A:** Manter os planos dentro da pasta `.agent/plans` e descartar a pasta `backup`.
  * *Motivo do descarte:* O usuário prefere manter a organização centralizada em `backup/Plan` e `backup/Executados` como no projeto original de investimentos, facilitando o gerenciamento visual fora da pasta oculta `.agent`.

### 5.6 Referências
- Histórico de adaptação da pasta `.agent` na Conversa `17d6e05d`.
- Conversa `99bc9264` — Refining Agentic Workflow Integration (auditoria prévia de paths).

---

## 6. Pós-Mortem (Preenchido automaticamente ao finalizar)
- **PR**: #XX
- **Data de conclusão**: YYYY-MM-DD
- **Desvios do plano**: [breve descrição ou "nenhum"]
- **Issues imprevistas durante execução**: [breve ou "nenhuma"]
