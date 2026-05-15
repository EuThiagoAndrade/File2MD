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
            if not silent: console.print(f"[danger]❌ Não encontrado: {input_path}[/danger]")
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
    if not silent: console.print(f"[info]🔄 Processando: {input_path if is_url else input_path.name}...[/info]")
    
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
            if not silent: console.print(f"[success]✅ Salvo em: {output_path}[/success]")
            return True
        return False

    except Exception as e:
        if not silent: console.print(f"[danger]❌ Erro: {e}[/danger]")
        return False

def process_batch(input_path, remove_header=True):
    """Processa múltiplos arquivos em paralelo com barra de progresso."""
    if not input_path.is_dir():
        console.print("[danger]❌ Pasta inválida.[/danger]")
        return

    exts = ['.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', 
            '.jpg', '.png', '.mp3', '.wav', '.html', '.htm', '.csv', 
            '.json', '.xml', '.epub', '.zip', '.msg']
    
    files = [f for f in input_path.glob("*.*") if f.suffix.lower() in exts]
    
    if not files:
        console.print("[warning]⚠️ Nenhum arquivo compatível encontrado na pasta.[/warning]")
        return

    console.print(f"[info]🚀 Iniciando processamento em lote ({len(files)} arquivos)...[/info]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Convertendo...", total=len(files))
        
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

    console.print("\n[success]✨ Processamento em lote concluído![/success]")

# --- Classes para o Watcher ---
class WatcherHandler(FileSystemEventHandler):
    def __init__(self, remove_header):
        self.remove_header = remove_header
        self.exts = ['.pdf', '.docx', '.pptx', '.xlsx', '.jpg', '.png']

    def on_created(self, event):
        if not event.is_directory:
            f = Path(event.src_path)
            if f.suffix.lower() in self.exts:
                console.print(f"\n[accent]🔔 Novo arquivo detectado:[/accent] {f.name}")
                # Espera um pouco para o arquivo terminar de ser escrito pelo SO
                time.sleep(1)
                convert_single_file(f, remove_header=self.remove_header)

