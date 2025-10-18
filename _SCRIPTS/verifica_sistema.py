#!/usr/bin/env python3
"""
Verifica finale del sistema completo
"""

import os
import sys
from pathlib import Path

# Configurazione encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

def check_item(name, condition, details=""):
    """Stampa risultato verifica"""
    status = "[OK]" if condition else "[FAIL]"
    print(f"{status} {name}")
    if details:
        print(f"     {details}")
    return condition

def main():
    print("="*60)
    print("VERIFICA SISTEMA COMPLETO")
    print("="*60)
    print()
    
    all_ok = True
    
    # Verifica struttura
    print("STRUTTURA PROGETTO:")
    all_ok &= check_item("Cartella src", Path("src").exists())
    all_ok &= check_item("Cartella documents demo", Path("documents demo").exists())
    all_ok &= check_item("Cartella tests", Path("tests").exists())
    all_ok &= check_item("Cartella scripts", Path("scripts").exists())
    all_ok &= check_item("Cartella docs", Path("docs").exists())
    print()
    
    # Verifica documenti demo
    print("DOCUMENTI DEMO:")
    demo_files = list(Path("documents demo").glob("*.pdf"))
    all_ok &= check_item(f"PDF trovati", len(demo_files) >= 4, f"{len(demo_files)} file")
    print()
    
    # Verifica componenti Python
    print("COMPONENTI PYTHON:")
    
    try:
        from src.translation.engine import TranslationEngine
        all_ok &= check_item("Engine traduzione", True)
    except:
        all_ok &= check_item("Engine traduzione", False)
    
    try:
        from src.workers.clean_worker import CleanWorker
        all_ok &= check_item("Worker traduzione", True)
    except:
        all_ok &= check_item("Worker traduzione", False)
    
    try:
        from src.ui.main_window import MainWindow
        all_ok &= check_item("GUI principale", True)
    except:
        all_ok &= check_item("GUI principale", False)
    
    print()
    
    # Verifica componenti OCR
    print("COMPONENTI OCR:")
    
    try:
        from pdf2image import convert_from_path
        all_ok &= check_item("pdf2image", True)
    except:
        all_ok &= check_item("pdf2image", False)
    
    try:
        import cv2
        all_ok &= check_item("OpenCV", True)
    except:
        all_ok &= check_item("OpenCV", False)
    
    try:
        import easyocr
        all_ok &= check_item("EasyOCR", True)
    except:
        all_ok &= check_item("EasyOCR", False)
    
    try:
        import pytesseract
        all_ok &= check_item("Tesseract", True)
    except:
        all_ok &= check_item("Tesseract", False)
    
    print()
    
    # Verifica file essenziali
    print("FILE ESSENZIALI:")
    all_ok &= check_item("README.md", Path("README.md").exists())
    all_ok &= check_item("TUTTO_PRONTO.txt", Path("TUTTO_PRONTO.txt").exists())
    all_ok &= check_item("CREA_ICONA_DESKTOP.bat", Path("CREA_ICONA_DESKTOP.bat").exists())
    all_ok &= check_item("run.bat", Path("run.bat").exists())
    print()
    
    # Riepilogo finale
    print("="*60)
    if all_ok:
        print("[SUCCESS] SISTEMA COMPLETO E PRONTO!")
        print()
        print("Prossimi passi:")
        print("1. Esegui: CREA_ICONA_DESKTOP.bat")
        print("2. Avvia il traduttore dall'icona desktop")
        print("3. Testa con i documenti in 'documents demo'")
    else:
        print("[WARNING] Alcuni componenti mancanti")
        print()
        print("Azioni consigliate:")
        print("1. Installa modelli: python scripts\\install_models.py")
        print("2. Installa OCR: python scripts\\install_ocr_dependencies.py")
    
    print("="*60)
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
