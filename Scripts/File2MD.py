import os
import sys
import subprocess
import argparse
import re
import json
import time
import threading
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

# Bibliotecas de Interface
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.theme import Theme
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.live import Live
from rich.markdown import Markdown

# Bibliotecas de Funcionalidades Extras (Opcionais)
try:
    import msvcrt
except ImportError:
    msvcrt = None

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    Observer = None
    FileSystemEventHandler = object

# Tentativa de importar MarkItDown e OpenAI
try:
    from markitdown import MarkItDown
    HAS_MARKITDOWN_API = True
except ImportError:
    HAS_MARKITDOWN_API = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Configuração de tema para a interface
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "success": "bold green",
    "header": "bold white",
    "menu_opt": "white",
    "selected": "bold white on blue",
    "status": "white on blue",
    "accent": "bold green"
})

console = Console(theme=custom_theme)

# Arquivo de configuração persistente
CONFIG_FILE = Path(__file__).parent.parent / "config" / "file2md_config.json"

TRANSLATIONS = {
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
        "menu_instrucao": "Navegue com [bold]↑ ↓[/bold] e selecione com [bold]Enter[/bold].",
        "menu_info_saida": " [info]Saída:[/info] [white]{}[/white]",
        "mesma_pasta_origem": "Mesma pasta da origem",
        "ia_on": " [ IA ON ]",
        "ia_off": " [ IA OFF ]",
        "ativada": " [ ATIVADA ]",
        "desativada": " [ DESATIVADA ]",
        "escolha": " Escolha:",
        "err_nao_encontrado": "❌ Não encontrado: {}",
        "status_processando": "🔄 Processando: {}...",
        "status_salvo": "✅ Salvo em: {}",
        "err_erro": "❌ Erro: {}",
        "err_pasta_invalida": "❌ Pasta inválida.",
        "warn_nenhum_arquivo": "⚠️ Nenhum arquivo compatível encontrado na pasta.",
        "status_lote_inicio": "🚀 Iniciando processamento em lote ({} arquivos)...",
        "status_lote_convertendo": "Convertendo...",
        "status_lote_fim": "✨ Processamento em lote concluído!",
        "err_watchdog": "❌ Erro: Biblioteca 'watchdog' não instalada.",
        "watcher_detectado": "🔔 Novo arquivo detectado: {}",
        "watcher_monitorando": "Monitorando pasta:",
        "watcher_parar": "Pressione Ctrl+C para parar e voltar ao menu.",
        "fmt_titulo": "📄 Formatos Suportados pelo MarkItDown",
        "fmt_categoria": "Categoria",
        "fmt_extensoes": "Extensões",
        "fmt_descricao": "Descrição",
        "cat_documentos": "Documentos",
        "desc_documentos": "Texto, tabelas e estrutura básica",
        "cat_planilhas": "Planilhas",
        "desc_planilhas": "Converte tabelas para formato Markdown",
        "cat_slides": "Slides",
        "desc_slides": "Extrai texto e estrutura de slides",
        "cat_web": "Web",
        "desc_web": "Websites, artigos e vídeos do YouTube",
        "cat_imagens": "Imagens",
        "desc_imagens": "Extrai texto via OCR ou descrição via IA",
        "cat_audio": "Áudio",
        "desc_audio": "Metadados e transcrição via IA (se configurado)",
        "cat_dados": "Dados",
        "desc_dados": "Formata dados estruturados",
        "cat_outros": "Outros",
        "desc_outros": "Livros, arquivos compactados e e-mails",
        "fmt_dica": "💡 Dica: URLs do YouTube podem gerar resumos automáticos.",
        "enter_voltar": "Pressione Enter para voltar ao menu...",
        "header_subtitulo": " - Wrapper Inteligente para o MarkItDown",
        "warn_sem_saida": "⚠️ Pasta de saída não configurada ou vazia.",
        "warn_sem_preview": "⚠️ Nenhum arquivo .md encontrado para preview.",
        "preview_titulo": "📖 Preview: {}",
        "preview_truncado": "... (conteúdo truncado)",
        "enter_voltar_curto": "Pressione Enter para voltar...",
        "ai_titulo": "🤖 Configuração de Inteligência Artificial",
        "ai_subtitulo": "Use para descrever imagens e transcrever áudios complexos.",
        "ai_ativar_prompt": "Ativar IA? (s/n) [Atual: {}]: ",
        "sim": "Sim",
        "nao": "Não",
        "ai_key_prompt": "OpenAI API Key: ",
        "ai_url_prompt": "Base URL (Vazio para padrão OpenAI): ",
        "ai_modelo_prompt": "Modelo (Padrão: gpt-4o): ",
        "ai_salvo": "✅ Configurações de IA salvas!",
        "err_pyperclip": "❌ Erro: Biblioteca 'pyperclip' não instalada.",
        "warn_clipboard_vazio": "⚠️ Área de transferência vazia.",
        "clipboard_detectado": "📋 Detectado no Clipboard: {}",
        "prompt_pasta_lote": "Pasta para Lote: ",
        "prompt_pasta_watcher": "Pasta para Monitorar: ",
        "prompt_pasta_saida": "Pasta de Saída (Branco para origem): ",
        "prompt_arquivo_url": "Arquivo ou URL: ",
        "status_configurado": "✅ Configurado!"
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
        "menu_instrucao": "Navigate with [bold]↑ ↓[/bold] and select with [bold]Enter[/bold].",
        "menu_info_saida": " [info]Output:[/info] [white]{}[/white]",
        "mesma_pasta_origem": "Same folder as source",
        "ia_on": " [ IA ON ]",
        "ia_off": " [ IA OFF ]",
        "ativada": " [ ENABLED ]",
        "desativada": " [ DISABLED ]",
        "escolha": " Choose:",
        "err_nao_encontrado": "❌ Not found: {}",
        "status_processando": "🔄 Processing: {}...",
        "status_salvo": "✅ Saved to: {}",
        "err_erro": "❌ Error: {}",
        "err_pasta_invalida": "❌ Invalid folder.",
        "warn_nenhum_arquivo": "⚠️ No compatible files found in the folder.",
        "status_lote_inicio": "🚀 Starting batch processing ({} files)...",
        "status_lote_convertendo": "Converting...",
        "status_lote_fim": "✨ Batch processing completed!",
        "err_watchdog": "❌ Error: 'watchdog' library not installed.",
        "watcher_detectado": "🔔 New file detected: {}",
        "watcher_monitorando": "Watching folder:",
        "watcher_parar": "Press Ctrl+C to stop and return to menu.",
        "fmt_titulo": "📄 Formatos Suportados pelo MarkItDown",
        "fmt_categoria": "Category",
        "fmt_extensoes": "Extensions",
        "fmt_descricao": "Description",
        "cat_documentos": "Documents",
        "desc_documentos": "Text, tables and basic structure",
        "cat_planilhas": "Spreadsheets",
        "desc_planilhas": "Converts tables to Markdown format",
        "cat_slides": "Slides",
        "desc_slides": "Extracts text and structure from slides",
        "cat_web": "Web",
        "desc_web": "Websites, articles and YouTube videos",
        "cat_imagens": "Images",
        "desc_imagens": "Extracts text via OCR or description via AI",
        "cat_audio": "Audio",
        "desc_audio": "Metadata and transcription via AI (if configured)",
        "cat_dados": "Data",
        "desc_dados": "Formats structured data",
        "cat_outros": "Others",
        "desc_outros": "Books, compressed files and emails",
        "fmt_dica": "💡 Tip: YouTube URLs can generate automatic summaries.",
        "enter_voltar": "Press Enter to return to menu...",
        "header_subtitulo": " - Intelligent Wrapper for MarkItDown",
        "warn_sem_saida": "⚠️ Output folder not configured or empty.",
        "warn_sem_preview": "⚠️ No .md files found for preview.",
        "preview_titulo": "📖 Preview: {}",
        "preview_truncado": "... (content truncated)",
        "enter_voltar_curto": "Press Enter to return...",
        "ai_titulo": "🤖 Artificial Intelligence Configuration",
        "ai_subtitulo": "Use to describe images and transcribe complex audio.",
        "ai_ativar_prompt": "Activate AI? (y/n) [Current: {}]: ",
        "sim": "Yes",
        "nao": "No",
        "ai_key_prompt": "OpenAI API Key: ",
        "ai_url_prompt": "Base URL (Empty for default OpenAI): ",
        "ai_modelo_prompt": "Model (Default: gpt-4o): ",
        "ai_salvo": "✅ AI configurations saved!",
        "err_pyperclip": "❌ Error: 'pyperclip' library not installed.",
        "warn_clipboard_vazio": "⚠️ Clipboard is empty.",
        "clipboard_detectado": "📋 Detected in Clipboard: {}",
        "prompt_pasta_lote": "Batch Folder: ",
        "prompt_pasta_watcher": "Folder to Watch: ",
        "prompt_pasta_saida": "Output Folder (Blank for source): ",
        "prompt_arquivo_url": "File or URL: ",
        "status_configurado": "✅ Configured!"
    }
}

