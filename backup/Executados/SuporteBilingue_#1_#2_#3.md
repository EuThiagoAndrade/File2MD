# Plano de Implementação — Adicionar Suporte Bilíngue (i18n)

> **Status:** Em Execução
> **Data de criação:** 2026-05-21
> **Última atualização:** 2026-05-21
> **Autor:** Thiago Andrade
> **Tipo:** feature
> **Prioridade:** 🟡 P3
> **Prioridade de Execução:** (Item 1 → Item 2) || Item 3

---

## 1. Rastreabilidade (Preenchido automaticamente)
- **Issues do GitHub:** #1, #2, #3
- **Pull Request (PR):** #ZZ

---

## 2. Objetivo e Escopo

### 2.1 Objetivo
Adicionar suporte a internacionalização (Português e Inglês) no projeto File2MD, abrangendo a interface do console e o README do GitHub, melhorando a adoção internacional da ferramenta.

### 2.2 Escopo
* **✅ Dentro do Escopo:**
  - Extração de strings estáticas para um dicionário de traduções interno no script.
  - Adição de "toggle" de idioma no menu principal do script.
  - Persistência do idioma selecionado no `config/file2md_config.json`.
  - Separação da documentação em `README.md` (PT) e `README_en.md` (EN) com navegação mútua via links.
* **❌ Fora do Escopo:**
  - Tradução de mensagens de erro cruas oriundas de bibliotecas ou APIs externas (ex: erros de requisição da OpenAI ou MarkItDown).
  - Suporte a idiomas adicionais além de Português e Inglês no escopo atual.

---

## 3. Arquivos Afetados (Consolidado)

| Arquivo | Ação | Camada | Item(ns) |
|---|---|---|---|
| `Scripts/File2MD.py` | Modificar | Python Core / TUI | Item 1, Item 2 |
| `README.md` | Modificar | Docs | Item 3 |
| `README_en.md` | Criar | Docs | Item 3 |

---

## 4. Detalhamento Técnico por Item

## Item 1 — Dicionário de Traduções e Lógica Core

**Contexto:**
Atualmente, as strings de interface do usuário estão hardcoded em Português ao longo de todo o `Scripts/File2MD.py`. As áreas afetadas incluem:
- A lista `options` em `show_menu()` (L397-L408) — todas as 10 opções do menu.
- Os prompts de `console.input()` em `show_menu()` (L462, L466, L470, L482) — textos como `"Arquivo ou URL: "`, `"Pasta para Lote: "`.
- Mensagens de status e erro em `convert_single_file()` (L134, L150, L176, L181), `process_batch()` (L187, L197, L200, L227), `convert_from_clipboard()` (L378, L383, L386).
- Títulos e conteúdos de `show_supported_formats()` (L272-L288) — título da tabela, categorias e descrições.
- O subtítulo do header em `draw_header()` (L315) — `"Wrapper Inteligente para o MarkItDown"`.
- Os textos de `setup_ai()` (L360-L362) e `preview_last_conversion()` (L338-L353).
- A instrução de navegação em `show_menu()` (L419) — `"Navegue com ↑ ↓..."`.

Precisamos isolá-las em um dicionário para permitir a troca dinâmica.

