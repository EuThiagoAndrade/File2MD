# Plano de Implementação — [TÍTULO CLARO E OBJETIVO]

> **Status:** Rascunho | Em Revisão | Aprovado | Em Execução | Executado
> **Data de criação:** YYYY-MM-DD
> **Última atualização:** YYYY-MM-DD
> **Autor:** Thiago Andrade
> **Tipo:** feature | fix | chore
> **Prioridade:** 🔴 P1 | 🟠 P2 | 🟡 P3 | 🟢 P4
> **Prioridade de Execução:** Item X → Item Y → Item Z

---

## 1. Rastreabilidade (Preenchido automaticamente)
- **Issues do GitHub:** #XX, #YY
- **Pull Request (PR):** #ZZ

---

## 2. Objetivo e Escopo

### 2.1 Objetivo
[Descreva em uma frase o que esta modificação realiza e por que é necessária.]

### 2.2 Escopo
* **✅ Dentro do Escopo:**
  - [Item de escopo 1]
  - [Item de escopo 2]
* **❌ Fora do Escopo:**
  - [Item fora de escopo 1]
  - [Item fora de escopo 2]

---

## 3. Arquivos Afetados (Consolidado)

| Arquivo | Ação | Camada | Item(ns) |
|---|---|---|---|
| `Scripts/File2MD.py` | Modificar | Python Core / TUI | Item 1, Item 2 |
| `README.md` | Modificar | Docs | Item 3 |
| `Tests/test_file2md.py` | Criar | Tests | Item 4 |

---

## 4. Detalhamento Técnico por Item

### 4.1 Item 1 — [Nome do Módulo ou Função Core]

**Contexto:**
[Explique o problema no código atual, citando nomes de funções ou comportamentos.]

**Ação Técnica:**
- Arquivo afetado: `Scripts/File2MD.py`
- [Descrição passo-a-passo da alteração técnica]
  ```python
  # Escreva o protótipo do código real em Python.
  # Use tipagem estrita (Type Hints) e garanta UTF-8 explícito para arquivos abertos.
  ```
- **Nota:** [O que NÃO deve ser alterado neste arquivo ou função para evitar regressões colaterais.]

**Arquivos afetados:** `Scripts/File2MD.py` (N alterações, ~X linhas)

**Critério de Aceite:**
- [ ] [Critério 1 — Condição empírica e objetiva de aceitação]
- [ ] [Critério 2 — Condição empírica e objetiva de aceitação]

---

### 4.2 Item 2 — [Nome da Tela ou Painel da TUI]

**Contexto:**
[Explique a mudança na interface de terminal ou navegação do menu.]

**Ação Técnica:**
- Arquivo afetado: `Scripts/File2MD.py`
- [Descreva as alterações de menu e estilização via Rich]
  ```python
  # Protótipo de código Rich/TUI usando custom_theme tokens.
  ```
- **Nota:** [O que NÃO deve ser alterado para preservar a estética de console.]

**Arquivos afetados:** `Scripts/File2MD.py` (N alterações, ~X linhas)

**Critério de Aceite:**
- [ ] [A opção X aparece no Menu Interativo]
- [ ] [A renderização do painel Y respeita os tokens do custom_theme]

---

## 5. Governança e Roteiro de Entrega

### 5.1 Decomposição em Issues

| # | Título da Issue | Tipo | Prioridade | Depende de | Item(ns) do Plano |
|---|---|---|---|---|---|
| 1 | `[FEATURE] Adicionar suporte a X` | feature | 🟠 P2 | Nenhuma | Item 1 |
| 2 | `[FEATURE] Adicionar opção de menu para X` | feature | 🟠 P2 | Issue #1 | Item 2 |

### 5.2 Dependências e Blockers
[Liste qualquer blocalizador ou dependência externa de pacotes]

### 5.3 Sequência de Implementação Recomendada
1. **Passo 1:** Implementar a lógica Core no script.
2. **Passo 2:** Integrar e testar visualmente no Menu Principal (TUI).
3. **Passo 3:** Executar testes manuais e de fumaça:
   - *Comando:* `python Scripts/File2MD.py [argumentos]`
   - *Verificação:* [o que checar no terminal]

### 5.4 Riscos e Suposições
* **Risco:** [Risco identificado] -> **Mitigação:** [Ação mitigadora]

### 5.5 Alternativas Consideradas
* **Alternativa A:** [Descreva alternativa descartada e o porquê]

### 5.6 Referências
- [Links para issues, PRs ou discussões anteriores]

---

## 6. Pós-Mortem (Preenchido progressivamente)
> *(Nota para o Agente: Cada PR associado a este plano deve adicionar um novo tópico principal aqui. Não sobrescreva PRs anteriores e NÃO concatene blocos inteiros novos com "## 6. Pós-Mortem" no fim do arquivo. Edite esta seção.)*

* **PR #XX (Issue Y):**
  - **Data de conclusão**: YYYY-MM-DD
  - **Desvios do plano**: [breve descrição ou "nenhum"]
  - **Issues imprevistas**: [breve ou "nenhuma"]