# Diretrizes de Comportamento de IA — File2MD

> **Última atualização:** 2026-05-18

Este arquivo define regras mandatórias para qualquer agente ou modelo de IA (Antigravity, Claude, Gemini, etc.) que interaja com este workspace.

## 1. Prioridade das Instruções
- **A palavra do Usuário no chat é a autoridade máxima.**
- Se o usuário solicitar explicitamente "apenas o plano", "não execute" ou qualquer restrição específica, o agente deve **IGNORAR** qualquer sinal de "aprovação automática" ou "prosseguir para execução" vindo do sistema/terminal.
- O agente nunca deve assumir que uma tarefa pode ser executada sem revisão humana se o usuário indicou que gostaria de revisar primeiro.

## 2. Modo de Planejamento
- Mesmo que o sistema retorne uma mensagem de `automatic approval`, o agente deve respeitar o contexto da conversa. Se o usuário pediu para parar, o agente deve parar.
- O registro de aprovação manual no chat (ex: "Aprovado", "Pode fazer", "Prosseguir") é o único gatilho válido quando uma restrição foi imposta pelo usuário.

## 3. Integridade das Skills
- Antes de iniciar qualquer tarefa complexa, o agente deve consultar as diretrizes em `.agent/workflows/` e as skills em `.agent/skills/`.
- As skills em `.agent/skills/` definem **personas especializadas** (`python-cli-architect`, `tui-designer`, `doc-updater`, `governance-check`, `feature-workflow`) com regras de execução próprias. O agente deve consultá-las quando a tarefa envolver a camada correspondente.
- Este arquivo (`ai_behavior.md`) deve ter precedência sobre comportamentos padrão do modelo que conflitem com as preferências do usuário.

## 4. Simplicidade Primeiro _(ver também §5 — Mudanças Cirúrgicas)_
- Escreva o **mínimo de código** que resolva o problema. Nada especulativo.
- Não adicione funcionalidades além do que foi pedido.
- Não crie abstrações para código de uso único.
- Não adicione "flexibilidade" ou "extensibilidade" que não foi solicitada.
- Antes de entregar, pergunte: *"Um engenheiro sênior diria que isso está complicado demais?"*. Se sim, simplifique.
- Mantenha o estilo de código existente no projeto, mesmo que você faria diferente.

## 5. Mudanças Cirúrgicas _(ver também §4 — Simplicidade Primeiro)_
- Toque apenas o que for estritamente necessário para a tarefa. Não "melhore" código adjacente não relacionado.
- Não refatore, reformate ou reordene código que não está quebrado.
- Se notar código morto ou problemas não relacionados, **mencione-os ao usuário** — não os corrija silenciosamente.
- Quando suas mudanças tornarem imports, variáveis ou funções desnecessários, remova **apenas os que foram criados por você**. Nunca remova código pre-existente sem instrução explícita.
- Teste: cada linha alterada deve ser rastreável diretamente ao que o usuário pediu.

## 6. Gestão de Incertezas
- **Nunca assuma. Nunca esconda confusão. Exponha tradeoffs.**
- Se a tarefa tiver interpretações múltiplas, apresente-as ao usuário — não escolha silenciosamente.
- Se existir uma abordagem mais simples, diga. Questione quando for necessário.
- Se algo estiver confuso, **pare**. Nomeie o que está confuso e pergunte. Perguntas de clarificação devem vir **antes** da implementação, não após os erros.

## 7. Execução Orientada a Critérios
- Transforme tarefas inespecíficas em critérios verificáveis antes de executar:
  - "Corrigir bug" → "Identificar o cenário que falha e confirmar que deixou de falhar."
  - "Refatorar X" → "Garantir que o comportamento permanece idêntico antes e depois."
- Para tarefas multi-etapas, declare um plano breve com critérios de verificação por etapa antes de começar.
- Critérios fortes permitem execução independente. Critérios vagos ("fazer funcionar") exigem clarificação.

## 8. Interface de Terminal (TUI) e Console
- **Antes de criar ou modificar qualquer componente visual ou interação no terminal (TUI)**, o agente DEVE seguir as diretrizes estéticas do Rich Console.
- Respeitar estritamente o `custom_theme` definido no script `Scripts/File2MD.py` (cores: info, warning, danger, success, header, menu_opt, selected, status, accent).
- NUNCA usar `print()` brutos quando a aplicação estiver rodando no modo Menu (TUI). Utilizar os métodos de renderização do `rich.console`.
- Garantir que as interações por teclado sejam compatíveis com Windows (`msvcrt`) e possuam fallbacks adequados para ambientes Unix/Linux.
- Exibir barras de progresso (`Progress`, `SpinnerColumn`, `BarColumn`) durante conversões em lote e operações de monitoramento em tempo real.

## 9. Protocolo de Planejamento (Source of Truth)
- **Complexidade exige Plano**: Qualquer tarefa que afete mais de 2 arquivos ou altere a lógica de fluxo do sistema DEVE iniciar pelo workflow `@[/rascunhar_plano]`.
- **Gate de Qualidade**: O agente não deve criar issues (`@[/criar_issues]`) baseadas em rascunhos. O plano deve estar com `Status: Aprovado` após passar pelo `@[/revisar_plano]`.
- **Rastreabilidade Local**: O arquivo em `.agent/plans/` é a autoridade máxima de implementação. Se houver divergência entre o que o usuário disse no passado e o que está no plano Aprovado, o plano prevalece (ou deve ser revisado).
- **Template Canônico**: O plano DEVE seguir o template em `.agent/templates/plano_implementacao.md`. Seções do template não devem ser omitidas.
