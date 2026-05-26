# Plano de Implementação — Refatoração de Arquitetura e Reestruturação do Menu Principal

> **Status:** Concluído
> **Data de criação:** 2026-05-26
> **Última atualização:** 2026-05-26
> **Autor:** Thiago Andrade
> **Tipo:** chore / feature
> **Prioridade:** 🔴 P1
> **Prioridade de Execução:** Item 1 → Item 2 → Item 3

---

## 1. Rastreabilidade (Preenchido automaticamente)
- **Issues do GitHub:** #12, #13, #14
- **Pull Request (PR):** #ZZ

---

## 2. Objetivo e Escopo

### 2.1 Objetivo
Refatorar o arquivo monolítico `Scripts/File2MD.py` (~700 linhas) separando-o em módulos de responsabilidade única (Core, UI, Utils), introduzindo conceitos leves de Orientação a Objetos, e reestruturar o Menu Principal da TUI movendo opções de configuração para um Submenu dedicado.

### 2.2 Escopo
* **✅ Dentro do Escopo:**
  - Criação de uma nova estrutura de pastas (`core/`, `ui/`, `utils/`) dentro de `Scripts/`, com `__init__.py` em cada pacote.
  - Separação de lógicas de Conversão, Watchdog, Configuração, Internacionalização e Pós-Processamento em classes/módulos dedicados.
  - Reestruturação do Menu da interface (Rich) para um Menu Principal de ações e um Submenu de configurações.
  - Atualização do ponto de entrada principal (`File2MD.py`) para apenas instanciar as classes e orquestrar o fluxo.
* **❌ Fora do Escopo:**
  - Alterações nas regras de negócio de conversão do MarkItDown.
  - Adição de novos provedores de IA ou novas integrações de API.
  - Modificações no estilo de cores atual do Rich console (`custom_theme`).

---

## 3. Arquivos Afetados (Consolidado)

| Arquivo | Ação | Camada | Item(ns) |
|---|---|---|---|
| `Scripts/core/__init__.py` | Criar | Pacote | Item 1 |
| `Scripts/core/converter.py` | Criar | Lógica Core | Item 1 |
| `Scripts/core/watcher.py` | Criar | Lógica Core | Item 1 |
| `Scripts/core/postprocess.py` | Criar | Lógica Core | Item 1 |
| `Scripts/utils/__init__.py` | Criar | Pacote | Item 1 |
| `Scripts/utils/config_manager.py` | Criar | Utils | Item 1 |
| `Scripts/utils/i18n.py` | Criar | Utils | Item 1 |
| `Scripts/ui/__init__.py` | Criar | Pacote | Item 2 |
| `Scripts/ui/components.py` | Criar | TUI | Item 2 |
| `Scripts/ui/menus.py` | Criar | TUI | Item 2 |
| `Scripts/File2MD.py` | Modificar | Entrypoint | Item 3 |

---

## 4. Detalhamento Técnico por Item

### 4.1 Item 1 — Separação de Módulos (Core e Utils) em Classes

**Contexto:**
As funções de configuração (`load_config`, `save_config`, L246-260), internacionalização (`set_language`, `_t`, L234-244), conversões (`convert_single_file` L300-358, `process_batch` L360-403), pós-processamento (`clean_header` L282-285, `post_process_markdown` L287-298), a factory `get_markitdown_instance` (L262-280) e o tratador de eventos do Watchdog (`WatcherHandler` L406-418, `start_watcher` L420-440) estão todas no mesmo arquivo `File2MD.py`. Variáveis como `CONFIG_FILE`, `TRANSLATIONS`, `_CURRENT_LANG` e `console` vivem no escopo de módulo sem encapsulamento. O import de `ProcessPoolExecutor` (L10) está presente mas não é utilizado e deve ser removido na limpeza.

**Ação Técnico:**
- Criar arquivos: `core/__init__.py`, `utils/__init__.py`, `utils/config_manager.py`, `utils/i18n.py`, `core/converter.py`, `core/watcher.py`, `core/postprocess.py`.

