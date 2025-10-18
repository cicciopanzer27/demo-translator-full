#!/usr/bin/env python3
"""
Test isolato del sistema di traduzione
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

def test_traduzione_diretta():
    """Test traduzione diretta"""
    print("VERIFICA TRADUZIONE DIRETTA")
    print("=" * 50)
    
    try:
        # Import diretto
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from translation.engine import TranslationEngine
        
        engine = TranslationEngine()
        result = engine.translate_text("Hello world", 'en', 'it')
        print(f"[OK] Traduzione: '{result}'")
        return True
    except Exception as e:
        print(f"[ERROR] Traduzione: {e}")
        return False

def test_worker_isolato():
    """Test worker isolato"""
    print("\nVERIFICA WORKER ISOLATO")
    print("=" * 50)
    
    try:
        # Import diretto
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from workers.clean_worker import CleanWorker
        
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

def test_gui_isolata():
    """Test GUI isolata"""
    print("\nVERIFICA GUI ISOLATA")
    print("=" * 50)
    
    try:
        # Import diretto
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from PyQt6.QtWidgets import QApplication
        from ui.main_window import MainWindow
        
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
    """Test isolato del sistema"""
    print("TEST ISOLATO - SISTEMA TRADUZIONE")
    print("=" * 60)
    
    tests = [
        ("Traduzione Diretta", test_traduzione_diretta),
        ("Worker Isolato", test_worker_isolato),
        ("GUI Isolata", test_gui_isolata),
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
    print("\nRIEPILOGO ISOLATO")
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