**Ação Técnica:**
- Arquivo afetado: `Scripts/File2MD.py`
- Criar o dicionário global `TRANSLATIONS` no topo do arquivo (após as constantes existentes), a variável de módulo `_CURRENT_LANG`, e a função auxiliar `_t(key)` para resgatar a tradução de forma rápida:
  ```python
  TRANSLATIONS: dict[str, dict[str, str]] = {
      "pt": {
          "menu_formatos": "1. Ver Formatos de Arquivo Suportados",
          "menu_converter": "2. Converter Arquivo Único",
          "menu_lote": "3. Converter Pasta em Lote (Lote/Paralelo)",
          "menu_watcher": "4. Monitorar Pasta (Watcher Mode)",
          "menu_clipboard": "5. Converter do Clipboard (Link ou Caminho)",
          "menu_preview": "6. Ver Preview da Última Conversão",
          "menu_ia": "7. Configurar IA (OpenAI/Local)",
          "menu_yaml": "8. Limpeza de Metadados YAML",
          "menu_saida": "9. Configurar Pasta de Saída",
          "menu_idioma": "10. Idioma / Language",
          "menu_sair": "0. Sair",
          # ... demais chaves para prompts, status, erros, tabelas
      },
      "en": {
          "menu_formatos": "1. View Supported File Formats",
          "menu_converter": "2. Convert Single File",
          "menu_lote": "3. Batch Convert Folder (Parallel)",
          "menu_watcher": "4. Watch Folder (Watcher Mode)",
          "menu_clipboard": "5. Convert from Clipboard (Link or Path)",
          "menu_preview": "6. Preview Last Conversion",
          "menu_ia": "7. Configure AI (OpenAI/Local)",
          "menu_yaml": "8. YAML Metadata Cleanup",
          "menu_saida": "9. Set Output Folder",
          "menu_idioma": "10. Idioma / Language",
          "menu_sair": "0. Exit",
          # ... demais chaves
      }
  }

  _CURRENT_LANG: str = "pt"

  def set_language(lang: str) -> None:
      """Define o idioma ativo para toda a sessão."""
      global _CURRENT_LANG
      _CURRENT_LANG = lang if lang in TRANSLATIONS else "pt"

  def _t(key: str) -> str:
      """Retorna a tradução da chave no idioma ativo."""
      return TRANSLATIONS.get(_CURRENT_LANG, TRANSLATIONS["pt"]).get(key, key)
  ```
- Substituir progressivamente cada string literal de UI pelo correspondente `_t("chave")`.
- No início de `show_menu()` e de `main()`, chamar `set_language(config.get("language", "pt"))` para carregar o idioma persistido.
- **Nota:** NÃO alterar a lógica de conversão real dos arquivos (`convert_single_file`, `post_process_markdown`, `clean_header`, `get_markitdown_instance` — exceto suas mensagens de `console.print/input`). NÃO alterar o `custom_theme`, o layout do banner ASCII, nem a lógica de `argparse`.

**Arquivos afetados:** `Scripts/File2MD.py` (Múltiplas alterações em blocos UI, ~120 linhas estimadas)

**Critério de Aceite:**
- [ ] O dicionário `TRANSLATIONS` contém chaves para PT e EN cobrindo **todas** as strings visíveis ao usuário (menu, prompts, status, erros, tabela de formatos, títulos de painéis).
- [ ] Toda chamada `console.print()` e `console.input()` que exibe texto de UI utiliza `_t("chave")` em vez de strings literais.
- [ ] O comando `python Scripts/File2MD.py` inicia no idioma configurado no `config/file2md_config.json` (ou `"pt"` por padrão na primeira execução).

---

## Item 2 — Toggle de Idioma no Menu (TUI) e Persistência

**Contexto:**
O menu principal (`show_menu()`, L393-L488) possui 10 opções numeradas de 1-9 e 0 (sair). A captura de tecla via `msvcrt.getch()` (L443-L451) aceita: setas (prefixo `b'\xe0'`), Enter (`b'\r'` — seleciona pelo índice), e dígitos (`key.isdigit()`). Qualquer outra tecla é ignorada pelo `else: continue` (L451). Para adicionar um atalho de letra ('I'), é necessário estender esse bloco. O idioma será persistido na chave `"language"` do `config/file2md_config.json`.

**Ação Técnica:**
- Arquivo afetado: `Scripts/File2MD.py`
- Adicionar o item `"10. Idioma / Language [PT]"` à lista `options` (entre a opção 9 e a opção 0), usando `_t()` para o texto base e exibindo o idioma ativo:
  ```python
  # Em show_menu(), na construção da lista options:
  options = [
      _t("menu_formatos"),
      _t("menu_converter"),
      _t("menu_lote"),
      _t("menu_watcher"),
      _t("menu_clipboard"),
      _t("menu_preview"),
      _t("menu_ia"),
      _t("menu_yaml"),
      _t("menu_saida"),
      f"{_t('menu_idioma')} [{_CURRENT_LANG.upper()}]",
      _t("menu_sair")
  ]
  ```
