#!/usr/bin/env python3
"""
Test rapido traduzione per verificare che funzioni
"""

import sys
from pathlib import Path
import os

# Fix encoding per Windows console
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Setup path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from translation.engine import TranslationEngine

def test_traduzione():
    """Test traduzione diretta"""
    print("=" * 50)
    print("TEST TRADUZIONE DIRETTA")
    print("=" * 50)
    
    try:
        engine = TranslationEngine()
        
        # Test EN -> IT
        print("Test EN -> IT:")
        test_text = "Hello world, this is a test document."
        result = engine.translate_text(test_text, 'en', 'it')
        print(f"  '{test_text}'")
        print(f"  -> '{result}'")
        print()
        
        # Test IT -> EN
        print("Test IT -> EN:")
        test_text_it = "Ciao mondo, questo è un documento di test."
        result = engine.translate_text(test_text_it, 'it', 'en')
        print(f"  '{test_text_it}'")
        print(f"  -> '{result}'")
        print()
        
        print("[SUCCESS] Traduzione funzionante!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Errore traduzione: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_traduzione()
    sys.exit(0 if success else 1)