- **`ConfigManager`** (`utils/config_manager.py`): Classe que encapsula `CONFIG_FILE`, `load_config()` e `save_config()`.
  ```python
  from pathlib import Path
  import json

  class ConfigManager:
      def __init__(self, config_path: Path | None = None):
          self.config_path = config_path or Path(__file__).parent.parent.parent / "config" / "file2md_config.json"

      def load(self) -> dict:
          if self.config_path.exists():
              with open(self.config_path, 'r', encoding='utf-8') as f:
                  return json.load(f)
          return {}

      def save(self, config: dict) -> None:
          self.config_path.parent.mkdir(parents=True, exist_ok=True)
          with open(self.config_path, 'w', encoding='utf-8') as f:
              json.dump(config, f, indent=4)
  ```

- **`I18nService`** (`utils/i18n.py`): Classe que encapsula o dicionário `TRANSLATIONS` e a língua ativa. Elimina o `global _CURRENT_LANG`.

- **`PostProcessor`** (`core/postprocess.py`): Módulo contendo `clean_header()` e `post_process_markdown()`, extraídas sem alteração de lógica.

- **`ConverterService`** (`core/converter.py`): Classe que encapsula `get_markitdown_instance()`, `convert_single_file()` e `process_batch()`.
  ```python
  class ConverterService:
      def __init__(self, config_manager: ConfigManager, i18n_service: I18nService, console: Console):
          self.config = config_manager
          self._t = i18n_service.translate
          self.console = console
          self._init_markitdown()

      def convert_single_file(self, input_path: str, output_path: str | None = None,
                              remove_header: bool = True, silent: bool = False) -> bool:
          # Lógica atual de L300-358 preservada
          ...
  ```

- **`WatcherHandler` / `start_watcher`** (`core/watcher.py`): Classe movida sem alteração lógica, recebendo `ConverterService` e `Console` via injeção.

- **Nota:** Nenhuma regra de parse do MarkItDown ou do pós-processamento (regex de `clean_header`, normalização de quebras de linha) deve ser alterada — apenas movida. O import não utilizado de `ProcessPoolExecutor` deve ser removido do entrypoint final.

**Arquivos afetados:** `Scripts/core/*.py`, `Scripts/utils/*.py` (7 arquivos novos incluindo `__init__.py`, ~450 linhas movidas)

**Critério de Aceite:**
- [ ] A lógica de configuração (`ConfigManager`) lê e grava o JSON adequadamente sem uso de `global`.
- [ ] A conversão via código (sem menu) gera o Markdown exatamente igual à versão monolítica. Teste: `python -c "from Scripts.core.converter import ConverterService; ..."` com um arquivo PDF de referência, comparando output byte-a-byte.
- [ ] `clean_header()` e `post_process_markdown()` existem em `core/postprocess.py` e produzem resultado idêntico ao original.

---

### 4.2 Item 2 — Reestruturação da Interface de Usuário (TUI e Submenus)

**Contexto:**
A tela do Menu atual (`show_menu`, L569-674) mistura 11 opções numa lista plana: ações primárias (Converter, Lote, Watcher, Clipboard, Preview, Formatos) com configurações de ambiente (IA, YAML, Pasta de Saída, Idioma). As funções de UI (`draw_header` L468-499, `draw_status_bar` L501-507, `show_supported_formats` L442-464, `preview_last_conversion` L509-529, `setup_ai` L531-549, `convert_from_clipboard` L551-565) estão soltas no módulo. Precisamos migrar tudo para o pacote `ui/` e criar dois loops de menu distintos.

**Ação Técnica:**
- Criar arquivos: `ui/__init__.py`, `ui/components.py`, `ui/menus.py`.

- **`components.py`**: Conterá:
  - `custom_theme` (movido de L54-64)
  - Singleton `console = Console(theme=custom_theme)` — ponto único de instanciação
  - `draw_header()` (movida de L468-499)
  - `draw_status_bar()` (movida de L501-507)
  - Banner ASCII data

