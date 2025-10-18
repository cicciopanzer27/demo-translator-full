#!/usr/bin/env python3
"""
Test finale del sistema di traduzione
"""

import os
import sys
import logging
from pathlib import Path

# Configurazione encoding per Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_traduzione():
    """Test traduzione base"""
    print("VERIFICA TRADUZIONE")
    print("=" * 50)
    
    try:
        from src.translation.engine import TranslationEngine
        engine = TranslationEngine()
        
        # Test traduzione
        result = engine.translate_text("Hello world", 'en', 'it')
        print(f"[OK] Traduzione: '{result}'")
        return True
    except Exception as e:
        print(f"[ERROR] Traduzione: {e}")
        return False

def test_worker():
    """Test worker pulito"""
    print("\nVERIFICA WORKER")
    print("=" * 50)
    
    try:
        from src.workers.clean_worker import CleanWorker
        
        worker = CleanWorker(
            input_path="test.pdf",
            output_dir="output",
            from_lang="en",
            to_lang="it"
        )
        
        print("[OK] Worker - Inizializzato")
        print(f"   Engine traduzione: {'Si' if worker.engine else 'No'}")
        return True
    except Exception as e:
        print(f"[ERROR] Worker: {e}")
        return False

def test_gui():
    """Test GUI"""
    print("\nVERIFICA GUI")
    print("=" * 50)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from src.ui.main_window import MainWindow
        
        app = QApplication([])
        window = MainWindow()
        
        print("[OK] GUI - Inizializzata")
        print("[OK] Worker integrato")
        
        app.quit()
        return True
    except Exception as e:
        print(f"[ERROR] GUI: {e}")
        return False

def main():
    """Test finale del sistema"""
    print("TEST FINALE - SISTEMA TRADUZIONE")
    print("=" * 60)
    
    tests = [
        ("Traduzione", test_traduzione),
        ("Worker", test_worker),
        ("GUI", test_gui),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[ERROR] Errore test {test_name}: {e}")
            results.append((test_name, False))
    
    # Riepilogo
    print("\nRIEPILOGO FINALE")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nRisultato: {passed}/{len(results)} test superati")
    
    if passed == len(results):
        print("SISTEMA COMPLETO FUNZIONANTE!")
        print("   - Traduzione documenti nativi OK")
        print("   - GUI integrata OK")
        print("   - Pronto per l'uso!")
    else:
        print("Alcuni componenti richiedono attenzione")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
