import os
import sys
import time
from pathlib import Path

# Bibliotecas de Interface
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.markdown import Markdown

# Bibliotecas opcionais
try:
    import msvcrt
except ImportError:
    msvcrt = None

try:
    import pyperclip
except ImportError:
    pyperclip = None

from ui.components import console, draw_header, draw_status_bar
from core.watcher import start_watcher

class MenuApp:
    """Orquestrador da Interface de Usuário no Terminal (TUI) e navegação de menus."""

    def __init__(self, config_manager, i18n_service, converter_service, console_inst=None):
        self.config_manager = config_manager
        self.i18n = i18n_service
        self.converter = converter_service
        self.console = console_inst or console
        self._t = i18n_service.translate
        self.remove_header = True

    def show_supported_formats(self) -> None:
        """Exibe a lista de formatos que o MarkItDown suporta."""
        self.console.clear()
        draw_header(self._t)
        self.console.print()
        
        table = Table(title=self._t("fmt_titulo"), show_header=True, header_style="bold magenta")
        table.add_column(self._t("fmt_categoria"), style="cyan", width=15)
        table.add_column(self._t("fmt_extensoes"), style="white")
        table.add_column(self._t("fmt_descricao"), style="dim")
        
        table.add_row(self._t("cat_documentos"), "PDF, DOCX, DOC", self._t("desc_documentos"))
        table.add_row(self._t("cat_planilhas"), "XLSX, XLS, CSV", self._t("desc_planilhas"))
        table.add_row(self._t("cat_slides"), "PPTX, PPT", self._t("desc_slides"))
        table.add_row(self._t("cat_web"), "HTML, HTM, URL", self._t("desc_web"))
        table.add_row(self._t("cat_imagens"), "JPG, PNG, TIFF", self._t("desc_imagens"))
        table.add_row(self._t("cat_audio"), "MP3, WAV", self._t("desc_audio"))
        table.add_row(self._t("cat_dados"), "JSON, XML", self._t("desc_dados"))
        table.add_row(self._t("cat_outros"), "EPUB, ZIP, MSG", self._t("desc_outros"))
        
        self.console.print(table)
        self.console.print(f"\n[info]{self._t('fmt_dica')}[/info]")
        self.console.input(f"\n[dim]{self._t('enter_voltar')}[/dim]")

    def preview_last_conversion(self) -> None:
        """Mostra o preview do último arquivo convertido."""
        config = self.config_manager.load()
        out_dir = config.get("output_dir")
        if not out_dir or not Path(out_dir).exists():
            self.console.print(f"[warning]{self._t('warn_sem_saida')}[/warning]")
            self.console.input(f"\n[dim]{self._t('enter_voltar_curto')}[/dim]")
            return

        md_files = sorted(Path(out_dir).glob("*.md"), key=os.path.getmtime, reverse=True)
        if not md_files:
            self.console.print(f"[warning]{self._t('warn_sem_preview')}[/warning]")
            self.console.input(f"\n[dim]{self._t('enter_voltar_curto')}[/dim]")
            return
        
        last_file = md_files[0]
        try:
            with open(last_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.console.print(f"[danger]{self._t('err_erro').format(e)}[/danger]")
            self.console.input(f"\n[dim]{self._t('enter_voltar_curto')}[/dim]")
            return
        
        self.console.clear()
        self.console.print(Panel(f"{self._t('preview_titulo').format(last_file.name)}", style="bold magenta"))
        self.console.print(Markdown(content[:2000] + (f"\n\n{self._t('preview_truncado')}" if len(content) > 2000 else "")))
        self.console.input(f"\n[dim]{self._t('enter_voltar_curto')}[/dim]")

    def setup_ai(self) -> None:
        """Configurações de IA."""
        config = self.config_manager.load()
        self.console.clear()
        draw_header(self._t)
        self.console.print(f"\n[header]{self._t('ai_titulo')}[/header]")
        self.console.print(f"[info]{self._t('ai_subtitulo')}[/info]\n")
        
        enabled = self.console.input(self._t("ai_ativar_prompt").format(self._t("sim") if config.get("llm_enabled") else self._t("nao"))).lower() in ['s', 'y']
        config["llm_enabled"] = enabled
        
        if enabled:
            config["openai_key"] = self.console.input(self._t("ai_key_prompt")).strip()
            config["openai_base_url"] = self.console.input(self._t("ai_url_prompt")).strip() or None
            config["openai_model"] = self.console.input(self._t("ai_modelo_prompt")).strip() or "gpt-4o"
        
        self.config_manager.save(config)
        self.console.print(f"[success]{self._t('ai_salvo')}[/success]")
        time.sleep(1)

    def convert_from_clipboard(self) -> None:
        """Tenta converter um caminho ou URL da área de transferência (clipboard)."""
        if not pyperclip:
            self.console.print(f"[danger]{self._t('err_pyperclip')}[/danger]")
            return
        
        text = pyperclip.paste().strip().strip('"').strip("'")
        if not text:
            self.console.print(f"[warning]{self._t('warn_clipboard_vazio')}[/warning]")
            return
        
        self.console.print(f"[info]{self._t('clipboard_detectado').format(text)}[/info]")
        self.converter.convert_single_file(text, remove_header=self.remove_header)

    def show_settings_menu(self) -> None:
        """Loop do Submenu de Configurações."""
        selected_index = 0

        while True:
            config = self.config_manager.load()
            out_dir = config.get("output_dir")
            out_dir_str = out_dir if out_dir else self._t("mesma_pasta_origem")
            llm_status = Text.from_markup(f"[bold green] {self._t('ia_on')} [/bold green]" if config.get("llm_enabled") else f"[bold dim] {self._t('ia_off')} [/bold dim]")

            self.console.clear()
            draw_header(self._t)
            self.console.print()
            self.console.print(f"[menu_opt]{self._t('menu_instrucao')}[/menu_opt]\n")

            # Opções do Submenu
            options = [
                self._t("menu_ia_opt"),
                self._t("menu_yaml_opt"),
                self._t("menu_saida_opt"),
                f"{self._t('menu_idioma_opt')} [{self.i18n.current_lang.upper()}]",
                self._t("menu_voltar")
            ]

            for i, option in enumerate(options):
                style = "selected" if i == selected_index else "menu_opt"
                prefix = " ➜ " if i == selected_index else "   "
                
                line = Text(f"{prefix}{option}", style=style)
                
                if self._t("menu_yaml_opt") in option:
                    line.append(Text(self._t("ativada"), style="success") if self.remove_header else Text(self._t("desativada"), style="danger"))
                if self._t("menu_ia_opt") in option:
                    line.append(llm_status)
                    
                self.console.print(line)

            self.console.print("\n" + "─" * 60, style="dim white")
            self.console.print(self._t("menu_info_saida").format(out_dir_str))
            self.console.print()
            draw_status_bar()
            self.console.print(f"\n [bold blue]➜[/bold blue] [bold white]{self._t('escolha')}[/bold white] ", end="")

            if msvcrt:
                key = msvcrt.getch()
                if key == b'\xe0':
                    key = msvcrt.getch()
                    if key == b'H': selected_index = (selected_index - 1) % len(options)
                    elif key == b'P': selected_index = (selected_index + 1) % len(options)
                    continue
                if key == b'\r': opcao = options[selected_index].split('.')[0].strip()
                elif key.isdigit(): opcao = key.decode()
                else: continue
            else:
                try:
                    opcao = self.console.input("\n [bold blue]➜[/bold blue] ").strip()
                    if not opcao: continue
                except Exception:
                    break

            if opcao == '1':
                self.setup_ai()
            elif opcao == '2':
                self.remove_header = not self.remove_header
            elif opcao == '3':
                path = self.console.input(f"\n[info]{self._t('prompt_pasta_saida')}[/info]").strip('"').strip("'")
                config["output_dir"] = path if path else None
                self.config_manager.save(config)
                self.console.print(f"[success]{self._t('status_configurado')}[/success]")
                time.sleep(1)
            elif opcao == '4':
                new_lang = "en" if self.i18n.current_lang == "pt" else "pt"
                self.i18n.set_language(new_lang)
                config["language"] = new_lang
                self.config_manager.save(config)
            elif opcao == '0':
                break

    def show_main_menu(self) -> None:
        """Loop do Menu Principal."""
        selected_index = 0

        while True:
            config = self.config_manager.load()
            out_dir = config.get("output_dir")
            out_dir_str = out_dir if out_dir else self._t("mesma_pasta_origem")

            self.console.clear()
            draw_header(self._t)
            self.console.print()
            self.console.print(f"[menu_opt]{self._t('menu_instrucao')}[/menu_opt]\n")

            options = [
                self._t("menu_formatos"),
                self._t("menu_converter"),
                self._t("menu_lote"),
                self._t("menu_watcher"),
                self._t("menu_clipboard"),
                self._t("menu_preview"),
                self._t("menu_configuracoes"),
                self._t("menu_sair")
            ]

            for i, option in enumerate(options):
                style = "selected" if i == selected_index else "menu_opt"
                prefix = " ➜ " if i == selected_index else "   "
                line = Text(f"{prefix}{option}", style=style)
                self.console.print(line)

            self.console.print("\n" + "─" * 60, style="dim white")
            self.console.print(self._t("menu_info_saida").format(out_dir_str))
            self.console.print()
            draw_status_bar()
            self.console.print(f"\n [bold blue]➜[/bold blue] [bold white]{self._t('escolha')}[/bold white] ", end="")

            if msvcrt:
                key = msvcrt.getch()
                if key == b'\xe0':
                    key = msvcrt.getch()
                    if key == b'H': selected_index = (selected_index - 1) % len(options)
                    elif key == b'P': selected_index = (selected_index + 1) % len(options)
                    continue
                if key == b'\r': opcao = options[selected_index].split('.')[0].strip()
                elif key.isdigit(): opcao = key.decode()
                else: continue
            else:
                try:
                    opcao = self.console.input("\n [bold blue]➜[/bold blue] ").strip()
                    if not opcao: continue
                except Exception:
                    break

            if opcao == '1':
                self.show_supported_formats()
            elif opcao == '2':
                path = self.console.input(f"\n[info]{self._t('prompt_arquivo_url')}[/info]").strip('"').strip("'")
                if path: 
                    self.converter.convert_single_file(path, remove_header=self.remove_header)
                self.console.input(f"\n[dim]{self._t('enter_voltar')}[/dim]")
            elif opcao == '3':
                path = self.console.input(f"\n[info]{self._t('prompt_pasta_lote')}[/info]").strip('"').strip("'")
                if path: 
                    self.converter.process_batch(Path(path), remove_header=self.remove_header)
                self.console.input(f"\n[dim]{self._t('enter_voltar')}[/dim]")
            elif opcao == '4':
                path = self.console.input(f"\n[info]{self._t('prompt_pasta_watcher')}[/info]").strip('"').strip("'")
                if path and Path(path).exists():
                    start_watcher(
                        Path(path), 
                        self.remove_header, 
                        self.converter, 
                        self.console, 
                        draw_header_fn=lambda: draw_header(self._t)
                    )
            elif opcao == '5':
                self.convert_from_clipboard()
                self.console.input(f"\n[dim]{self._t('enter_voltar')}[/dim]")
            elif opcao == '6':
                self.preview_last_conversion()
            elif opcao == '7':
                self.show_settings_menu()
            elif opcao == '0':
                break
