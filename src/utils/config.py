import json
from pathlib import Path
from typing import Dict, Any

class Config:
    """Gestione configurazione applicazione"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = Path(config_file)
        self.data = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Carica configurazione da file"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Configurazione di default"""
        return {
            'last_source_lang': 'en',
            'last_target_lang': 'it',
            'last_input_dir': '',
            'last_output_dir': '',
            'chunk_size': 500,
            'theme': 'light'
        }
    
    def save(self):
        """Salva configurazione su file"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default=None):
        """Ottieni valore configurazione"""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any):
        """Imposta valore configurazione"""
        self.data[key] = value
        self.save()

