# Task Tracking — Implementar Issue #14

> **Workflow:** `@[/implementar_issue]`
> **Iniciado em:** 2026-05-26 13:45
> **Issue relacionada:** #14

---

## Etapas

- [x] Passo 0 — Diagnóstico Inicial e Auditoria de Planos Locais (SoT)
- [x] Passo 1 — Planejamento Executável (Checklist de Arquivos e Escopo)
- [x] Passo 2 — Preparação do Ambiente (Criar Branch `chore/issue-14`)
- [x] Passo 3 — Implementação (Limpar e adaptar `File2MD.py` para entrypoint mínimo)
- [x] Passo 4 — Auditoria Obrigatória (`@governance-check`)
- [x] Passo 5 — Commit e Pull Request da Issue 14
- [x] Passo 6 — Barreira de Aprovação (Confirmação Humana)
- [x] Passo 7 — Manutenção de Planos (Ciclo de vida e Pós-Mortem)

---

## Notas

### Planejamento Executável (Issue #14)
* **Arquivos-alvo:**
  * `Scripts/File2MD.py` [MODIFY] (Modificado)
* **Camadas afetadas:** Entrypoint (Core e UI)
* **Itens obrigatórios:**
  * Limpar todo o código monolítico original migrado de `File2MD.py` (reduzindo de ~700 para ~60 lines).
  * Importar e instanciar `ConfigManager`, `I18nService`, `ConverterService` e `MenuApp`.
  * Integrar o loop de linha de comando (`argparse`) com os novos pacotes sem alterar as flags existentes (`input`, `-o`/`--output`, `-d`/`--directory`, `--watch`, `--keep-header`).
* **Itens fora de escopo:**
  * Renomeação ou modificação das flags originais do `argparse`.

### Relatório de Governança (@governance-check)
```
STATUS: APROVADO
Camadas auditadas: geral | core | tui
Itens aprovados:
  - Redução cirúrgica do File2MD.py para ~65 linhas.
  - Implementação de fachadas de compatibilidade para manter compatibilidade retroativa total com testes legados.
  - Remoção completa de imports não utilizados e lógicas de negócios duplicadas.
  - Todos os 14 testes da suíte passam com 100% de sucesso.
Violações: nenhuma
Recomendação: Pode abrir PR
```

---

## Resultado

> _Preenchido ao final da execução._
> **Status:** Concluído
> **Resumo:** O monolito `File2MD.py` foi reduzido com sucesso para cerca de 65 linhas. Fachadas de compatibilidade foram implementadas de forma a garantir que toda a suíte de testes unitários passasse sem quebras. PR #17 aberto no GitHub.
