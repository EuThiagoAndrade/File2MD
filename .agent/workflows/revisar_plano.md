---
description: Revisão crítica e refinamento do Plano de Implementação (V2.0) — segunda passagem (LLM revisora)
---

> [!IMPORTANT]
> **MODO ESTRITO**: Ao ser invocado por `@[/revisar_plano]`, o agente DEVE iniciar sua resposta com: *"Protocolo Revisor de Plano ativado."*. Em seguida, DEVE criar ou atualizar o arquivo `.agent/task.md` listando estas etapas como pendentes `[ ]`.

# Revisor Crítico de Plano de Implementação

Este workflow recebe um rascunho produzido pelo `@[/rascunhar_plano]`, aplica uma revisão crítica sistemática e entrega uma versão refinada e aprovável. O output é o **mesmo arquivo** atualizado em `.agent/plans/`, mais completo, preciso e sem ambiguidades.

> **Responsabilidade deste workflow:** questionar tudo, validar cada seção contra o codebase, e elevar a qualidade do plano ao nível de Source of Truth (SoT) válido para `@[/criar_issues]` e `@[/implementar_issue]`.

## Regras Gerais

- **Este workflow é somente crítica e refinamento.** Não cria issues, não abre PR, não altera código.
- **Não preserve o texto original por educação.** Se uma seção está errada ou imprecisa, reescreva-a.
- **Cite evidências para cada crítica.** Nunca diga "está errado" sem apontar a linha/função do script que contradiz o rascunho.
- Se encontrar um problema bloqueante (ex.: arquivo referenciado não existe, função descrita não corresponde ao código), **PARE** e reporte ao usuário antes de continuar.

---

## 0. Localização do Plano a Revisar

**a) Se o usuário indicou o arquivo:** leia diretamente o path informado.

**b) Se o usuário não indicou o arquivo:**
- Liste `.agent/plans/` e identifique o arquivo mais recente.
- Apresente ao usuário: *"Vou revisar o plano `.agent/plans/<nome>.md`. Confirme ou indique outro arquivo."*
- **Aguarde** confirmação antes de prosseguir.

**c) Leia o plano completo** antes de iniciar qualquer revisão.

---

## 1. Validação da Estrutura Mínima (Gate de SoT)

**Antes de validar o conteúdo, verifique a conformidade com o template oficial:**
- Leia `.agent/templates/plano_implementacao.md` integralmente.
- Compare as seções do rascunho com as seções do template.
- Se o rascunho tiver **seções a menos**: adicione-as na versão revisada.
- Se o rascunho tiver **seções que não existem no template**: questione o usuário.

Verifique se o plano atende à estrutura mínima exigida pelos workflows `criar_issues` e `implementar_issue`:

| Seção Obrigatória | Presente? | Válida? |
|---|---|---|
| `Objetivo` (seção clara, 1 frase de ação) | ✅/❌ | ✅/❌ |
| `Escopo` (✅ Dentro + ❌ Fora, ao menos 2 itens cada) | ✅/❌ | ✅/❌ |
| `Critérios de Aceite` (ao menos 1 por item técnico) | ✅/❌ | ✅/❌ |
| `Arquivos Afetados` (tabela consolidada) | ✅/❌ | ✅/❌ |
| `Decomposição em Issues` (tabela com tipo e prioridade) | ✅/❌ | ✅/❌ |
| `Sequência de Implementação` (ordem explícita) | ✅/❌ | ✅/❌ |

**Regra de bloqueio:**
- Se `Objetivo`, `Escopo` ou `Critérios de Aceite` estiverem ausentes ou vazios → **PARE**. Reporte ao usuário e aguarde correção antes de prosseguir com o restante da revisão.
- Se outras seções estiverem ausentes → registre como ⚠️ e continue, preenchendo-as na revisão.

---

## 2. Auditoria Técnica — Verificação contra o Codebase

Esta é a etapa mais crítica. Para cada item técnico do plano:

### 2.1 Validação de Existência de Arquivos e Funções
- [ ] O arquivo do script referenciado existe (ex: `Scripts/File2MD.py`)?
- [ ] A função/bloco mencionado no `**Contexto:**` existe no arquivo indicado?
- [ ] O comportamento atual descrito no contexto corresponde ao código real?
- **Método:** leia o trecho relevante do script no repositório e compare com o que o rascunho descreve.

### 2.2 Validação dos Exemplos de Código
- [ ] O código de exemplo no `**Ação Técnica:**` é compatível com os padrões de tipagem e padrões do projeto (ex: UTF-8 explícito, uso de Path)?
- [ ] Não introduz dependências novas sem declarar isso no escopo e no `requirements.txt`?
- **Falha:** código incompatível com padrões do projeto → reescreva com base no codebase real.

