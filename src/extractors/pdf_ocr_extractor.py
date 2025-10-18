#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrattore per documenti PDF scannerizzati con OCR
"""

import fitz  # PyMuPDF
import logging
from typing import List, Dict, Optional, Callable
import cv2
import numpy as np
from PIL import Image
import io

logger = logging.getLogger(__name__)

class PDFOCRExtractor:
    """Estrattore per PDF scannerizzati con OCR"""
    
    def __init__(self):
        self.ocr_available = self._check_ocr()
        if not self.ocr_available:
            logger.warning("OCR non disponibile - installare EasyOCR")
    
    def _check_ocr(self) -> bool:
        """Verifica se OCR è disponibile"""
        try:
            import easyocr
            return True
        except ImportError:
            return False
    
    def extract_text_with_ocr(self, pdf_path: str, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        Estrae testo da PDF scannerizzato usando OCR
        
        Args:
            pdf_path: Percorso del PDF
            progress_callback: Callback per progress updates
            
        Returns:
            List[Dict]: Lista di pagine con testo estratto
        """
        
        logger.info(f"Estrazione PDF con OCR: {pdf_path}")
        
        if not self.ocr_available:
            logger.error("OCR non disponibile")
            return []
        
        try:
            import easyocr
            
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            pages_data = []
            
            logger.info(f"Pagine totali: {total_pages}")
            
            # Inizializza OCR reader
            reader = easyocr.Reader(['en', 'it'])  # Inglese e italiano
            
            for page_num in range(total_pages):
                if progress_callback:
                    progress_callback(
                        int((page_num / total_pages) * 100),
                        f"OCR pagina {page_num + 1}/{total_pages}"
                    )
                
                page = doc[page_num]
                
                # Estrai pagina con OCR
                page_data = self._extract_page_with_ocr(page, page_num + 1, reader)
                
                if page_data['text'].strip():  # Solo pagine con contenuto
                    pages_data.append(page_data)
                    logger.debug(f"Pagina {page_num + 1}: {len(page_data['text'])} caratteri")
            
            doc.close()
            
            logger.info(f"Estratte {len(pages_data)} pagine con contenuto")
            return pages_data
            
        except Exception as e:
            logger.error(f"Errore estrazione OCR: {e}")
            raise
    
    def _extract_page_with_ocr(self, page, page_num: int, reader) -> Dict:
        """
        Estrae una singola pagina con OCR
        
        Args:
            page: Pagina PyMuPDF
            page_num: Numero pagina
            reader: Reader EasyOCR
            
        Returns:
            Dict con dati della pagina
        """
        
        try:
            # Converti pagina in immagine ad alta risoluzione
            mat = fitz.Matrix(2.0, 2.0)  # Zoom 2x per migliore qualità
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            # Converti in immagine OpenCV
            img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
            
            # Preprocessing immagine per migliorare OCR
            processed_img = self._preprocess_image(img)
            
            # OCR sull'immagine processata
            try:
                results = reader.readtext(processed_img)
            except Exception as e:
                # Gestisci errori di encoding
                logger.warning(f"Errore OCR pagina {page_num}: {e}")
                results = []
            
            # Combina tutto il testo estratto
            text_blocks = []
            blocks_info = []
            
            for (bbox, text_extracted, confidence) in results:
                if confidence > 0.5:  # Soglia di confidenza
                    text_blocks.append(text_extracted)
                    blocks_info.append({
                        'bbox': bbox,
                        'text': text_extracted,
                        'confidence': confidence
                    })
            
            # Combina testo
            full_text = " ".join(text_blocks)
            
            # Pulisci testo
            cleaned_text = self._clean_text(full_text)
            
            return {
                'page_num': page_num,
                'text': cleaned_text,
                'blocks': blocks_info,
                'char_count': len(cleaned_text),
                'word_count': len(cleaned_text.split()),
                'method': 'OCR'
            }
            
        except Exception as e:
            logger.error(f"Errore OCR pagina {page_num}: {e}")
            return {
                'page_num': page_num,
                'text': "",
                'blocks': [],
                'char_count': 0,
                'word_count': 0,
                'method': 'OCR_FAILED'
            }
    
    def _preprocess_image(self, img: np.ndarray) -> np.ndarray:
        """
        Preprocessing immagine per migliorare OCR
        
        Args:
            img: Immagine OpenCV
            
        Returns:
            np.ndarray: Immagine processata
        """
        
        # Converti in scala di grigi
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Riduci rumore
        denoised = cv2.medianBlur(gray, 3)
        
        # Migliora contrasto
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # Binarizzazione
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def _clean_text(self, text: str) -> str:
        """
        Pulisce il testo estratto da OCR
        
        Args:
            text: Testo da pulire
            
        Returns:
            str: Testo pulito
        """
        
        if not text:
            return ""
        
        import re
        
        # Rimuovi caratteri di controllo
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Normalizza spazi multipli
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Normalizza newline
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Rimuovi spazi all'inizio e alla fine
        text = text.strip()
        
        return text

# Test dell'estrattore OCR
if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test con documento scannerizzato
    extractor = PDFOCRExtractor()
    
    pdf_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\documents demo\Distribution Contract Trotec Bompan SRL_01062024_signed both parties.pdf"
    
    def progress_callback(percent, message):
        print(f"[{percent:3d}%] {message}")
    
    pages_data = extractor.extract_text_with_ocr(pdf_path, progress_callback)
    
    print(f"\nRisultati estrazione OCR:")
    print(f"Pagine estratte: {len(pages_data)}")
    
    total_chars = sum(page['char_count'] for page in pages_data)
    total_words = sum(page['word_count'] for page in pages_data)
    
    print(f"Caratteri totali: {total_chars:,}")
    print(f"Parole totali: {total_words:,}")
    
    # Mostra anteprima prima pagina
    if pages_data:
        print(f"\nAnteprima prima pagina:")
        print("-" * 60)
        preview = pages_data[0]['text'][:500] + "..." if len(pages_data[0]['text']) > 500 else pages_data[0]['text']
        print(preview)
        print("-" * 60)
