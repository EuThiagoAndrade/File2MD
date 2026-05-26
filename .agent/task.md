# Task Tracking — Implementar Issue #12

> **Workflow:** `@[/implementar_issue]`
> **Iniciado em:** 2026-05-26 12:50
> **Issue relacionada:** #12

---

## Etapas

- [x] Passo 0 — Diagnóstico Inicial e Auditoria de Planos Locais (SoT)
- [x] Passo 1 — Planejamento Executável (Checklist de Arquivos e Escopo)
- [x] Passo 2 — Preparação do Ambiente (Criar Branch `chore/issue-12`)
- [x] Passo 3 — Implementação (Criar pacotes `core` e `utils`, extrair lógicas de `File2MD.py`)
- [x] Passo 4 — Auditoria Obrigatória (`@governance-check`)
- [x] Passo 5 — Commit e Pull Request da Issue 12
- [/] Passo 6 — Barreira de Aprovação (Confirmação Humana)
- [ ] Passo 7 — Manutenção de Planos (Ciclo de vida e Pós-Mortem)

---

## Notas

### Planejamento Executável (Issue #12)
* **Arquivos-alvo:**
  * `Scripts/core/__init__.py` [NEW] (Criado)
  * `Scripts/core/converter.py` [NEW] (Criado)
  * `Scripts/core/watcher.py` [NEW] (Criado)
  * `Scripts/core/postprocess.py` [NEW] (Criado)
  * `Scripts/utils/__init__.py` [NEW] (Criado)
  * `Scripts/utils/config_manager.py` [NEW] (Criado)
  * `Scripts/utils/i18n.py` [NEW] (Criado)
* **Camadas afetadas:** Core Python, Utilitários.
* **Itens obrigatórios:**
  * Criar classes especialistas mantendo a lógica de conversão, tratamento de caminhos, tratamento i18n e configurações JSON.
  * Preservar o padrão do MarkItDown.
  * Remover imports não utilizados (ex: `ProcessPoolExecutor`).
* **Itens fora de escopo:**
  * Alteração da UI/menus ou limpeza final do `File2MD.py`.
  * Modificação das regras de negócio de conversão ou comportamento de pós-processamento.

### Relatório de Governança (@governance-check)
```
STATUS: APROVADO
Camadas auditadas: geral | core
Itens aprovados: 
  - Codificação em UTF-8 obrigatória e explícita ao abrir e salvar arquivos.
  - Ausência de credenciais hardcoded.
  - Separação em classes e injeção de dependências do Rich Console, I18nService e ConfigManager.
  - BoundedSemaphore(4) utilizado para concorrência de threads.
  - Testes unitários para nova estrutura criados e executados com 100% de sucesso.
Violações: nenhuma
Recomendação: Pode abrir PR
```

---

## Resultado

> _Preenchido ao final da execução._
> **Status:** Em Execução (Aguardando Aprovação do PR #15)
> **Resumo:** Extraídos com sucesso os módulos de core (`converter`, `watcher`, `postprocess`) e utils (`config_manager`, `i18n`) do monolito, organizando-os em pacotes e adicionando testes de unidade robustos. PR #15 aberto no GitHub.
