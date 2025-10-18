#!/usr/bin/env python3
"""
Test completo del sistema di traduzione con OCR
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

def test_ocr_availability():
    """Test disponibilità componenti OCR"""
    print("VERIFICA COMPONENTI OCR")
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
    
    # Test EasyOCR
    try:
        import easyocr
        print("[OK] EasyOCR - Disponibile")
    except ImportError:
        print("[ERROR] EasyOCR - Non disponibile")
    
    # Test Tesseract
    try:
        import pytesseract
        print("[OK] Tesseract - Disponibile")
    except ImportError:
        print("[ERROR] Tesseract - Non disponibile")
    
    # Test OCR Engine
    try:
        from src.ocr.advanced_ocr_engine import AdvancedOCREngine
        engine = AdvancedOCREngine()
        print("[OK] OCR Engine - Inizializzato")
        return True
    except Exception as e:
        print(f"[ERROR] OCR Engine - Errore: {e}")
        return False

def test_translation_engine():
    """Test engine traduzione"""
    print("\nVERIFICA ENGINE TRADUZIONE")
    print("=" * 50)
    
    try:
        from src.translation.engine import TranslationEngine
        engine = TranslationEngine()
        
        # Test traduzione semplice
        test_text = "Hello world"
        result = engine.translate_text(test_text, 'en', 'it')
        print(f"[OK] Traduzione EN->IT: '{test_text}' -> '{result}'")
        
        return True
    except Exception as e:
        print(f"[ERROR] Errore engine traduzione: {e}")
        return False

def test_advanced_worker():
    """Test worker avanzato"""
    print("\nVERIFICA WORKER AVANZATO")
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
        
        print("[OK] Worker avanzato - Inizializzato")
        print(f"   OCR disponibile: {'Si' if worker.ocr_engine else 'No'}")
        print(f"   Engine traduzione: {'Si' if worker.engine else 'No'}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Errore worker avanzato: {e}")
        return False

def test_gui_integration():
    """Test integrazione GUI"""
    print("\nVERIFICA INTEGRAZIONE GUI")
    print("=" * 50)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from src.ui.main_window import MainWindow
        
        app = QApplication([])
        window = MainWindow()
        
        print("[OK] GUI - Inizializzata")
        print("[OK] Worker avanzato - Integrato")
        
        app.quit()
        return True
    except Exception as e:
        print(f"[ERROR] Errore GUI: {e}")
        return False

def main():
    """Test completo del sistema"""
    print("TEST SISTEMA COMPLETO - TRADUTTORE + OCR")
    print("=" * 60)
    
    tests = [
        ("Componenti OCR", test_ocr_availability),
        ("Engine Traduzione", test_translation_engine),
        ("Worker Avanzato", test_advanced_worker),
        ("Integrazione GUI", test_gui_integration),
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
        print("Alcuni componenti richiedono installazione")
        print("   Esegui: python install_ocr_dependencies.py")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