_CURRENT_LANG = "pt"

def set_language(lang):
    """Define o idioma ativo para toda a sessão."""
    global _CURRENT_LANG
    if lang in TRANSLATIONS:
        _CURRENT_LANG = lang
    else:
        _CURRENT_LANG = "pt"

def _t(key):
    """Retorna a tradução da chave no idioma ativo."""
    return TRANSLATIONS.get(_CURRENT_LANG, TRANSLATIONS["pt"]).get(key, key)

def load_config():
    """Carrega as configurações do arquivo JSON."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    """Salva as configurações no arquivo JSON."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

def get_markitdown_instance():
    """Inicializa a instância do MarkItDown com suporte a LLM se configurado."""
    if not HAS_MARKITDOWN_API:
        return None
    
    config = load_config()
    llm_enabled = config.get("llm_enabled", False)
    
    if llm_enabled and HAS_OPENAI:
        try:
            client = OpenAI(
                api_key=config.get("openai_key"),
                base_url=config.get("openai_base_url") # Para Ollama ou local
            )
            return MarkItDown(llm_client=client, llm_model=config.get("openai_model", "gpt-4o"))
        except:
            return MarkItDown()
    
    return MarkItDown()

def clean_header(content):
    """Remove o cabeçalho YAML de forma robusta."""
    pattern = r'^---\s*[\r\n]+.*?[\r\n]+---\s*'
    return re.sub(pattern, '', content, count=1, flags=re.DOTALL | re.MULTILINE).lstrip()

