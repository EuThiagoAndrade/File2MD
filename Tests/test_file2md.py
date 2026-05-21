import os
import sys
import unittest
import json
import tempfile
from pathlib import Path

# Adiciona o diretório Scripts ao path de importação
sys.path.insert(0, str(Path(__file__).parent.parent / "Scripts"))

import File2MD

class TestFile2MDConfig(unittest.TestCase):
    
    def setUp(self):
        # Configura um arquivo temporário de configuração para evitar alterar as preferências reais do usuário
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_config_path = Path(self.temp_dir.name) / "file2md_config.json"
        
        # Faz mock do CONFIG_FILE no script principal
        self.original_config_file = File2MD.CONFIG_FILE
        File2MD.CONFIG_FILE = self.temp_config_path

    def tearDown(self):
        # Restaura o caminho de configuração original e limpa arquivos temporários
        File2MD.CONFIG_FILE = self.original_config_file
        self.temp_dir.cleanup()

    def test_load_config_empty_when_file_not_exist(self):
        """Valida se load_config retorna um dicionário vazio quando o arquivo não existe."""
        if self.temp_config_path.exists():
            os.remove(self.temp_config_path)
            
        config = File2MD.load_config()
        self.assertEqual(config, {})

    def test_save_and_load_config(self):
        """Valida o fluxo de salvar e carregar as configurações JSON."""
        test_data = {
            "llm_enabled": True,
            "openai_model": "gpt-4o-mini",
            "openai_base_url": "http://localhost:11434/v1"
        }
        
        # Garante que a pasta config existe antes de salvar
        self.temp_config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Salva
        File2MD.save_config(test_data)
        self.assertTrue(self.temp_config_path.exists())
        
        # Carrega e compara
        loaded_data = File2MD.load_config()
        self.assertEqual(loaded_data["llm_enabled"], True)
        self.assertEqual(loaded_data["openai_model"], "gpt-4o-mini")
        self.assertEqual(loaded_data["openai_base_url"], "http://localhost:11434/v1")

    def test_load_config_corrupted_json(self):
        """Valida que load_config trata arquivos JSON corrompidos e retorna um dicionário vazio sem quebrar."""
        self.temp_config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.temp_config_path, 'w', encoding='utf-8') as f:
            f.write("{corrupt_json: invalid}")
            
        config = File2MD.load_config()
        self.assertEqual(config, {})

    def test_default_language_is_pt(self):
        """Valida se o idioma padrão inicial é PT."""
        self.assertEqual(File2MD._CURRENT_LANG, "pt")

    def test_set_language_valid(self):
        """Valida que definir um idioma válido altera _CURRENT_LANG."""
        File2MD.set_language("en")
        self.assertEqual(File2MD._CURRENT_LANG, "en")
        File2MD.set_language("pt")
        self.assertEqual(File2MD._CURRENT_LANG, "pt")

    def test_set_language_invalid_fallback(self):
        """Valida que definir um idioma inválido faz fallback para PT."""
        File2MD.set_language("en")
        File2MD.set_language("es")  # inválido
        self.assertEqual(File2MD._CURRENT_LANG, "pt")

    def test_t_translation_lookup(self):
        """Valida a tradução de chaves conhecidas em PT e EN."""
        File2MD.set_language("pt")
        self.assertEqual(File2MD._t("menu_sair"), "0. Sair")
        
        File2MD.set_language("en")
        self.assertEqual(File2MD._t("menu_sair"), "0. Exit")

    def test_t_fallback_key_itself(self):
        """Valida que uma chave inexistente no dicionário retorna ela mesma."""
        self.assertEqual(File2MD._t("chave_inexistente_123"), "chave_inexistente_123")

if __name__ == '__main__':
    unittest.main()
