import sys
import unittest
from pathlib import Path
from rich.console import Console

# Adiciona o diretório Scripts ao path de importação
sys.path.insert(0, str(Path(__file__).parent.parent / "Scripts"))

from utils.config_manager import ConfigManager
from utils.i18n import I18nService
from core.converter import ConverterService
from ui.menus import MenuApp

class TestModularUI(unittest.TestCase):
    def setUp(self):
        self.config_manager = ConfigManager()
        self.i18n_service = I18nService("pt")
        self.console = Console()
        self.converter = ConverterService(self.config_manager, self.i18n_service, self.console)
        self.app = MenuApp(self.config_manager, self.i18n_service, self.converter, self.console)

    def test_app_initialization(self):
        """Valida se o MenuApp é inicializado com as dependências corretas."""
        self.assertEqual(self.app.config_manager, self.config_manager)
        self.assertEqual(self.app.i18n, self.i18n_service)
        self.assertEqual(self.app.converter, self.converter)
        self.assertEqual(self.app.console, self.console)
        self.assertTrue(self.app.remove_header)

if __name__ == '__main__':
    unittest.main()
