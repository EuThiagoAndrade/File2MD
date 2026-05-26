import os
import sys
import argparse
from pathlib import Path

# Adiciona o diretório Scripts ao path de importação para garantir resoluções corretas
sys.path.insert(0, str(Path(__file__).parent))

from utils.config_manager import ConfigManager
from utils.i18n import I18nService
from core.converter import ConverterService
from core.watcher import start_watcher
from ui.components import console, draw_header
from ui.menus import MenuApp

# --- Fachadas de Compatibilidade Retroativa para os Testes Unitários ---
_cm_default = ConfigManager()
_i18n_default = I18nService()

CONFIG_FILE = _cm_default.config_path
_CURRENT_LANG = _i18n_default.current_lang

def load_config():
    """Fachada de compatibilidade para carregar as configurações JSON."""
    _cm_default.config_path = CONFIG_FILE
    return _cm_default.load()

def save_config(config):
    """Fachada de compatibilidade para salvar as configurações JSON."""
    _cm_default.config_path = CONFIG_FILE
    _cm_default.save(config)

def set_language(lang):
    """Fachada de compatibilidade para configurar o idioma ativo."""
    global _CURRENT_LANG
    _i18n_default.set_language(lang)
    _CURRENT_LANG = _i18n_default.current_lang

def _t(key):
    """Fachada de compatibilidade para tradução de chaves."""
    return _i18n_default.translate(key)


# --- Função Principal / Entrypoint CLI ---
def main():
    config_manager = ConfigManager()
    config = config_manager.load()
    
    i18n_service = I18nService(config.get("language", "pt"))
    converter_service = ConverterService(config_manager, i18n_service, console)
    app = MenuApp(config_manager, i18n_service, converter_service, console)
    
    parser = argparse.ArgumentParser(description="File2MD Pro - MarkItDown Wrapper")
    parser.add_argument("input", nargs="?", help="Arquivo ou URL")
    parser.add_argument("-o", "--output", help="Saída")
    parser.add_argument("-d", "--directory", action="store_true", help="Modo diretório")
    parser.add_argument("--watch", action="store_true", help="Inicia modo Watcher")
    parser.add_argument("--keep-header", action="store_true", help="Mantém cabeçalho original")
    
    args = parser.parse_args()
    
    remove_header = not args.keep_header
    
    if args.watch and args.input:
        start_watcher(
            Path(args.input), 
            remove_header, 
            converter_service, 
            console, 
            draw_header_fn=lambda: draw_header(i18n_service.translate)
        )
    elif args.input:
        if args.directory or Path(args.input).is_dir():
            converter_service.process_batch(Path(args.input), remove_header)
        else:
            converter_service.convert_single_file(args.input, args.output, remove_header)
    else:
        app.show_main_menu()

if __name__ == "__main__":
    main()
