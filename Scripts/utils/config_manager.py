from pathlib import Path
import json

class ConfigManager:
    """Gerencia a carga e salvamento das configurações persistentes do File2MD."""
    
    def __init__(self, config_path: Path | None = None):
        # A partir de Scripts/utils/config_manager.py:
        # parent = Scripts/utils
        # parent.parent = Scripts
        # parent.parent.parent = workspace root (onde fica config/)
        self.config_path = config_path or Path(__file__).parent.parent.parent / "config" / "file2md_config.json"

    def load(self) -> dict:
        """Carrega as configurações do arquivo JSON."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save(self, config: dict) -> None:
        """Salva as configurações no arquivo JSON."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
