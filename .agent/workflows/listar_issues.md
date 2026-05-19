---
description: Como acessar e listar issues do GitHub via MCP Store do Antigravity
---

> [!IMPORTANT]
> **MODO ESTRITO**: Ao ser invocado por `@[/listar_issues]`, o agente DEVE iniciar sua resposta com: *"Protocolo Listador de Issues ativado."*

# Listador de Issues do GitHub

Sempre que o usuário solicitar acesso ou listagem de issues do GitHub, siga este workflow:

## 1. Verifique a disponibilidade do MCP
- Confirme que o servidor GitHub esta instalado e habilitado no MCP Store do Antigravity para o agente atual.
- Confirme que a autorizacao do GitHub ja foi concluida dentro do Antigravity.
- Se o usuario estiver consultando um repositorio privado, confira silenciosamente owner e repo antes de concluir que o MCP falhou.

## 2. Utilize as ferramentas MCP do GitHub
- Voce DEVE utilizar as ferramentas nativas expostas pelo servidor GitHub instalado via MCP Store do Antigravity.
- PROIBIDO: usar terminal, scripts HTTP manuais ou a CLI do GitHub (`gh`) para listar ou buscar issues quando o MCP estiver disponivel.

## 3. Adapte a busca
- Para listar todas as issues, nao limite o estado, a menos que o usuario tenha pedido um filtro.
- Para listar apenas issues abertas, filtre por `open`.
- Para buscar uma issue especifica, use a ferramenta apropriada com o numero da issue.

## 4. Listagem e avaliação
- Liste as issues retornadas pelo MCP para o usuário.
- Se a lista vier vazia, confira silenciosamente owner, repo e filtros antes de concluir que não há resultados.
- **Formato de saída preferencial** (quando aplicável):

| # | Título | Labels | Status | Assignees |
|---|---|---|---|---|
| N | Título da issue | label1, label2 | open/closed | user1 |

## 5. Recuperacao em caso de falha
- Se o MCP do GitHub falhar, primeiro verifique se o servidor GitHub continua instalado, ativo e autorizado no MCP Store do Antigravity.
- Se a falha persistir, informe ao usuario que o ajuste deve ser feito na configuracao do MCP Store, nao no repositorio.
- Nao reintroduza configuracoes locais antigas como fallback padrao.