### 2.3 Validação de Cores e Estilos (Interface de Terminal)
- [ ] Caso altere painéis ou mensagens de console, os estilos e cores propostos batem com o `custom_theme` do script?

---

## 3. Auditoria de Completude

Verifique se o rascunho está completo o suficiente para ser usado como SoT:

### 3.1 Critérios de Aceite
- [ ] Cada item técnico tem **ao menos 2 critérios** verificáveis?
- [ ] Os critérios são objetivos? Exemplos de critérios inválidos:
  - ❌ "Funciona corretamente" → sem observabilidade
  - ❌ "Sem erros no console" → muito genérico
  - ✅ "O comando `python Scripts/File2MD.py -d pasta --ext msg` gera arquivos .md correspondentes e não falha em lote."
  - ✅ "A TUI exibe a opção 10 correspondendo à configuração de logs no menu principal."

### 3.2 Contexto por Item
- [ ] O `**Contexto:**` de cada item descreve o **estado atual do código**, não a solução?

### 3.3 Notas de "Não Alterar"
- [ ] Cada `**Ação Técnica:**` tem uma `**Nota:**` indicando o que **não deve ser tocado**? (Isso evita regressões e quebras colaterais em outras partes do script compartilhado).

---

## 4. Auditoria de Governança

### 4.1 Decomposição em Issues
- [ ] As issues são verdadeiramente atômicas (1 PR cada)?
- [ ] A coluna `Depende de` reflete corretamente a ordem da `Sequência de Implementação`?
- [ ] Os títulos de issue seguem a convenção `[FEATURE/FIX/CHORE] Verbo no infinitivo`?

### 4.2 Sequência de Implementação
- [ ] A ordem faz sentido técnico (core antes de UI)?
- [ ] O teste de fumaça do fluxo completo está descrito?

---

## 5. Montagem do Relatório de Revisão

Antes de apresentar o plano revisado, produza um **Relatório de Revisão** estruturado:

```
╔══════════════════════════════════════════════════════╗
║     RELATÓRIO DE REVISÃO — <NomePlano>.md           ║
╚══════════════════════════════════════════════════════╝

GATE DE SoT:             ✅ VÁLIDO | ❌ INVÁLIDO (seções ausentes: X, Y)
Itens técnicos revisados: N
Issues na decomposição:   N

CRÍTICAS ENCONTRADAS:
─────────────────────────────────────────────────
🔴 BLOQUEANTES (impedem uso como SoT):
  - [Item N] [descrição da crítica + evidência do codebase]

🟡 AVISOS (corrigidos na versão revisada):
  - [Item N] [descrição + o que foi corrigido]

🟢 APROVADOS SEM ALTERAÇÃO:
  - [Item N] — contexto, ação técnica e critérios estão corretos.

SEÇÕES ADICIONADAS (ausentes no rascunho):
  - [nome da seção]

ALTERAÇÕES NO CABEÇALHO:
  - Prioridade ajustada de X para Y (motivo)
  - Prioridade de Execução definida: Item A → Item B → Item C
─────────────────────────────────────────────────
VEREDITO: ✅ APROVADO PARA CRIAR ISSUES | ⚠️ APROVADO COM RESSALVAS | 🔴 REQUER NOVA RODADA
```

---

## 6. Apresentação do Plano Revisado e Barreira de Aprovação (Hard Stop)

**PAUSE a execução.**

Apresente:
1. O Relatório de Revisão (Passo 5) completo.
2. O plano revisado completo (em bloco de código markdown), com todas as correções aplicadas.

**Aguarde** aprovação explícita antes de salvar.
- Aprovações válidas: *"Aprovado"*, *"Pode salvar"*, *"Prosseguir"*.

---

## 7. Salvamento da Versão Revisada

Após aprovação:
1. Atualize o arquivo existente em `.agent/plans/<nome>.md` **localmente** usando a ferramenta de edição/escrita de arquivos do workspace.
2. **PROIBIDO** usar `create_or_update_file` ou `push_files` do MCP para salvar na branch padrão.
3. Altere o `**Status:**` do cabeçalho de `Rascunho` para `Em Revisão` (se aprovado com ressalvas) ou `Aprovado` (se aprovação plena).
4. Atualize a `**Última atualização:**` para a data atual.

---

## 8. Handoff para Criação de Issues

Após salvar a versão revisada, fornece o handoff explícito:
> "Para criar as issues deste plano, chame: `@[/criar_issues]`
> O agente irá ler `.agent/plans/<nome>.md` como SoT e usar a seção **Decomposição em Issues** como entrada."
