---
description: Implementar uma issue do GitHub com branch, validação e Pull Request, usando MCP quando disponível e o workspace local quando necessário
---

> [!IMPORTANT]
> **MODO ESTRITO**: Ao ser invocado por `@[/implementar_issue]`, o agente DEVE iniciar sua resposta com: *"Protocolo Implementador ativado."*. Em seguida, DEVE criar ou atualizar o arquivo `.agent/task.md` listando as etapas principais deste workflow como pendentes `[ ]`.

# Implementador de Issues (Issue to PR)

Siga este workflow para transformar uma issue do GitHub em código funcional e validado no File2MD.

## Regras Gerais
- **NUNCA** realize alterações de código antes de concluir o diagnóstico inicial (passo 0) e registrar o planejamento no `task.md` (passo 1).
- O cumprimento deste workflow é validado acompanhando a checklist no `task.md`.
- Leia a issue inteira antes de codificar.
- Execute apenas as camadas necessárias (`core`, `tui`, `docs`).
- Quando este workflow estiver orquestrando outras skills, evite pausas intermediárias para confirmação humana. O checkpoint humano fica no fim, antes da abertura do PR.
- Se houver bloqueio explícito (dependência, issue prévia, credencial ou ambiente), pare e reporte antes de seguir.

---

## 0. Diagnóstico Inicial Obrigatório

**Ação Obrigatória:** Leia a issue via MCP do GitHub (`issue_read/get`) ou ferramenta equivalente local.

Extraia e registre:
- número, título, labels, assignees e links relacionados;
- tipo da issue: `feature`, `fix` ou `chore`.
- critérios de aceite, dependências, blockers, notas, evidências e referências.

**Auditoria de Planos Locais (Source of Truth):**
- Antes de prosseguir para o planejamento, o agente **DEVE** listar a pasta `.agent/plans/` buscando por arquivos que contenham o número da issue (`#<numero>`) ou palavras-chave do título.
- Se um plano for encontrado, ele deve ser lido integralmente e passará a ser a **Fonte da Verdade (SoT)** para todas as decisões técnicas subsequentes.
- **Fallback de rastreabilidade:** Se a busca por `#ID` em `.agent/plans/` não retornar resultados, verificar também o campo `📋 Plano de Referência` no corpo da issue (via MCP). Esse campo é inserido pelo workflow `@[/criar_issues]` e contém o path do plano original.

**Validação de Status e Sequência:**
- O agente **DEVE** verificar se o plano possui `Status: Aprovado`. Se estiver como `Rascunho`, recomende a revisão primeiro.
- A seção **"Sequência de Implementação Recomendada"** do plano deve ser transposta para o `task.md` como a ordem obrigatória de execução.
- **Ação Obrigatória**: Ao iniciar a implementação, atualize o `Status` no arquivo do plano para `Em Execução`.

---

## 1. Planejamento Executável

Antes de editar arquivos, produza um checklist curto de execução no `task.md` com:
- arquivos-alvo;
- camadas afetadas (`core`, `tui`, `docs`);
- itens obrigatórios e itens fora de escopo.

**Regra de Complexidade (ai_behavior.md §9):**
- Se a issue afetar **mais de 2 arquivos** e **não houver plano local** em `.agent/plans/`:
  **PARE** e sugira ao usuário: *"Esta issue afeta N arquivos. Recomendo criar um plano com `@[/rascunhar_plano]` antes de prosseguir."*
- Se o usuário autorizar prosseguir sem plano, registre o aviso no `task.md`.

---

## 2. Preparação do Ambiente

**Branch:** crie a branch a partir da branch padrão do repositório. Não presuma `main` sem verificar.

**Padrão de nomenclatura:**
- `feature/issue-<numero>`
- `fix/issue-<numero>`
- `chore/issue-<numero>`

---

## 3. Implementação Condicional por Camada

### 3.1 Python Core e CLI (API, lógica e regras)
Execute este bloco se a issue exigir alterações em lógica de conversão, tratamento de caminhos, configurações do JSON ou parâmetros do CLI.
- **Delegação sugerida:** acione `@python-cli-architect` em modo orquestrado.
- **Objetivo:** modificar apenas as funções e classes necessárias em `Scripts/File2MD.py`, preservando o padrão de tratamento do MarkItDown.

