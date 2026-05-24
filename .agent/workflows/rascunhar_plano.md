---
description: Preencher o Template de Plano de Implementação (V2.0) a partir de uma demanda do usuário — primeira passagem (LLM rascunhadora)
---

> [!IMPORTANT]
> **MODO ESTRITO**: Ao ser invocado por `@[/rascunhar_plano]`, o agente DEVE iniciar sua resposta com: *"Protocolo Rascunhador de Plano ativado."*. Em seguida, DEVE criar ou atualizar o arquivo `.agent/task.md` listando estas etapas como pendentes `[ ]`.

# Rascunhador de Plano de Implementação

Este workflow preenche o **Template V2.0** com base em uma demanda informada pelo usuário. O resultado é um rascunho em `backup/Plan/` pronto para ser revisado pelo workflow `@[/revisar_plano]`.

> **Responsabilidade deste workflow:** produzir um rascunho completo e estruturado. A crítica de qualidade é responsabilidade exclusiva do `@[/revisar_plano]`. Não tente corrigir o que você escreveu — escreva o melhor rascunho possível e pare.

## Regras Gerais

- **NUNCA** salve o arquivo sem apresentar o rascunho completo ao usuário primeiro (Passo 5).
- Este workflow **não cria issues e não abre PR**. Seu único output é um arquivo `.md` em `backup/Plan/`.
- Se a demanda for vaga demais para preencher o Passo 3 com segurança, **PARE** e faça perguntas de clarificação antes de continuar.
- **PROIBIDO** inventar arquivos, funções ou comportamentos que não existam no codebase atual.

---

## 0. Leitura de Contexto (Obrigatório)

Antes de qualquer escrita, colete o contexto necessário:

**a) Leia a demanda do usuário:**
- Extraia: qual problema resolve, qual área do script afeta, qual o resultado esperado.
- Classifique o tipo: `feature` | `fix` | `chore`.
- Classifique a prioridade inicial: `🔴 P1` | `🟠 P2` | `🟡 P3` | `🟢 P4`.

**b) Verifique se já existe um plano relacionado:**
- Liste `backup/Plan/` buscando planos com palavras-chave da demanda.
- Se existir plano relacionado, leia-o e use-o como contexto adicional — **nunca duplique** um plano existente sem motivo.

**c) Leia os arquivos relevantes do codebase:**
- Identifique quais partes do script `Scripts/File2MD.py` serão afetadas.
- Leia ao menos a função/bloco relevante para entender o estado atual.
- **PROIBIDO** preencher "Ação Técnica" sem ter lido o código que será alterado.

**d) Leia a TUI/Design System do console (somente se a demanda afetar console):**
- Verifique o `custom_theme` em `Scripts/File2MD.py`.
- **PROIBIDO** inventar tokens de cor que não estejam definidos no tema do script.

**e) Leia o template oficial do plano (Leitura Obrigatória):**
- Abra e leia `.agent/templates/plano_implementacao.md` integralmente.
- Este arquivo é a **estrutura canônica** que DEVE ser seguida para o preenchimento.

---

## 1. Nomeação do Arquivo

Defina o nome do arquivo de saída seguindo a convenção:

```
backup/Plan/<NomeCurtoDescritivo>.md
```

**Regras de nomenclatura:**
- PascalCase sem espaços: `SuporteLoteMsg.md`, `WatcherFiltros.md`
- Máximo 4 palavras.
- Sem prefixos de tipo (`feature_`, `fix_`) — o tipo fica dentro do plano.
- Sem números no nome inicial — o número da issue será adicionado **pelo workflow `criar_issues`** após a criação.

---

## 2. Preenchimento do Cabeçalho

Preencha o cabeçalho do template:

```markdown
# Plano de Implementação — [TÍTULO CLARO E OBJETIVO]

> **Status:** Rascunho
> **Data de criação:** YYYY-MM-DD
> **Última atualização:** YYYY-MM-DD
> **Autor:** Thiago Andrade
> **Tipo:** feature | fix | chore
> **Prioridade:** 🔴 P1 | 🟠 P2 | 🟡 P3 | 🟢 P4
> **Prioridade de Execução:** Item X → Item Y → Item Z
```

**Regras:**
- O título deve ser uma frase de ação clara: *"Adicionar Conversão de Arquivos MSG no Lote"*, não *"Melhorias no script"*.
- A `Prioridade de Execução` só pode ser preenchida após o Passo 4 (quando os itens já foram definidos).
- Se a ordem de execução não for clara ainda, deixe como `A definir` e retorne a esta linha no final.

---

## 3. Preenchimento das Seções Estruturais

**Regra sobre seções automáticas:**
- Seções marcadas como "Preenchido automaticamente" no template (Rastreabilidade, Pós-Mortem) devem ser incluídas no rascunho com seus placeholders originais — **NÃO omitir.**

