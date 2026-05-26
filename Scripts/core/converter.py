import os
import subprocess
import threading
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

# Tenta importar MarkItDown e OpenAI
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

from core.postprocess import post_process_markdown
from utils.config_manager import ConfigManager
from utils.i18n import I18nService

class ConverterService:
    """Serviço que gerencia as operações de conversão de arquivos e diretórios."""

    def __init__(self, config_manager: ConfigManager, i18n_service: I18nService, console: Console):
        self.config_manager = config_manager
        self.i18n = i18n_service
        self.console = console
        self._t = i18n_service.translate

    def get_markitdown_instance(self):
        """Inicializa a instância do MarkItDown com suporte a LLM se configurado."""
        if not HAS_MARKITDOWN_API:
            return None
        
        config = self.config_manager.load()
        llm_enabled = config.get("llm_enabled", False)
        
        if llm_enabled and HAS_OPENAI:
            try:
                client = OpenAI(
                    api_key=config.get("openai_key"),
                    base_url=config.get("openai_base_url") # Para Ollama ou local
                )
                return MarkItDown(llm_client=client, llm_model=config.get("openai_model", "gpt-4o"))
            except Exception:
                return MarkItDown()
        
        return MarkItDown()

    def convert_single_file(self, input_path, output_path=None, remove_header=True, silent=False) -> bool:
        """Converte um arquivo individual usando API ou Subprocess."""
        config = self.config_manager.load()
        default_out_dir = config.get("output_dir")
        
        is_url = str(input_path).startswith(('http://', 'https://'))
        
        if not is_url:
            input_path = Path(input_path)
            if not input_path.exists():
                if not silent: 
                    self.console.print(f"[danger]{self._t('err_nao_encontrado').format(input_path)}[/danger]")
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
        if not silent: 
            self.console.print(f"[info]{self._t('status_processando').format(input_path if is_url else input_path.name)}[/info]")
        
        try:
            content = ""
            # Prioridade 1: API Nativa
            if HAS_MARKITDOWN_API:
                md = self.get_markitdown_instance()
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
                if not silent: 
                    self.console.print(f"[success]{self._t('status_salvo').format(output_path)}[/success]")
                return True
            return False

        except Exception as e:
            if not silent: 
                self.console.print(f"[danger]{self._t('err_erro').format(e)}[/danger]")
            return False

    def process_batch(self, input_path, remove_header=True) -> None:
        """Processa múltiplos arquivos em paralelo com barra de progresso."""
        if not input_path.is_dir():
            self.console.print(f"[danger]{self._t('err_pasta_invalida')}[/danger]")
            return

        exts = ['.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', 
                '.jpg', '.png', '.mp3', '.wav', '.html', '.htm', '.csv', 
                '.json', '.xml', '.epub', '.zip', '.msg']
        
        files = [f for f in input_path.glob("*.*") if f.suffix.lower() in exts]
        
        if not files:
            self.console.print(f"[warning]{self._t('warn_nenhum_arquivo')}[/warning]")
            return

        self.console.print(f"[info]{self._t('status_lote_inicio').format(len(files))}[/info]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task(self._t("status_lote_convertendo"), total=len(files))
            
            with threading.BoundedSemaphore(4): # Limita concorrência para não travar o PC
                def convert_and_update(f):
                    self.convert_single_file(f, remove_header=remove_header, silent=True)
                    progress.advance(task)

                threads = []
                for f in files:
                    t = threading.Thread(target=convert_and_update, args=(f,))
                    t.start()
                    threads.append(t)
                
                for t in threads:
                    t.join()

        self.console.print(f"\n[success]{self._t('status_lote_fim')}[/success]")
