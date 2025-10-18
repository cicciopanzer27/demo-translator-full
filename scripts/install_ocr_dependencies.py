#!/usr/bin/env python3
"""
Script per installare le dipendenze OCR necessarie per documenti scannerizzati
"""

import os
import sys
import subprocess
import logging

# Configurazione encoding per Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def install_package(package_name, description=""):
    """Installa un pacchetto Python"""
    try:
        logger.info(f"Installazione {package_name}...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package_name
        ], capture_output=True, text=True, check=True)
        
        logger.info(f"✅ {package_name} installato con successo")
        if description:
            logger.info(f"   {description}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Errore installazione {package_name}: {e}")
        logger.error(f"   Output: {e.stderr}")
        return False

def main():
    """Installa tutte le dipendenze OCR"""
    logger.info("=" * 60)
    logger.info("INSTALLAZIONE DIPENDENZE OCR PER DOCUMENTI SCANNERIZZATI")
    logger.info("=" * 60)
    
    # Lista dipendenze OCR
    ocr_packages = [
        ("pdf2image", "Estrazione immagini da PDF scannerizzati"),
        ("opencv-python", "Pre-processing immagini (deskewing, denoising)"),
        ("Pillow", "Manipolazione immagini"),
        ("pytesseract", "OCR engine Tesseract"),
        ("easyocr", "OCR engine alternativo"),
        ("transformers", "Modelli TrOCR"),
        ("torch", "PyTorch per modelli AI"),
        ("torchvision", "Vision models"),
        ("layoutparser", "Analisi layout documenti"),
        ("detectron2", "Rilevamento elementi visivi"),
        ("python-docx", "Generazione DOCX"),
        ("reportlab", "Generazione PDF"),
        ("fitz", "PyMuPDF per PDF"),
        ("numpy", "Calcoli numerici"),
        ("scikit-image", "Elaborazione immagini"),
        ("matplotlib", "Visualizzazione"),
    ]
    
    success_count = 0
    total_count = len(ocr_packages)
    
    for package, description in ocr_packages:
        if install_package(package, description):
            success_count += 1
        print()  # Riga vuota per leggibilità
    
    logger.info("=" * 60)
    logger.info(f"INSTALLAZIONE COMPLETATA: {success_count}/{total_count} pacchetti installati")
    
    if success_count == total_count:
        logger.info("🎉 Tutte le dipendenze OCR installate con successo!")
        logger.info("📝 Nota: Potrebbe essere necessario installare Tesseract separatamente")
        logger.info("   Download: https://github.com/UB-Mannheim/tesseract/wiki")
    else:
        logger.warning(f"⚠️  {total_count - success_count} pacchetti non installati")
        logger.info("Controlla i log sopra per dettagli errori")
    
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