- Estender a captura de tecla `msvcrt` para aceitar `b'i'` e `b'I'`:
  ```python
  # Após elif key.isdigit(): opcao = key.decode()
  elif key.lower() == b'i':
      opcao = 'I'
  ```
- Adicionar a lógica de toggle na seção de execução:
  ```python
  elif opcao == 'I' or opcao == '10':
      new_lang = "en" if _CURRENT_LANG == "pt" else "pt"
      set_language(new_lang)
      config["language"] = new_lang
      save_config(config)
  ```
- Quando o usuário seleciona essa opção via Enter (cursor sobre ela), o `opcao` virá de `options[selected_index].split('.')[0].strip()` que retornará `"10"`, tratado pela condição acima.
- **Nota:** NÃO alterar a ordem nem o comportamento das opções 1-9 e 0 existentes. NÃO modificar a lógica de setas ↑↓ nem a renderização do banner/header.

**Arquivos afetados:** `Scripts/File2MD.py` (3 alterações principais: lista options, bloco msvcrt, bloco de execução — ~25 linhas)

**Critério de Aceite:**
- [ ] O menu exibe a opção "10. Idioma / Language [PT]" (ou [EN]) entre a opção 9 e a opção 0.
- [ ] Pressionar Enter quando o cursor está sobre a opção 10, ou pressionar a tecla 'I' a qualquer momento, alterna o idioma e reconstrói o menu inteiro no novo idioma instantaneamente.
- [ ] O arquivo `config/file2md_config.json` armazena corretamente o valor atualizado na chave `"language"` após o toggle.

---

## Item 3 — Atualização do README e Versão Bilíngue

**Contexto:**
O `README.md` original (99 linhas) é escrito inteiramente em Português. Contém um bloco HTML de logo no topo (L1-L7) usando `<picture>` com suporte a dark/light mode referenciando `.assets/Logo_branco.svg` e `.assets/Logo_preto.svg`. O restante é Markdown padrão com tabelas de parâmetros e funcionalidades.

**Ação Técnica:**
- Arquivos afetados: `README.md`, `README_en.md`
- Inserir imediatamente após o bloco `</p>` de fechamento do logo (L7) e antes do `# File2MD - Manual de Utilização` (L9), o bloco de links de idioma:
  ```markdown

  <p align="center">
    🇧🇷 <a href="README.md">Leia em Português</a> | 🇺🇸 <a href="README_en.md">Read in English</a>
  </p>

  ```
- Criar `README_en.md` traduzindo todo o conteúdo textual para Inglês, mantendo:
  - O mesmo bloco HTML do logo (L1-L7) sem alterações.
  - O bloco de links de idioma no topo (idêntico, apenas alterna a ênfase visual).
  - As mesmas chamadas de imagem/assets.
  - A mesma estrutura de tabelas (traduzindo conteúdo das células).
  - A nota `[!TIP]` traduzida para Inglês.
- **Nota:** NÃO alterar os paths de assets (`.assets/Logo_branco.svg`, etc.), NÃO alterar os nomes de arquivos/comandos nos exemplos de código (`python Scripts/File2MD.py` permanece igual), NÃO alterar a estrutura HTML do bloco de logo.

**Arquivos afetados:** `README.md` (1 inserção, ~4 linhas), `README_en.md` (1 criação de arquivo completo, ~99 linhas)

**Critério de Aceite:**
- [ ] `README.md` contém os links de navegação de idioma logo após o bloco de logo e antes do título H1.
- [ ] `README_en.md` existe, contém o mesmo bloco de logo, os links de idioma, e traduz todas as seções textuais para Inglês idiomático.
- [ ] Ao clicar nos links de alternância a partir do GitHub (web), os READMEs navegam corretamente entre si.