def post_process_markdown(content, remove_header=True):
    """Aplica limpezas adicionais ao Markdown."""
    if remove_header:
        content = clean_header(content)
    
    # Normalização de quebras de linha excessivas (máximo 2 seguidas)
    content = re.sub(r'(\r?\n){3,}', '\n\n', content)
    
    # Limpeza de espaços no final de cada linha
    content = "\n".join(line.rstrip() for line in content.splitlines())
    
    return content

def convert_single_file(input_path, output_path=None, remove_header=True, silent=False):
    """Converte um arquivo individual usando API ou Subprocess."""
    config = load_config()
    default_out_dir = config.get("output_dir")
    
    is_url = str(input_path).startswith(('http://', 'https://'))
    
    if not is_url:
        input_path = Path(input_path)
        if not input_path.exists():
            if not silent: console.print(f"[danger]{_t('err_nao_encontrado').format(input_path)}[/danger]")
            return False
        
        if not output_path:
            if default_out_dir and os.path.exists(default_out_dir):
                output_path = Path(default_out_dir) / input_path.with_suffix('.md').name
            else:
                output_path = input_path.with_suffix('.md')
    else:
        if not output_path:
            if default_out_dir and os.path.exists(default_out_dir):
                output_path = Path(default_out_dir) / "web_content.md"
            else:
                output_path = Path("web_content.md")

    output_path = Path(output_path)
    if not silent: console.print(f"[info]{_t('status_processando').format(input_path if is_url else input_path.name)}[/info]")
    
    try:
        content = ""
        # Prioridade 1: API Nativa
        if HAS_MARKITDOWN_API:
            md = get_markitdown_instance()
            result = md.convert(str(input_path))
            content = result.text_content
        # Prioridade 2: Subprocess (Legacy)
        else:
            exe_path = config.get("path") or "markitdown"
            res = subprocess.run([exe_path, str(input_path)], capture_output=True, check=False)
            if res.returncode == 0:
                try:
                    content = res.stdout.decode('utf-8')
                except UnicodeDecodeError:
                    content = res.stdout.decode('cp1252', errors='replace')
            else:
                raise Exception(res.stderr.decode('utf-8', errors='replace'))

        if content:
            content = post_process_markdown(content, remove_header)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                f.write(content)
            if not silent: console.print(f"[success]{_t('status_salvo').format(output_path)}[/success]")
            return True
        return False

    except Exception as e:
        if not silent: console.print(f"[danger]{_t('err_erro').format(e)}[/danger]")
        return False

