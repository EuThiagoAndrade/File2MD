from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.theme import Theme

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

# Ponto único de instanciação do Console
console = Console(theme=custom_theme)

def draw_header(translate_fn=None) -> None:
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
    
    subtitulo = translate_fn("header_subtitulo") if translate_fn else " - Wrapper Inteligente para o MarkItDown"
    header.append(subtitulo, style="header")
    
    buttons = Text("  ○ ○ ○", style="dim white")
    header_table = Table.grid(expand=True)
    header_table.add_column(justify="left")
    header_table.add_column(justify="right")
    header_table.add_row(header, buttons)
    
    console.print(Panel(header_table, style="on grey15", padding=(0, 1)))

def draw_status_bar() -> None:
    """Desenha a barra de status inferior."""
    status = Text("File2MD | v1.0.0 | THIAGO ANDRADE | https://github.com/EuThiagoAndrade/", style="bold white")
    status_table = Table.grid(expand=True)
    status_table.add_column(justify="center")
    status_table.add_row(status)
    console.print(status_table, style="on blue")
