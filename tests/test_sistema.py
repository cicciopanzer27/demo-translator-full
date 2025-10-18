#!/usr/bin/env python3
"""
Script di test per verificare che il sistema di traduzione funzioni
"""

import sys
from pathlib import Path
import os

# Fix encoding per Windows console
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Aggiungi src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Test 1: Verifica che tutti i moduli si importino correttamente"""
    print("=" * 60)
    print("TEST 1: Importazione moduli")
    print("=" * 60)
    
    try:
        from translation.engine import TranslationEngine, ModelManager
        print("[OK] Translation engine importato")
        
        from extraction.pdf_extractor import PDFExtractor
        print("[OK] PDF extractor importato")
        
        from extraction.docx_extractor import DOCXExtractor
        print("[OK] DOCX extractor importato")
        
        from generation.pdf_generator import PDFGenerator
        print("[OK] PDF generator importato")
        
        from generation.docx_generator import DOCXGenerator
        print("[OK] DOCX generator importato")
        
        from translation.chunker import DocumentChunker
        print("[OK] Chunker importato")
        
        from workers.translation_worker import TranslationWorker
        print("[OK] Translation worker importato")
        
        from ui.main_window import MainWindow
        print("[OK] Main window importata")
        
        print("\n[SUCCESS] Tutti i moduli importati con successo!\n")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Errore importazione: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_translation_engine():
    """Test 2: Verifica engine traduzione"""
    print("=" * 60)
    print("TEST 2: Engine di traduzione")
    print("=" * 60)
    
    try:
        from translation.engine import TranslationEngine
        
        engine = TranslationEngine()
        print(f"[OK] Engine inizializzato")
        
        languages = engine.get_available_languages()
        print(f"[OK] Lingue disponibili: {len(languages)}")
        
        for lang in languages:
            print(f"  - {lang['code']}: {lang['name']} -> {lang['translations_to']}")
        
        if len(languages) == 0:
            print("\n[WARNING] Nessun modello installato!")
            print("   Usa il dialog 'Gestisci Modelli' nella GUI per installare modelli")
        else:
            print(f"\n[SUCCESS] Engine funzionante con {len(languages)} lingue!\n")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Errore engine: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_gui():
    """Test 3: Verifica GUI"""
    print("=" * 60)
    print("TEST 3: Interfaccia grafica")
    print("=" * 60)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.main_window import MainWindow
        
        print("[OK] PyQt6 importato")
        
        app = QApplication(sys.argv)
        print("[OK] QApplication creata")
        
        window = MainWindow()
        print("[OK] MainWindow creata")
        
        print("\n[SUCCESS] GUI pronta!\n")
        print("Chiudi la finestra per continuare...\n")
        
        window.show()
        app.exec()
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Errore GUI: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Esegui tutti i test"""
    print("\n" + "=" * 60)
    print("TEST SISTEMA TRADUTTORE DOCUMENTI LEGALI")
    print("=" * 60 + "\n")
    
    # Test 1: Import
    if not test_imports():
        print("\n[ERROR] Test fallito: problemi con importazioni")
        return False
    
    # Test 2: Engine
    if not test_translation_engine():
        print("\n[ERROR] Test fallito: problemi con engine traduzione")
        return False
    
    # Test 3: GUI (saltato in modalità automatica)
    print("[SKIP] Test GUI saltato (modalita' automatica)\n")
    print("Per testare la GUI manualmente, esegui: python src/main.py\n")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] TUTTI I TEST COMPLETATI CON SUCCESSO!")
    print("=" * 60 + "\n")
    
    print("Il sistema è pronto per l'uso!")
    print("\nPer avviare l'applicazione:")
    print("  python src/main.py")
    print("\nOppure usa:")
    print("  run.bat        (Windows)")
    print("  ./run.sh       (Linux/Mac)")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

