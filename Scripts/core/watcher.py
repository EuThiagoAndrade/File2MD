import time
from pathlib import Path
from rich.panel import Panel

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    HAS_WATCHDOG = True
except ImportError:
    Observer = None
    FileSystemEventHandler = object
    HAS_WATCHDOG = False

class WatcherHandler(FileSystemEventHandler):
    """Handler para capturar eventos de criação de arquivo e convertê-los automaticamente."""
    
    def __init__(self, remove_header: bool, converter_service, console):
        super().__init__()
        self.remove_header = remove_header
        self.converter = converter_service
        self.console = console
        self._t = converter_service._t
        self.exts = ['.pdf', '.docx', '.pptx', '.xlsx', '.jpg', '.png']

    def on_created(self, event):
        if not event.is_directory:
            f = Path(event.src_path)
            if f.suffix.lower() in self.exts:
                self.console.print(f"\n[accent]{self._t('watcher_detectado').format(f.name)}[/accent]")
                # Espera um pouco para o arquivo terminar de ser escrito pelo SO
                time.sleep(1)
                self.converter.convert_single_file(f, remove_header=self.remove_header)

def start_watcher(path, remove_header: bool, converter_service, console, draw_header_fn=None) -> None:
    """Inicia o monitoramento de uma pasta utilizando watchdog observer."""
    _t = converter_service._t
    if not Observer:
        console.print(f"[danger]{_t('err_watchdog')}[/danger]")
        return

    event_handler = WatcherHandler(remove_header, converter_service, console)
    observer = Observer()
    observer.schedule(event_handler, str(path), recursive=False)
    observer.start()
    
    console.clear()
    if draw_header_fn:
        draw_header_fn()
    console.print(Panel(f"👀 [bold white]{_t('watcher_monitorando')}[/bold white] [cyan]{path}[/cyan]\n[dim]{_t('watcher_parar')}[/dim]", border_style="green"))
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