### 3.2 Terminal UI (TUI) (Visualização e menus)
Execute este bloco se a issue exigir painéis de console, spinners de progresso, navegação por teclado ou alterações no tema de exibição do Rich.
- **Delegação sugerida:** acione `@tui-designer` em modo orquestrado.
- **Objetivo:** alterar e testar apenas as funções visuais necessárias na TUI em `Scripts/File2MD.py`.

### 3.3 Documentação
**Acionamento obrigatório**: Este bloco DEVE ser executado em todo workflow. Avalie cada gatilho abaixo e registre o resultado no `task.md`:

| Gatilho | Arquivo(s) afetado(s) |
|---|---|
| Novo parâmetro CLI ou flag adicionada/modificada | `README.md` |
| Nova opção de menu visual na TUI | `README.md` |
| Nova biblioteca ou dependência adicionada/removida | `README.md` e `requirements.txt` |
| Alteração nas diretrizes de processos do agente | `.agent/ai_behavior.md` ou workflows |

- Se **algum** gatilho for ativado → acione `@doc-updater` em modo orquestrado.
- Se **nenhum** gatilho for ativado → registre explicitamente: `Documentação: nenhuma alteração necessária — [motivo]`.

---

## 4. Auditoria Obrigatória (Governance)

**Acionamento obrigatório:** acione `@governance-check` em modo orquestrado ao final de toda implementação, sem exceção — independentemente do tipo de issue ou das camadas alteradas.

**Declare o escopo ao acionar:** informe ao `@governance-check` quais camadas foram efetivamente alteradas nesta issue (conforme registrado no `task.md` no passo 1).

**Validação obrigatória mínima por camada:**
- Core alterado: executar testes automatizados em `Tests/` e registrar o resultado.
- TUI alterada: registrar um smoke test manual objetivo.
- Docs alteradas: conferir links, comandos e coerência com o projeto.
- Bugfix: confirmar que a falha relatada deixou de ocorrer no cenário coberto.

**Regra de bloqueio — obrigatória antes do passo 5:**
- Resultado **"Aprovado"** → registre o status no `task.md` e prossiga para o passo 5.
- Resultado **"Reprovado"** → **PARE**. Corrija todas as violações apontadas e acione `@governance-check` novamente antes de avançar.

---

## 5. Commit e Pull Request

**Commit:** use staging seletivo e uma mensagem coerente com o tipo da issue, por exemplo:
- `feat(issue-17): adiciona ...`
- `fix(issue-17): corrige ...`
- `chore(issue-17): ajusta ...`

**Ação Obrigatória:** abra o PR usando a integração GitHub/MCP sempre que disponível.

**O corpo do PR deve incluir:**
- fechamento da issue: `Closes #<numero>` ou `Resolves #<numero>`;
- resumo do que foi implementado e validações executadas;
- resultado do `@governance-check`: `STATUS: APROVADO` ou `STATUS: REPROVADO — justificativa aceita`;
- status do plano local: informar se o plano em `.agent/plans/` foi totalmente atendido.

---

## 6. Barreira de Aprovação do PR (Hard Stop)

PAUSE a execução. Apresente o link do PR (ou a intenção de criá-lo, caso aplicável) e um resumo curto.
- **Aguarde** o usuário confirmar expressamente (ex: "Aprovado", "Pode prosseguir") para dar o workflow como concluído.

---

## 7. Manutenção de Planos (Finalização)

Após a aprovação do usuário e conclusão da tarefa, o agente deve mover o arquivo de plano de `.agent/plans/` para `.agent/plans/completed/`, mantendo a pasta de pendências limpa.

**Pós-Mortem Automático:** Ao mover o plano para `completed/`, o agente **DEVE** adicionar um bloco de fechamento abaixo no final do arquivo:

```markdown
---
## Pós-Mortem (gerado automaticamente)
- **PR**: #XX
- **Data de conclusão**: YYYY-MM-DD
- **Desvios do plano**: [breve descrição ou "nenhum"]
- **Issues imprevistas durante execução**: [breve ou "nenhuma"]
```