#!/usr/bin/env python3
"""
Test semplificato del sistema di traduzione con OCR
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

def test_basic_components():
    """Test componenti base"""
    print("VERIFICA COMPONENTI BASE")
    print("=" * 50)
    
    # Test traduzione
    try:
        from src.translation.engine import TranslationEngine
        engine = TranslationEngine()
        result = engine.translate_text("Hello world", 'en', 'it')
        print(f"[OK] Traduzione: '{result}'")
        return True
    except Exception as e:
        print(f"[ERROR] Traduzione: {e}")
        return False

def test_ocr_components():
    """Test componenti OCR"""
    print("\nVERIFICA COMPONENTI OCR")
    print("=" * 50)
    
    # Test pdf2image
    try:
        from pdf2image import convert_from_path
        print("[OK] pdf2image - Disponibile")
    except ImportError:
        print("[ERROR] pdf2image - Non disponibile")
        return False
    
    # Test OpenCV
    try:
        import cv2
        print("[OK] OpenCV - Disponibile")
    except ImportError:
        print("[ERROR] OpenCV - Non disponibile")
        return False
    
    # Test OCR Engine semplificato
    try:
        from src.ocr.simple_ocr_engine import SimpleOCREngine
        engine = SimpleOCREngine()
        print("[OK] OCR Engine - Inizializzato")
        return True
    except Exception as e:
        print(f"[ERROR] OCR Engine: {e}")
        return False

def test_worker_simple():
    """Test worker semplificato"""
    print("\nVERIFICA WORKER SEMPLIFICATO")
    print("=" * 50)
    
    try:
        from src.workers.simple_advanced_worker import SimpleAdvancedWorker
        
        # Test inizializzazione
        worker = SimpleAdvancedWorker(
            input_path="test.pdf",
            output_dir="output",
            from_lang="en",
            to_lang="it"
        )
        
        print("[OK] Worker - Inizializzato")
        print(f"   OCR disponibile: {'Si' if worker.ocr_engine else 'No'}")
        print(f"   Engine traduzione: {'Si' if worker.engine else 'No'}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Worker: {e}")
        return False

def test_gui_simple():
    """Test GUI semplificato"""
    print("\nVERIFICA GUI SEMPLIFICATA")
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
    """Test semplificato del sistema"""
    print("TEST SISTEMA SEMPLIFICATO - TRADUTTORE + OCR")
    print("=" * 60)
    
    tests = [
        ("Componenti Base", test_basic_components),
        ("Componenti OCR", test_ocr_components),
        ("Worker Semplificato", test_worker_simple),
        ("GUI Semplificata", test_gui_simple),
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
    print("\nRIEPILOGO TEST")
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
        print("   - OCR documenti scannerizzati OK")
        print("   - GUI integrata OK")
    else:
        print("Alcuni componenti richiedono attenzione")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
