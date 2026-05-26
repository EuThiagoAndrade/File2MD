import os
import sys
import unittest
import tempfile
import json
from pathlib import Path
from rich.console import Console

# Adiciona o diretório Scripts ao path de importação
sys.path.insert(0, str(Path(__file__).parent.parent / "Scripts"))

from utils.config_manager import ConfigManager
from utils.i18n import I18nService
from core.postprocess import clean_header, post_process_markdown
from core.converter import ConverterService

class TestModularCore(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_config_path = Path(self.temp_dir.name) / "file2md_config.json"
        self.config_manager = ConfigManager(config_path=self.temp_config_path)
        self.i18n_service = I18nService("pt")
        self.console = Console()
        self.converter = ConverterService(self.config_manager, self.i18n_service, self.console)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_config_manager_load_empty(self):
        """Valida que ConfigManager carrega vazio se o arquivo não existir."""
        config = self.config_manager.load()
        self.assertEqual(config, {})

    def test_config_manager_save_and_load(self):
        """Valida salvamento e carregamento de configurações com ConfigManager."""
        test_data = {"language": "en", "llm_enabled": True}
        self.config_manager.save(test_data)
        config = self.config_manager.load()
        self.assertEqual(config["language"], "en")
        self.assertEqual(config["llm_enabled"], True)

    def test_i18n_service_translations(self):
        """Valida se o I18nService traduz corretamente e faz fallbacks necessários."""
        self.i18n_service.set_language("pt")
        self.assertEqual(self.i18n_service.translate("menu_sair"), "0. Sair")
        
        self.i18n_service.set_language("en")
        self.assertEqual(self.i18n_service.translate("menu_sair"), "0. Exit")

        # Fallback para idioma inexistente
        self.i18n_service.set_language("es")
        self.assertEqual(self.i18n_service.current_lang, "pt")

        # Fallback para chave inexistente
        self.assertEqual(self.i18n_service.translate("non_existent"), "non_existent")

    def test_postprocess_clean_header(self):
        """Valida que clean_header limpa o cabeçalho YAML."""
        content = "---\ntitle: Hello\n---\nReal Content"
        cleaned = clean_header(content)
        self.assertEqual(cleaned, "Real Content")

    def test_postprocess_markdown(self):
        """Valida remoção do cabeçalho YAML e normalização de quebras de linha excessivas."""
        content = "---\ntitle: Test\n---\nLine 1\n\n\n\nLine 2   "
        processed = post_process_markdown(content, remove_header=True)
        self.assertEqual(processed, "Line 1\n\nLine 2")

if __name__ == '__main__':
    unittest.main()
