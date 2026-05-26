# Task Tracking — Implementar Issue #13

> **Workflow:** `@[/implementar_issue]`
> **Iniciado em:** 2026-05-26 13:25
> **Issue relacionada:** #13

---

## Etapas

- [x] Passo 0 — Diagnóstico Inicial e Auditoria de Planos Locais (SoT)
- [x] Passo 1 — Planejamento Executável (Checklist de Arquivos e Escopo)
- [x] Passo 2 — Preparação do Ambiente (Criar Branch `feature/issue-13`)
- [x] Passo 3 — Implementação (Criar pacote `ui`, migrar componentes de UI e loop de menus)
- [x] Passo 4 — Auditoria Obrigatória (`@governance-check`)
- [/] Passo 5 — Commit e Pull Request da Issue 13
- [ ] Passo 6 — Barreira de Aprovação (Confirmação Humana)
- [ ] Passo 7 — Manutenção de Planos (Ciclo de vida e Pós-Mortem)

---

## Notas

### Planejamento Executável (Issue #13)
* **Arquivos-alvo:**
  * `Scripts/ui/__init__.py` [NEW] (Criado)
  * `Scripts/ui/components.py` [NEW] (Criado)
  * `Scripts/ui/menus.py` [NEW] (Criado)
* **Camadas afetadas:** UI / TUI
* **Itens obrigatórios:**
  * Migrar `custom_theme`, `console` (como Singleton), `draw_header`, `draw_status_bar` e banner ASCII para `ui/components.py`.
  * Criar classe `MenuApp` em `ui/menus.py` com `show_main_menu` e `show_settings_menu`.
  * O menu principal deve mostrar as 7 opções de ação (e a opção de configurações).
  * O submenu de configurações deve conter as 4 opções de setup (IA, YAML, pasta de saída, idioma).
  * Manter a navegação ↑↓ e Enter e o fallback para UNIX/Linux.
* **Itens fora de escopo:**
  * Modificações no esquema de cores ou layout visual do Rich.
  * Integração CLI ou remoção do código monolítico original do `File2MD.py`.

### Relatório de Governança (@governance-check)
```
STATUS: APROVADO
Camadas auditadas: geral | tui
Itens aprovados:
  - Criação da pasta de UI e do Singleton Console em components.py.
  - Implementação da navegação interactiva msvcrt e fallback UNIX na classe MenuApp.
  - Divisão de responsabilidade com loops separados para Menu Principal (ações) e Submenu (configuração).
  - Todas as chamadas usam Console do Rich com o tema customizado.
Violações: nenhuma
Recomendação: Pode abrir PR
```

---

## Resultado

> _Preenchido ao final da execução._
> **Status:** Em Execução
> **Resumo:** [breve resumo do que foi feito]
