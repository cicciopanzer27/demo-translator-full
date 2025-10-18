#!/usr/bin/env python3
"""
Test specifico per documenti demo nella cartella 'documents demo'
Analizza e testa la capacità del sistema di gestire documenti scannerizzati reali
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

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def analyze_document(pdf_path):
    """Analizza un documento PDF"""
    print(f"\n{'='*60}")
    print(f"ANALISI: {Path(pdf_path).name}")
    print(f"{'='*60}")
    
    try:
        # Verifica esistenza
        if not os.path.exists(pdf_path):
            print(f"[ERROR] File non trovato: {pdf_path}")
            return False
        
        # Dimensione file
        size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        print(f"Dimensione: {size_mb:.2f} MB")
        
        # Test estrazione con PyMuPDF
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(pdf_path)
            num_pages = len(doc)
            print(f"Pagine: {num_pages}")
            
            # Analizza prima pagina
            first_page = doc[0]
            text = first_page.get_text()
            
            if len(text.strip()) < 50:
                print("[INFO] Documento probabilmente scannerizzato (poco testo estraibile)")
                print(f"Testo estratto: {len(text)} caratteri")
                
                # Verifica se ha immagini
                images = first_page.get_images()
                print(f"Immagini nella prima pagina: {len(images)}")
                
                if len(images) > 0:
                    print("[CONFERMA] Documento scannerizzato - richiede OCR")
                    return True
            else:
                print("[INFO] Documento nativo con testo selezionabile")
                print(f"Testo estratto: {len(text)} caratteri")
                print(f"Anteprima: {text[:200]}...")
                return True
            
            doc.close()
            
        except Exception as e:
            print(f"[ERROR] Errore analisi PyMuPDF: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Errore generale: {e}")
        return False

def test_ocr_capability():
    """Testa disponibilità componenti OCR"""
    print(f"\n{'='*60}")
    print("VERIFICA CAPACITÀ OCR")
    print(f"{'='*60}")
    
    components = {
        'pdf2image': False,
        'OpenCV': False,
        'EasyOCR': False,
        'Tesseract': False,
        'Pillow': False
    }
    
    # Test pdf2image
    try:
        from pdf2image import convert_from_path
        components['pdf2image'] = True
        print("[OK] pdf2image - Disponibile")
    except ImportError:
        print("[WARN] pdf2image - Non disponibile")
    
    # Test OpenCV
    try:
        import cv2
        components['OpenCV'] = True
        print("[OK] OpenCV - Disponibile")
    except ImportError:
        print("[WARN] OpenCV - Non disponibile")
    
    # Test EasyOCR
    try:
        import easyocr
        components['EasyOCR'] = True
        print("[OK] EasyOCR - Disponibile")
    except ImportError:
        print("[WARN] EasyOCR - Non disponibile")
    
    # Test Tesseract
    try:
        import pytesseract
        components['Tesseract'] = True
        print("[OK] Tesseract - Disponibile")
    except ImportError:
        print("[WARN] Tesseract - Non disponibile")
    
    # Test Pillow
    try:
        from PIL import Image
        components['Pillow'] = True
        print("[OK] Pillow - Disponibile")
    except ImportError:
        print("[WARN] Pillow - Non disponibile")
    
    # Riepilogo
    available = sum(components.values())
    total = len(components)
    print(f"\nComponenti OCR: {available}/{total} disponibili")
    
    if available >= 3:
        print("[OK] Sistema OCR funzionale")
        return True
    else:
        print("[WARN] Installa componenti mancanti con: python scripts/install_ocr_dependencies.py")
        return False

def main():
    """Test documenti demo"""
    print("="*60)
    print("TEST DOCUMENTI DEMO - ANALISI E CAPACITÀ")
    print("="*60)
    
    # Verifica cartella documenti
    docs_dir = Path("documents demo")
    if not docs_dir.exists():
        print(f"[ERROR] Cartella non trovata: {docs_dir}")
        return False
    
    # Lista documenti
    pdf_files = list(docs_dir.glob("*.pdf"))
    print(f"\nTrovati {len(pdf_files)} documenti PDF")
    
    if len(pdf_files) == 0:
        print("[WARN] Nessun documento PDF trovato nella cartella")
        return False
    
    # Test capacità OCR
    ocr_available = test_ocr_capability()
    
    # Analizza ogni documento
    results = []
    for pdf_file in pdf_files:
        result = analyze_document(str(pdf_file))
        results.append((pdf_file.name, result))
    
    # Riepilogo finale
    print(f"\n{'='*60}")
    print("RIEPILOGO ANALISI")
    print(f"{'='*60}")
    
    for filename, result in results:
        status = "[OK]" if result else "[FAIL]"
        print(f"{status} {filename}")
    
    successful = sum(1 for _, r in results if r)
    print(f"\nDocumenti analizzati: {successful}/{len(results)}")
    
    if ocr_available:
        print("\n[INFO] Sistema pronto per tradurre documenti scannerizzati")
    else:
        print("\n[WARN] Installa componenti OCR per documenti scannerizzati")
    
    print("\n[NEXT] Avvia l'applicazione con: python src/main.py")
    print("       Seleziona un documento e testa la traduzione")
    
    return successful == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
