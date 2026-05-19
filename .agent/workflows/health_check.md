---
description: Verificação periódica de integridade do sistema de workflows, skills e documentação do agente
---

> [!IMPORTANT]
> **MODO ESTRITO**: Ao ser invocado por `@[/health_check]`, o agente DEVE iniciar sua resposta com: *"Protocolo Health Check ativado."*

# Health Check do Sistema de Agente

Verificação de integridade e sincronia entre workflows, skills, templates e documentos do File2MD. Execute periodicamente ou quando houver mudanças significativas no agente.

## Regras Gerais
- Este workflow é **somente leitura**: NÃO edite nenhum arquivo. Apenas diagnostique e reporte.
- O resultado é um relatório estruturado com status por seção.
- Se encontrar problemas, liste-os com severidade e sugira correções.

---

## 1. Integridade da Interface de Terminal (TUI) e Console

**Verificar:**
- [ ] O `custom_theme` existe no `Scripts/File2MD.py`?
- [ ] As diretrizes estéticas no `.agent/ai_behavior.md` (§8) citam o `custom_theme` e a biblioteca Rich corretamente?
- [ ] A skill `tui-designer.md` cita as cores e padrões estéticos corretos?
- [ ] A skill `feature-workflow.md` menciona a TUI e o Rich na seção correspondente?
- [ ] O workflow `implementar_issue.md` indica a skill `@tui-designer` para a camada visual?

---

## 2. Sincronia entre Workflows

**Consistência de passos:**
- [ ] `criar_issues.md` tem numeração sequencial de passos?
- [ ] `implementar_issue.md` tem numeração sequencial de passos?
- [ ] `atualizar_docs.md` tem numeração sequencial de passos?

**Referências cruzadas entre workflows:**
- [ ] `implementar_issue.md` referencia `@[/criar_issues]` no fallback de rastreabilidade?
- [ ] `criar_issues.md` menciona a seção `📋 Plano de Referência` que o `implementar_issue.md` espera encontrar?
- [ ] Todos os workflows referenciam `.agent/plans/` como diretório de planos?

**Consistência do protocolo SoT:**
- [ ] `criar_issues.md` e `implementar_issue.md` definem a mesma estrutura mínima para planos (`Objetivo`, `Escopo`, `Critérios de Aceite`)?
- [ ] A skill `python-cli-architect.md` referencia `.agent/plans/` como fonte de verdade?
- [ ] `criar_issues.md` e `implementar_issue.md` validam o `Status: Aprovado` antes de agir?
- [ ] `revisar_plano.md` e `rascunhar_plano.md` utilizam os status padronizados (`Rascunho`, `Em Revisão`, `Aprovado`)?
- [ ] `rascunhar_plano.md` e `revisar_plano.md` referenciam `.agent/templates/plano_implementacao.md` como leitura obrigatória?

---

## 3. Sincronia entre Skills

**Padrão "Regras de Ouro" — verificar que TODAS as skills seguem o mesmo formato:**
- [ ] `python-cli-architect.md` tem seção "REGRAS DE OURO" com standalone vs. orquestrado?
- [ ] `tui-designer.md` tem seção "REGRAS DE OURO" com standalone vs. orquestrado?
- [ ] `doc-updater.md` tem seção "REGRAS DE OURO" com standalone vs. orquestrado?
- [ ] `governance-check.md` tem seção "REGRAS DE OURO" com standalone vs. orquestrado?
- [ ] `feature-workflow.md` tem seção "REGRAS DE OURO" com standalone vs. orquestrado?

**Cadeia de handoff — verificar que cada skill sugere a próxima no modo standalone:**
- [ ] `python-cli-architect` → sugere `@tui-designer`?
- [ ] `tui-designer` → sugere `@doc-updater`?
- [ ] `doc-updater` → sugere `@governance-check`?
- [ ] `feature-workflow` → sugere `@python-cli-architect`?

**Consistência de outputs orquestrados — cada skill devolve um handoff estruturado?**
- [ ] `python-cli-architect` → handoff com: funções alteradas, flags CLI, dependências, testes?
- [ ] `tui-designer` → handoff com: elementos visuais, teclas, testes?
- [ ] `doc-updater` → handoff com: arquivos alterados, seções, verificação?
- [ ] `governance-check` → handoff com: STATUS, camadas, violações, recomendação?

---

## 4. Templates de Issue vs. Workflows

**Verificar que os templates em `.github/ISSUE_TEMPLATE/` cobrem os tipos esperados:**
- [ ] Existe template para `feature` (feature_request.yml)?
- [ ] Existe template para `fix` (bug_report.yml)?
- [ ] Existe template para `chore` (chore.yml)?

**Campos esperados pelos workflows:**
- [ ] Template `feature_request.yml` contém "Critérios de Aceite" e "Detalhamento Técnico / Arquitetura"?
- [ ] Template `bug_report.yml` contém "Descrição do bug", "Evidências" e "Severidade"?
- [ ] Template `chore.yml` contém "Objetivo", "Escopo" e "Impacto"?

---

## 5. Saúde da Pasta `.agent/plans/`

**Planos pendentes:**
- [ ] Listar todos os arquivos em `.agent/plans/` (excluindo `completed/`).
- [ ] Algum plano tem mais de **30 dias** sem issue associada? (stale ⚠️)
- [ ] Algum plano contém `#ID` no nome mas a issue correspondente está `closed`? (sugerir mover para `completed/`).

**Planos executados:**
- [ ] Listar arquivos em `.agent/plans/completed/`.
- [ ] Os planos em `completed/` possuem bloco de "Pós-Mortem"?

---

## 6. `ai_behavior.md` — Consistência

- [ ] A seção "Interface de Terminal (TUI) e Console" (§8) está alinhada com as instruções do `tui-designer.md`?
- [ ] A seção "Simplicidade Primeiro" não conflita com instruções de nenhuma skill?
- [ ] A seção "Mudanças Cirúrgicas" é compatível com a postura do `doc-updater.md`?

---

## 7. Documentação (`README.md`)

- [ ] A tabela de triggers do `implementar_issue.md` (passo 3.3) é idêntica à do `atualizar_docs.md` (passo 0)?
- [ ] A tabela de triggers do `doc-updater.md` é idêntica ou compatível com as anteriores?
- [ ] Os triggers apontam corretamente para o `README.md` do projeto File2MD?

---

# Formato do Relatório Final

Após completar todas as seções, apresente o relatório neste formato:

```
╔══════════════════════════════════════════╗
║        HEALTH CHECK — YYYY-MM-DD        ║
╚══════════════════════════════════════════╝

1. Interface de Terminal:  ✅ OK | ⚠️ N problemas
2. Sincronia Workflows:   ✅ OK | ⚠️ N problemas
3. Sincronia Skills:      ✅ OK | ⚠️ N problemas
4. Templates vs Workflows:✅ OK | ⚠️ N problemas
5. Pasta .agent/plans/:   ✅ OK | ⚠️ N problemas
6. ai_behavior.md:        ✅ OK | ⚠️ N problemas
7. Documentação (README): ✅ OK | ⚠️ N problemas

──────────────────────────────────────────
RESULTADO GERAL: ✅ SAUDÁVEL | ⚠️ ATENÇÃO (N itens) | 🔴 CRÍTICO (N itens)
──────────────────────────────────────────

DETALHAMENTO DE PROBLEMAS:
(listar cada problema com severidade, arquivo afetado e sugestão de correção)
```