def process_batch(input_path, remove_header=True):
    """Processa múltiplos arquivos em paralelo com barra de progresso."""
    if not input_path.is_dir():
        console.print(f"[danger]{_t('err_pasta_invalida')}[/danger]")
        return

    exts = ['.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', 
            '.jpg', '.png', '.mp3', '.wav', '.html', '.htm', '.csv', 
            '.json', '.xml', '.epub', '.zip', '.msg']
    
    files = [f for f in input_path.glob("*.*") if f.suffix.lower() in exts]
    
    if not files:
        console.print(f"[warning]{_t('warn_nenhum_arquivo')}[/warning]")
        return

    console.print(f"[info]{_t('status_lote_inicio').format(len(files))}[/info]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task(_t("status_lote_convertendo"), total=len(files))
        
        # Uso de ThreadPool para I/O ou ProcessPool para CPU. 
        # MarkItDown costuma ser pesado em I/O e processamento de documentos, então ThreadPool funciona bem e evita pickling errors.
        with threading.BoundedSemaphore(4): # Limita concorrência para não travar o PC
            def convert_and_update(f):
                convert_single_file(f, remove_header=remove_header, silent=True)
                progress.advance(task)

            threads = []
            for f in files:
                t = threading.Thread(target=convert_and_update, args=(f,))
                t.start()
                threads.append(t)
            
            for t in threads:
                t.join()

    console.print(f"\n[success]{_t('status_lote_fim')}[/success]")

# --- Classes para o Watcher ---
class WatcherHandler(FileSystemEventHandler):
    def __init__(self, remove_header):
        self.remove_header = remove_header
        self.exts = ['.pdf', '.docx', '.pptx', '.xlsx', '.jpg', '.png']

    def on_created(self, event):
        if not event.is_directory:
            f = Path(event.src_path)
            if f.suffix.lower() in self.exts:
                console.print(f"\n[accent]{_t('watcher_detectado').format(f.name)}[/accent]")
                # Espera um pouco para o arquivo terminar de ser escrito pelo SO
                time.sleep(1)
                convert_single_file(f, remove_header=self.remove_header)

def start_watcher(path, remove_header):
    """Inicia o monitoramento de uma pasta."""
    if not Observer:
        console.print(f"[danger]{_t('err_watchdog')}[/danger]")
        return

    event_handler = WatcherHandler(remove_header)
    observer = Observer()
    observer.schedule(event_handler, str(path), recursive=False)
    observer.start()
    
    console.clear()
    draw_header()
    console.print(Panel(f"👀 [bold white]{_t('watcher_monitorando')}[/bold white] [cyan]{path}[/cyan]\n[dim]{_t('watcher_parar')}[/dim]", border_style="green"))
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def show_supported_formats():
    """Exibe a lista de formatos que o MarkItDown suporta."""
    console.clear()
    draw_header()
    console.print()
    
    table = Table(title=_t("fmt_titulo"), show_header=True, header_style="bold magenta")
    table.add_column(_t("fmt_categoria"), style="cyan", width=15)
    table.add_column(_t("fmt_extensoes"), style="white")
    table.add_column(_t("fmt_descricao"), style="dim")
    
    table.add_row(_t("cat_documentos"), "PDF, DOCX, DOC", _t("desc_documentos"))
    table.add_row(_t("cat_planilhas"), "XLSX, XLS, CSV", _t("desc_planilhas"))
    table.add_row(_t("cat_slides"), "PPTX, PPT", _t("desc_slides"))
    table.add_row(_t("cat_web"), "HTML, HTM, URL", _t("desc_web"))
    table.add_row(_t("cat_imagens"), "JPG, PNG, TIFF", _t("desc_imagens"))
    table.add_row(_t("cat_audio"), "MP3, WAV", _t("desc_audio"))
    table.add_row(_t("cat_dados"), "JSON, XML", _t("desc_dados"))
    table.add_row(_t("cat_outros"), "EPUB, ZIP, MSG", _t("desc_outros"))
    
    console.print(table)
    console.print(f"\n[info]{_t('fmt_dica')}[/info]")
    console.input(f"\n[dim]{_t('enter_voltar')}[/dim]")

# --- Funções de UI ---

def draw_header():
    """Desenha o banner ASCII e o cabeçalho estilo terminal."""
    banner_text = [
        ( " ███████ ██ ██      ███████ ", "bold white"), ( "  ██████  ", "bold green"), ( " ███    ███ ██████  ", "bold white" ),
        ( " ██      ██ ██      ██      ", "bold white"), ( "       ██ ", "bold green"), ( " ████  ████ ██   ██ ", "bold white" ),
        ( " █████   ██ ██      █████   ", "bold white"), ( "   █████  ", "bold green"), ( " ██ ████ ██ ██   ██ ", "bold white" ),
        ( " ██      ██ ██      ██      ", "bold white"), ( "  ██      ", "bold green"), ( " ██  ██  ██ ██   ██ ", "bold white" ),
        ( " ██      ██ ███████ ███████ ", "bold white"), ( "  ████████", "bold green"), ( " ██      ██ ██████  ", "bold white" )
    ]
    
    for i in range(0, len(banner_text), 3):
        line = Text()
        line.append(banner_text[i][0], style=banner_text[i][1])
        line.append(banner_text[i+1][0], style=banner_text[i+1][1])
        line.append(banner_text[i+2][0], style=banner_text[i+2][1])
        console.print(line)
    
    console.print() # Linha de espaço entre Banner e Header
 
    header = Text()
    header.append("File", style="header")
    header.append("2", style="success")
    header.append("MD", style="header")
    header.append(_t("header_subtitulo"), style="header")
    
    buttons = Text("  ○ ○ ○", style="dim white")
    header_table = Table.grid(expand=True)
    header_table.add_column(justify="left")
    header_table.add_column(justify="right")
    header_table.add_row(header, buttons)
    
    console.print(Panel(header_table, style="on grey15", padding=(0, 1)))
 
def draw_status_bar():
    """Desenha a barra de status inferior."""
    status = Text("File2MD | v1.0.0 | THIAGO ANDRADE | https://github.com/EuThiagoAndrade/", style="bold white")
    status_table = Table.grid(expand=True)
    status_table.add_column(justify="center")
    status_table.add_row(status)
    console.print(status_table, style="on blue")
 
def preview_last_conversion():
    """Mostra o preview do último arquivo convertido."""
    config = load_config()
    out_dir = config.get("output_dir")
    if not out_dir or not Path(out_dir).exists():
        console.print(f"[warning]{_t('warn_sem_saida')}[/warning]")
        return
 
    md_files = sorted(Path(out_dir).glob("*.md"), key=os.path.getmtime, reverse=True)
    if not md_files:
        console.print(f"[warning]{_t('warn_sem_preview')}[/warning]")
        return
    
    last_file = md_files[0]
    with open(last_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    console.clear()
    console.print(Panel(f"{_t('preview_titulo').format(last_file.name)}", style="bold magenta"))
    console.print(Markdown(content[:2000] + (f"\n\n{_t('preview_truncado')}" if len(content) > 2000 else "")))
    console.input(f"\n[dim]{_t('enter_voltar_curto')}[/dim]")
 
def setup_ai():
    """Configurações de IA."""
    config = load_config()
    console.clear()
    draw_header()
    console.print(f"\n[header]{_t('ai_titulo')}[/header]")
    console.print(f"[info]{_t('ai_subtitulo')}[/info]\n")
    
    enabled = console.input(_t("ai_ativar_prompt").format(_t("sim") if config.get("llm_enabled") else _t("nao"))).lower() in ['s', 'y']
    config["llm_enabled"] = enabled
    
    if enabled:
        config["openai_key"] = console.input(_t("ai_key_prompt")).strip()
        config["openai_base_url"] = console.input(_t("ai_url_prompt")).strip() or None
        config["openai_model"] = console.input(_t("ai_modelo_prompt")).strip() or "gpt-4o"
    
    save_config(config)
    console.print(f"[success]{_t('ai_salvo')}[/success]")
    time.sleep(1)
 
def convert_from_clipboard(remove_header):
    """Tenta converter um caminho ou URL do clipboard."""
    if not pyperclip:
        console.print(f"[danger]{_t('err_pyperclip')}[/danger]")
        return
    
    text = pyperclip.paste().strip().strip('"').strip("'")
    if not text:
        console.print(f"[warning]{_t('warn_clipboard_vazio')}[/warning]")
        return
    
    console.print(f"[info]{_t('clipboard_detectado').format(text)}[/info]")
    if convert_single_file(text, remove_header=remove_header):
        # Opcional: Copiar o resultado de volta para o clipboard?
        pass
 
# --- Menu Principal ---
 
def show_menu():
    config = load_config()
    set_language(config.get("language", "pt"))
    selected_index = 0
    remove_header = True

    while True:
        config = load_config()
        out_dir = config.get("output_dir")
        out_dir_str = out_dir if out_dir else _t("mesma_pasta_origem")
        llm_status = Text.from_markup(f"[bold green] {_t('ia_on')} [/bold green]" if config.get("llm_enabled") else f"[bold dim] {_t('ia_off')} [/bold dim]")
 
        console.clear()
        draw_header()
        
        console.print()
        console.print(f"[menu_opt]{_t('menu_instrucao')}[/menu_opt]\n")
 
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

        for i, option in enumerate(options):
            style = "selected" if i == selected_index else "menu_opt"
            prefix = " ➜ " if i == selected_index else "   "
            
            line = Text(f"{prefix}{option}", style=style)
            
            if _t("menu_yaml") in option:
                line.append(Text(_t("ativada"), style="success") if remove_header else Text(_t("desativada"), style="danger"))
            if _t("menu_ia") in option:
                line.append(llm_status)
                
            console.print(line)
        
        console.print("\n" + "─" * 60, style="dim white")
        console.print(_t("menu_info_saida").format(out_dir_str))
        console.print()
        draw_status_bar()
        
        # Prompt visualmente informativo
        console.print(f"\n [bold blue]➜[/bold blue] [bold white]{_t('escolha')}[/bold white] ", end="")
 
        if msvcrt:
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H': selected_index = (selected_index - 1) % len(options)
                elif key == b'P': selected_index = (selected_index + 1) % len(options)
                continue
            if key == b'\r': opcao = options[selected_index].split('.')[0].strip()
            elif key.isdigit(): opcao = key.decode()
            elif key.lower() == b'i': opcao = '10'
            else: continue
        else:
            try:
                opcao = console.input("\n [bold blue]➜[/bold blue] ").strip()
                if not opcao: continue
            except: break
 
        # Lógica de Execução
        if opcao == '1':
            show_supported_formats()
        elif opcao == '2':
            path = console.input(f"\n[info]{_t('prompt_arquivo_url')}[/info]").strip('"').strip("'")
            if path: convert_single_file(path, remove_header=remove_header)
            console.input(f"\n[dim]{_t('enter_voltar')}[/dim]")
        elif opcao == '3':
            path = console.input(f"\n[info]{_t('prompt_pasta_lote')}[/info]").strip('"').strip("'")
            if path: process_batch(Path(path), remove_header=remove_header)
            console.input(f"\n[dim]{_t('enter_voltar')}[/dim]")
        elif opcao == '4':
            path = console.input(f"\n[info]{_t('prompt_pasta_watcher')}[/info]").strip('"').strip("'")
            if path and Path(path).exists(): start_watcher(Path(path), remove_header)
        elif opcao == '5':
            convert_from_clipboard(remove_header)
            console.input(f"\n[dim]{_t('enter_voltar')}[/dim]")
        elif opcao == '6':
            preview_last_conversion()
        elif opcao == '7':
            setup_ai()
        elif opcao == '8':
            remove_header = not remove_header
        elif opcao == '9':
            path = console.input(f"\n[info]{_t('prompt_pasta_saida')}[/info]").strip('"').strip("'")
            config["output_dir"] = path if path else None
            save_config(config)
            console.print(f"[success]{_t('status_configurado')}[/success]")
            time.sleep(1)
        elif opcao == '10':
            new_lang = "en" if _CURRENT_LANG == "pt" else "pt"
            set_language(new_lang)
            config["language"] = new_lang
            save_config(config)
        elif opcao == '0':
            break
 
def main():
    config = load_config()
    set_language(config.get("language", "pt"))
    parser = argparse.ArgumentParser(description="File2MD Pro - MarkItDown Wrapper")
    parser.add_argument("input", nargs="?", help="Arquivo ou URL")
    parser.add_argument("-o", "--output", help="Saída")
    parser.add_argument("-d", "--directory", action="store_true", help="Modo diretório")
    parser.add_argument("--watch", action="store_true", help="Inicia modo Watcher")
    parser.add_argument("--keep-header", action="store_true", help="Mantém cabeçalho original")
    
    args = parser.parse_args()
    
    if args.watch and args.input:
        start_watcher(Path(args.input), not args.keep_header)
    elif args.input:
        remove_header = not args.keep_header
        if args.directory or Path(args.input).is_dir():
            process_batch(Path(args.input), remove_header)
        else:
            convert_single_file(args.input, args.output, remove_header)
    else:
        show_menu()
 
if __name__ == "__main__":
    main()