---

## 5. Governança e Roteiro de Entrega

### 5.1 Decomposição em Issues

| # | Título da Issue | Tipo | Prioridade | Depende de | Item(ns) do Plano |
|---|---|---|---|---|---|
| 1 | `[FEATURE] Adicionar dicionário de traduções i18n no core` | feature | 🟡 P3 | Nenhuma | Item 1 |
| 2 | `[FEATURE] Implementar toggle de idioma no Menu TUI` | feature | 🟡 P3 | Issue #1 | Item 2 |
| 3 | `[DOCS] Criar versão em Inglês do README (README_en.md)` | docs | 🟢 P4 | Nenhuma | Item 3 |

### 5.2 Dependências e Blockers
- Issue #2 depende de Issue #1 (o toggle precisa do dicionário e de `_t()` para funcionar).
- Issue #3 é independente e pode ser executada em paralelo com Issues #1 e #2.
- Nenhuma dependência externa de pacotes novos.

### 5.3 Sequência de Implementação Recomendada
1. **Passo 1:** Criar a estrutura estática (`TRANSLATIONS`, `_CURRENT_LANG`, `set_language()`, `_t()`) e substituir as strings em todo o script (Issue #1).
2. **Passo 2:** Adicionar a opção 10 ao menu, estender a captura de tecla e implementar o toggle com persistência (Issue #2).
3. **Passo 3 (paralelo):** Desenvolver e espelhar o `README.md` atual para `README_en.md` (Issue #3).
4. *Teste de Fumaça:* Executar `python Scripts/File2MD.py`, navegar até "10. Idioma / Language [PT]", pressionar Enter → verificar que todas as strings renderizaram em Inglês sem interromper a execução. Pressionar 'I' para alternar de volta e verificar que todas voltaram ao Português. Verificar `config/file2md_config.json` contém `"language": "en"` ou `"pt"` conforme a última escolha.

### 5.4 Riscos e Suposições
* **Risco 1:** A opção de menu 10 e seu atalho (letra `I`) falhar na captura via `msvcrt` que atualmente assume apenas bytes de dígitos numéricos. → **Mitigação:** Estender o bloco `elif key.isdigit()` com `elif key.lower() == b'i': opcao = 'I'` antes do `else: continue`.
* **Risco 2:** A pasta `config/` pode não existir na primeira execução, causando `FileNotFoundError` em `save_config()` ao tentar salvar o idioma. → **Mitigação:** Adicionar `CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)` no topo de `save_config()`. (**Nota:** este bug já existe no código atual para qualquer configuração, não é introduzido pelo i18n, mas será exposto pelo toggle de idioma na primeira execução.)
* **Risco 3:** Chaves faltantes no dicionário de traduções de um idioma causarem exibição da chave crua. → **Mitigação:** A função `_t()` já faz fallback para a chave; adicionar teste de fumaça que verifica paridade de chaves entre `TRANSLATIONS["pt"]` e `TRANSLATIONS["en"]`.

### 5.5 Alternativas Consideradas
* **Alternativa A:** Hospedar os textos traduzidos em múltiplos arquivos `.json` ou bibliotecas completas de i18n (`gettext`). Descartado para preservar a arquitetura simples e de script único (standalone) atual do projeto.

### 5.6 Referências
- Levantamento de base: `backup/Plan/Levantamento_Requisitos.md`

---

## 6. Pós-Mortem (Preenchido automaticamente ao finalizar)
- **PR**: #XX
- **Data de conclusão**: YYYY-MM-DD
- **Desvios do plano**: [breve descrição ou "nenhum"]
- **Issues imprevistas durante execução**: [breve ou "nenhuma"]

---
## Pós-Mortem (gerado automaticamente)
- **PR**: #4
- **Data de conclusão**: 2026-05-21
- **Desvios do plano**: Nenhum
- **Issues imprevistas durante execução**: Nenhuma