def start_watcher(path, remove_header):
    """Inicia o monitoramento de uma pasta."""
    if not Observer:
        console.print("[danger]❌ Erro: Biblioteca 'watchdog' não instalada.[/danger]")
        return

    event_handler = WatcherHandler(remove_header)
    observer = Observer()
    observer.schedule(event_handler, str(path), recursive=False)
    observer.start()
    
    console.clear()
    draw_header()
    console.print(Panel(f"👀 [bold white]Monitorando pasta:[/bold white] [cyan]{path}[/cyan]\n[dim]Pressione Ctrl+C para parar e voltar ao menu.[/dim]", border_style="green"))
    
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
    
    table = Table(title="📄 Formatos Suportados pelo MarkItDown", show_header=True, header_style="bold magenta")
    table.add_column("Categoria", style="cyan", width=15)
    table.add_column("Extensões", style="white")
    table.add_column("Descrição", style="dim")
    
    table.add_row("Documentos", "PDF, DOCX, DOC", "Texto, tabelas e estrutura básica")
    table.add_row("Planilhas", "XLSX, XLS, CSV", "Converte tabelas para formato Markdown")
    table.add_row("Slides", "PPTX, PPT", "Extrai texto e estrutura de slides")
    table.add_row("Web", "HTML, HTM, URL", "Websites, artigos e vídeos do YouTube")
    table.add_row("Imagens", "JPG, PNG, TIFF", "Extrai texto via OCR ou descrição via IA")
    table.add_row("Áudio", "MP3, WAV", "Metadados e transcrição via IA (se configurado)")
    table.add_row("Dados", "JSON, XML", "Formata dados estruturados")
    table.add_row("Outros", "EPUB, ZIP, MSG", "Livros, arquivos compactados e e-mails")
    
    console.print(table)
    console.print("\n[info]💡 Dica: URLs do YouTube podem gerar resumos automáticos.[/info]")
    console.input("\n[dim]Pressione Enter para voltar ao menu...[/dim]")

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
    header.append(" - Wrapper Inteligente para o MarkItDown", style="header")
    
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
        console.print("[warning]⚠️ Pasta de saída não configurada ou vazia.[/warning]")
        return

    md_files = sorted(Path(out_dir).glob("*.md"), key=os.path.getmtime, reverse=True)
    if not md_files:
        console.print("[warning]⚠️ Nenhum arquivo .md encontrado para preview.[/warning]")
        return
    
    last_file = md_files[0]
    with open(last_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    console.clear()
    console.print(Panel(f"📖 Preview: {last_file.name}", style="bold magenta"))
    console.print(Markdown(content[:2000] + ("\n\n... (conteúdo truncado)" if len(content) > 2000 else "")))
    console.input("\n[dim]Pressione Enter para voltar...[/dim]")

def setup_ai():
    """Configurações de IA."""
    config = load_config()
    console.clear()
    draw_header()
    console.print("\n[header]🤖 Configuração de Inteligência Artificial[/header]")
    console.print("[info]Use para descrever imagens e transcrever áudios complexos.[/info]\n")
    
    enabled = console.input(f"Ativar IA? (s/n) [Atual: {'Sim' if config.get('llm_enabled') else 'Não'}]: ").lower() == 's'
    config["llm_enabled"] = enabled
    
    if enabled:
        config["openai_key"] = console.input("OpenAI API Key: ").strip()
        config["openai_base_url"] = console.input("Base URL (Vazio para padrão OpenAI): ").strip() or None
        config["openai_model"] = console.input("Modelo (Padrão: gpt-4o): ").strip() or "gpt-4o"
    
    save_config(config)
    console.print("[success]✅ Configurações de IA salvas![/success]")
    time.sleep(1)

def convert_from_clipboard(remove_header):
    """Tenta converter um caminho ou URL do clipboard."""
    if not pyperclip:
        console.print("[danger]❌ Erro: Biblioteca 'pyperclip' não instalada.[/danger]")
        return
    
    text = pyperclip.paste().strip().strip('"').strip("'")
    if not text:
        console.print("[warning]⚠️ Área de transferência vazia.[/warning]")
        return
    
    console.print(f"[info]📋 Detectado no Clipboard: {text}[/info]")
    if convert_single_file(text, remove_header=remove_header):
        # Opcional: Copiar o resultado de volta para o clipboard?
        pass

# --- Menu Principal ---

def show_menu():
    selected_index = 0
    remove_header = True
    
    options = [
        "1. Ver Formatos de Arquivo Suportados",
        "2. Converter Arquivo Único",
        "3. Converter Pasta em Lote (Lote/Paralelo)",
        "4. Monitorar Pasta (Watcher Mode)",
        "5. Converter do Clipboard (Link ou Caminho)",
        "6. Ver Preview da Última Conversão",
        "7. Configurar IA (OpenAI/Local)",
        "8. Limpeza de Metadados YAML",
        "9. Configurar Pasta de Saída",
        "0. Sair"
    ]

    while True:
        config = load_config()
        out_dir = config.get("output_dir", "Mesma pasta da origem")
        llm_status = Text.from_markup("[bold green] [ IA ON ][/bold green]" if config.get("llm_enabled") else "[bold dim] [ IA OFF ][/bold dim]")

        console.clear()
        draw_header()
        
        console.print()
        console.print("[menu_opt]Navegue com [bold]↑ ↓[/bold] e selecione com [bold]Enter[/bold].[/menu_opt]\n")

        for i, option in enumerate(options):
            style = "selected" if i == selected_index else "menu_opt"
            prefix = " ➜ " if i == selected_index else "   "
            
            line = Text(f"{prefix}{option}", style=style)
            
            if "Limpeza" in option:
                line.append(Text(" [ ATIVADA ]", style="success") if remove_header else Text(" [ DESATIVADA ]", style="danger"))
            if "IA" in option:
                line.append(llm_status)
                
            console.print(line)
        
        console.print("\n" + "─" * 60, style="dim white")
        console.print(f" [info]Saída:[/info] [white]{out_dir}[/white]")
        console.print()
        draw_status_bar()
        
        # Prompt visualmente informativo
        console.print("\n [bold blue]➜[/bold blue] [bold white]Escolha:[/bold white] ", end="")

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
                opcao = console.input("\n [bold blue]➜[/bold blue] ").strip()
                if not opcao: continue
            except: break

        # Lógica de Execução
        if opcao == '1':
            show_supported_formats()
        elif opcao == '2':
            path = console.input("\n[info]Arquivo ou URL: [/info]").strip('"').strip("'")
            if path: convert_single_file(path, remove_header=remove_header)
            console.input("\n[dim]Pressione Enter para continuar...[/dim]")
        elif opcao == '3':
            path = console.input("\n[info]Pasta para Lote: [/info]").strip('"').strip("'")
            if path: process_batch(Path(path), remove_header=remove_header)
            console.input("\n[dim]Pressione Enter para continuar...[/dim]")
        elif opcao == '4':
            path = console.input("\n[info]Pasta para Monitorar: [/info]").strip('"').strip("'")
            if path and Path(path).exists(): start_watcher(Path(path), remove_header)
        elif opcao == '5':
            convert_from_clipboard(remove_header)
            console.input("\n[dim]Pressione Enter para continuar...[/dim]")
        elif opcao == '6':
            preview_last_conversion()
        elif opcao == '7':
            setup_ai()
        elif opcao == '8':
            remove_header = not remove_header
        elif opcao == '9':
            path = console.input("\n[info]Pasta de Saída (Branco para origem): [/info]").strip('"').strip("'")
            config["output_dir"] = path if path else None
            save_config(config)
            console.print("[success]✅ Configurado![/success]")
            time.sleep(1)
        elif opcao == '0':
            break

def main():
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