- **`menus.py`**: Conterá a classe `MenuApp` com:
  - `show_main_menu()` — loop principal com opções de **ação**:
    ```
    1. Ver Formatos Suportados
    2. Converter Arquivo Único
    3. Converter Pasta em Lote
    4. Monitorar Pasta (Watcher)
    5. Converter do Clipboard
    6. Ver Preview da Última Conversão
    7. Configurações ⚙️
    0. Sair
    ```
  - `show_settings_menu()` — submenu de **configuração**:
    ```
    1. Configurar IA (OpenAI/Local)
    2. Limpeza de Metadados YAML (ON/OFF)
    3. Configurar Pasta de Saída
    4. Idioma / Language
    0. Voltar ao Menu Principal
    ```
  - Métodos auxiliares migrados: `show_supported_formats()`, `preview_last_conversion()`, `setup_ai()`, `convert_from_clipboard()`

- **Nota:** Os atalhos de teclado (setinhas via `msvcrt`, L622-632) devem ser mantidos e suportar a navegação nos dois menus. O estilo `custom_theme` e os tokens de cor (`info`, `warning`, `danger`, `success`, `selected`, etc.) não devem ser alterados.

**Arquivos afetados:** `Scripts/ui/menus.py`, `Scripts/ui/components.py` (3 arquivos novos incluindo `__init__.py`, ~300 linhas movidas/refatoradas)

**Critério de Aceite:**
- [ ] O Menu Principal exibe apenas as 7 opções de ação (1-6 + Configurações) e Sair (0).
- [ ] Ao pressionar '7' (ou selecionar "Configurações"), a tela é limpa e o Submenu é exibido com 4 opções + Voltar.
- [ ] O Submenu permite alterar idioma, configurar IA, toggle YAML e definir pasta de saída, refletindo as alterações instantaneamente sem quebrar a TUI.
- [ ] As setas ↑↓ e Enter funcionam em ambos os menus.

---

### 4.3 Item 3 — Limpeza e Adaptação do Entrypoint (File2MD.py)

**Contexto:**
Após a refatoração, o `File2MD.py` deve deixar de ser o "faz tudo" (~700 linhas) e atuar apenas como o injetor de dependências inicial e leitor de CLI (argparse, L679-686).

**Ação Técnica:**
- Arquivo afetado: `Scripts/File2MD.py`
- Limpar todo o código movido para os pacotes `core/`, `ui/`, `utils/`.
- Remover o import não utilizado de `ProcessPoolExecutor`.
- Importar as classes dos novos pacotes.
- Adicionar `Scripts/` ao `sys.path` se necessário para resolver imports relativos.
- Atualizar a função `main()` para orquestrar as instâncias.
  ```python
  import sys
  import argparse
  from pathlib import Path

  # Garante que os pacotes internos sejam encontrados
  sys.path.insert(0, str(Path(__file__).parent))

  from core.converter import ConverterService
  from core.watcher import start_watcher
  from ui.components import console
  from ui.menus import MenuApp
  from utils.config_manager import ConfigManager
  from utils.i18n import I18nService

  def main():
      config_mgr = ConfigManager()
      config = config_mgr.load()
      i18n = I18nService(config.get("language", "pt"))
      converter = ConverterService(config_mgr, i18n, console)
      app = MenuApp(config_mgr, i18n, converter, console)

      parser = argparse.ArgumentParser(description="File2MD Pro - MarkItDown Wrapper")
      parser.add_argument("input", nargs="?", help="Arquivo ou URL")
      parser.add_argument("-o", "--output", help="Saída")
      parser.add_argument("-d", "--directory", action="store_true", help="Modo diretório")
      parser.add_argument("--watch", action="store_true", help="Inicia modo Watcher")
      parser.add_argument("--keep-header", action="store_true", help="Mantém cabeçalho original")
      args = parser.parse_args()

      if args.watch and args.input:
          start_watcher(Path(args.input), not args.keep_header, converter, console)
      elif args.input:
          remove_header = not args.keep_header
          if args.directory or Path(args.input).is_dir():
              converter.process_batch(Path(args.input), remove_header)
          else:
              converter.convert_single_file(args.input, args.output, remove_header)
      else:
          app.show_main_menu()

  if __name__ == "__main__":
      main()
  ```

- **Nota:** As flags do `argparse` (`input`, `-o`, `-d`, `--watch`, `--keep-header`) NÃO devem ser renomeadas ou removidas para manter compatibilidade com scripts e aliases existentes dos usuários.