### 3.1 Objetivo
- Uma frase única: QUÊ será feito + POR QUÊ é necessário agora.
- Se houver funcionalidade adjacente que **não existe** e está **fora do escopo**, documente com a nota:
  > **Nota de Escopo Negativo:** A funcionalidade de X **não existe** e está fora do escopo. Caso desejada futuramente, deve ser planejada como issue separada.

### 3.2 Escopo
- Liste ao menos 2 itens em cada categoria (✅ Dentro / ❌ Fora).

### 3.3 Arquivos Afetados (Consolidado)
- Preencha a tabela com **todos** os arquivos identificados no Passo 0c.
- Colunas: `Arquivo`, `Ação` (Criar / Modificar / Remover / Atualizar), `Camada` (Lógica Core / CLI / TUI / Docs / Tests), `Item(ns)`.

---

## 4. Preenchimento dos Itens Técnicos

Para **cada item técnico** do plano, preencha o bloco completo:

```markdown
### 4.X Item N — [Nome da Função ou Módulo Principal]

**Contexto:** [Por que esta alteração é necessária? Qual o problema atual?
Seja específico: mencione nome de função, linha aproximada, comportamento atual vs. esperado.]

**Ação Técnica:**
- Arquivo afetado: `Scripts/File2MD.py` _(função/linha relevante)_
- [Descrição da alteração — use verbos no infinitivo: "Alterar tratamento de X para Y"]
  ```python
  # código real baseado no codebase lido no Passo 0c
  # não use placeholders como `# seu código aqui`
  ```
- **Nota:** [O que NÃO deve ser alterado neste arquivo. Efeito colateral esperado, se houver.]

**Arquivos afetados:** `Scripts/File2MD.py` (N alterações, ~X linhas)

**Critério de Aceite:**
- [ ] [Condição objetiva e testável — sem "funciona corretamente"]
- [ ] [Nenhuma regressão em X]
- [ ] [Comportamento esperado em Y após a mudança]
```

**Regras por item:**
- O `**Contexto:**` deve explicar o estado atual do código, não a solução.
- O código de exemplo deve ser real.
- Cada item deve ter **ao menos 2 critérios de aceite** verificáveis.

---

## 5. Preenchimento das Seções de Governança

### 5.1 Decomposição em Issues

Monte a tabela de issues a serem criadas pelo `@[/criar_issues]`:

| # | Título da Issue | Tipo | Prioridade | Depende de | Item(ns) do Plano |
|---|---|---|---|---|---|

**Regras:**
- Cada issue deve ser atômica: 1 PR independente.
- Títulos seguem a convenção: `[FEATURE]`, `[FIX]`, `[CHORE]` + verbo no infinitivo.

### 5.2 Dependências e Blockers
- Se não houver: escreva explicitamente *"Nenhuma dependência identificada."* — **nunca omita silenciosamente.**

### 5.3 Sequência de Implementação Recomendada
- Liste a ordem obrigatória dos itens com justificativa curta por passo.
- Ao final, descreva o **teste de fumaça** do fluxo completo.

### 5.4 Riscos e Suposições
- Se não houver riscos relevantes: escreva *"Nenhum risco identificado além do padrão de regressão."*

### 5.5 Alternativas Consideradas
- Liste ao menos 1 alternativa descartada, mesmo que óbvia.

### 5.6 Referências
- Inclua ao menos referências a issues ou PRs relacionados, se existirem.

---

## 6. Retorno ao Cabeçalho

Volte ao cabeçalho (Passo 2) e preencha a `Prioridade de Execução` com a ordem definida na seção 5.3.

---

## 7. Apresentação e Barreira de Aprovação (Hard Stop)

**PAUSE a execução.**

Apresente o rascunho completo no chat (em bloco de código markdown) e informe:
- Quantos itens técnicos foram definidos.
- Quantas issues serão criadas.
- Qual arquivo será salvo em `backup/Plan/`.
- Se alguma seção ficou incompleta e por quê.

**Aguarde** aprovação explícita do usuário antes de salvar o arquivo.
- Aprovações válidas: *"Aprovado"*, *"Pode salvar"*, *"Prosseguir"*.
- **PROIBIDO** salvar sem aprovação, mesmo que o rascunho pareça completo.

---

## 8. Salvamento do Arquivo

Após aprovação:
1. Salve o arquivo **localmente** em `backup/Plan/<NomeCurtoDescritivo>.md` usando a ferramenta de criação/escrita de arquivos do workspace.
2. **PROIBIDO** usar `push_files` ou `create_or_update_file` do MCP para salvar na branch padrão — isso commitaria diretamente no GitHub sem PR.

---

## 9. Handoff para Revisão

Após salvar, sugira o próximo passo:
> "O rascunho foi salvo. Quando quiser, chame `@[/revisar_plano]` para a revisão crítica do plano antes de criar as issues."
