#!/usr/bin/env python3
"""
Script per installare automaticamente i modelli di traduzione essenziali
"""

import sys
from pathlib import Path
import logging
import os

# Fix encoding per Windows console
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Setup path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from translation.engine import ModelManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def install_essential_models():
    """Installa modelli essenziali per traduzione"""
    
    # Coppie essenziali da installare
    essential_pairs = [
        ('en', 'it'),  # Inglese -> Italiano
        ('it', 'en'),  # Italiano -> Inglese
    ]
    
    print("=" * 60)
    print("INSTALLAZIONE MODELLI DI TRADUZIONE ESSENZIALI")
    print("=" * 60)
    print()
    
    # Aggiorna indice pacchetti
    print("1. Aggiornamento indice pacchetti...")
    try:
        ModelManager.update_package_index()
        print("   [OK] Indice aggiornato")
    except Exception as e:
        print(f"   [ERROR] Errore aggiornamento indice: {e}")
        return False
    
    print()
    
    # Installa ogni coppia
    for i, (from_code, to_code) in enumerate(essential_pairs, 1):
        print(f"{i}. Installazione {from_code} -> {to_code}...")
        
        try:
            ModelManager.install_language_pair(
                from_code, 
                to_code,
                progress_callback=lambda v, t, m: print(f"   Progresso: {v}% - {m}")
            )
            print(f"   [OK] {from_code} -> {to_code} installato")
            
        except Exception as e:
            print(f"   [ERROR] Errore installazione {from_code} → {to_code}: {e}")
            continue
    
    print()
    print("=" * 60)
    print("INSTALLAZIONE COMPLETATA")
    print("=" * 60)
    print()
    
    # Verifica installazione
    print("Verifica modelli installati...")
    try:
        from translation.engine import TranslationEngine
        engine = TranslationEngine()
        languages = engine.get_available_languages()
        
        print(f"Lingue disponibili: {len(languages)}")
        for lang in languages:
            print(f"  - {lang['code']}: {lang['name']} → {lang['translations_to']}")
        
        # Test traduzione
        print("\nTest traduzione...")
        test_text = "Hello world"
        try:
            result = engine.translate_text(test_text, 'en', 'it')
            print(f"Test EN->IT: '{test_text}' -> '{result}'")
            print("[OK] Traduzione funzionante!")
        except Exception as e:
            print(f"[ERROR] Test traduzione fallito: {e}")
        
    except Exception as e:
        print(f"[ERROR] Errore verifica: {e}")
    
    print("\n[SUCCESS] Installazione completata!")
    print("Ora puoi usare l'applicazione per tradurre documenti.")
    
    return True

if __name__ == '__main__':
    success = install_essential_models()
    sys.exit(0 if success else 1)