**Arquivos afetados:** `Scripts/File2MD.py` (1 arquivo reduzido de ~700 linhas para ~60 linhas)

**Critério de Aceite:**
- [ ] `File2MD.py` contém no máximo ~60 linhas com apenas setup, argparse e orquestração.
- [ ] Execução em modo CLI (`python Scripts/File2MD.py arquivo.pdf`) funciona sem passar pela UI.
- [ ] Execução direta (`python Scripts/File2MD.py`) abre a nova TUI normalmente.
- [ ] Todas as flags de argparse originais continuam funcionando sem alteração de nomes.

---

## 5. Governança e Roteiro de Entrega

### 5.1 Decomposição em Issues

| # | Título da Issue | Tipo | Prioridade | Depende de | Item(ns) do Plano |
|---|---|---|---|---|---|
| 1 | `[CHORE] Extrair módulos Core e Utils do monolito File2MD.py` | chore | 🔴 P1 | Nenhuma | Item 1 |
| 2 | `[FEATURE] Reestruturar interface do terminal em submenus` | feature | 🔴 P1 | Issue #1 | Item 2 |
| 3 | `[CHORE] Reduzir File2MD.py a entrypoint mínimo` | chore | 🔴 P1 | Issue #2 | Item 3 |

### 5.2 Dependências e Blockers
Nenhuma dependência externa nova. Todas as bibliotecas (`rich`, `watchdog`, `pyperclip`, `openai`, `markitdown`) já estão declaradas em `requirements.txt`.

### 5.3 Sequência de Implementação Recomendada
1. **Passo 1:** Criar as pastas (`core/`, `ui/`, `utils/`) com `__init__.py` e extrair o código de utilitários e core (Item 1).
   - **Teste intermediário:** Executar `python -c "from Scripts.utils.config_manager import ConfigManager; c = ConfigManager(); print(c.load())"` para validar imports e funcionalidade isolada.
2. **Passo 2:** Criar o pacote UI e refatorar o loop de menus, conectando com as classes do passo 1 (Item 2).
3. **Passo 3:** Limpar definitivamente o `File2MD.py` integrando CLI e Menu. Executar testes manuais e de fumaça:
   - *Comando:* `python Scripts/File2MD.py` → Navegar no Menu Principal e no Submenu de Configurações
   - *Comando:* `python Scripts/File2MD.py arquivo.pdf` → Verificar conversão direta via CLI
   - *Comando:* `python Scripts/File2MD.py -d pasta_teste` → Verificar lote

### 5.4 Riscos e Suposições
* **Risco:** Quebra de escopo de variáveis no `watchdog` e concorrência multithread da UI com o processo em lote. -> **Mitigação:** Manter a injeção do objeto `Console` limpa nas classes de serviço e garantir que a barra de progresso lide corretamente com chamadas de thread.
* **Risco:** Imports circulares entre pacotes. -> **Mitigação:** Manter dependências unidirecionais: `utils ← core ← ui ← entrypoint`.

### 5.5 Alternativas Consideradas
* **Alternativa A:** Manter a estrutura monolítica mas usar "dobradura de código" (region) no editor. Descartada pois dificulta testes automatizados futuros e prejudica a saúde do projeto a longo prazo.

### 5.6 Referências
- Conversação de planejamento via `@[/grill-me]` e alinhamento de UX.

---

## 6. Pós-Mortem (Preenchido progressivamente)
> *(Nota para o Agente: Cada PR associado a este plano deve adicionar um novo tópico principal aqui. Não sobrescreva PRs anteriores e NÃO concatene blocos inteiros novos com "## 6. Pós-Mortem" no fim do arquivo. Edite esta seção.)*

* **PR #15 (Issue #12):**
  - **Data de conclusão**: 2026-05-26
  - **Desvios do plano**: nenhum
  - **Issues imprevistas**: nenhuma
* **PR #16 (Issue #13):**
  - **Data de conclusão**: 2026-05-26
  - **Desvios do plano**: nenhum
  - **Issues imprevistas**: nenhuma
* **PR #17 (Issue #14):**
  - **Data de conclusão**: 2026-05-26
  - **Desvios do plano**: nenhum
  - **Issues imprevistas**: nenhuma
