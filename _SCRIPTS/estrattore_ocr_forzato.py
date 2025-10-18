#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrattore con OCR forzato per PDF complessi
"""

import os
import sys
os.environ['PYTHONIOENCODING'] = 'utf-8'

import fitz  # PyMuPDF
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class PDFExtractorOCRForzato:
    """Estrattore PDF con OCR forzato per documenti complessi"""
    
    def __init__(self):
        self.ocr_available = self._check_ocr()
    
    def _check_ocr(self):
        """Verifica se OCR è disponibile"""
        try:
            import easyocr
            return True
        except ImportError:
            print("OCR non disponibile - uso estrazione standard")
            return False
    
    def estrai_con_ocr(self, pdf_path: str) -> List[Dict]:
        """Estrae testo usando OCR su tutte le pagine"""
        
        print(f"Estrazione con OCR: {pdf_path}")
        
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        pages_data = []
        
        print(f"Pagine totali: {total_pages}")
        
        if not self.ocr_available:
            print("OCR non disponibile - uso estrazione standard")
            return self._estrai_standard(doc, total_pages)
        
        try:
            import easyocr
            reader = easyocr.Reader(['en', 'it'])  # Inglese e italiano
            
            for page_num in range(total_pages):
                page = doc[page_num]
                
                print(f"Processando pagina {page_num + 1}/{total_pages}...")
                
                # Converti pagina in immagine
                mat = fitz.Matrix(2.0, 2.0)  # Zoom 2x per migliore qualità
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                
                # OCR sull'immagine
                try:
                    results = reader.readtext(img_data)
                    
                    # Combina tutto il testo estratto
                    text = ""
                    for (bbox, text_extracted, confidence) in results:
                        if confidence > 0.5:  # Soglia di confidenza
                            text += text_extracted + " "
                    
                    # Pulisci il testo
                    cleaned_text = self._pulisci_testo(text)
                    
                    char_count = len(cleaned_text)
                    word_count = len(cleaned_text.split())
                    
                    print(f"  Pagina {page_num + 1}: {char_count} caratteri, {word_count} parole")
                    
                    pages_data.append({
                        'page_num': page_num + 1,
                        'text': cleaned_text,
                        'char_count': char_count,
                        'word_count': word_count,
                        'method': 'OCR',
                        'is_empty': char_count < 100
                    })
                    
                except Exception as e:
                    print(f"  Errore OCR pagina {page_num + 1}: {e}")
                    pages_data.append({
                        'page_num': page_num + 1,
                        'text': "",
                        'char_count': 0,
                        'word_count': 0,
                        'method': 'OCR_FAILED',
                        'is_empty': True
                    })
        
        except Exception as e:
            print(f"Errore OCR: {e}")
            return self._estrai_standard(doc, total_pages)
        
        finally:
            doc.close()
        
        # Filtra pagine con contenuto
        pages_with_content = [p for p in pages_data if not p['is_empty']]
        
        print(f"Pagine con contenuto: {len(pages_with_content)}/{total_pages}")
        
        return pages_with_content
    
    def _estrai_standard(self, doc, total_pages):
        """Estrazione standard come fallback"""
        pages_data = []
        
        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text()
            cleaned_text = self._pulisci_testo(text)
            
            char_count = len(cleaned_text)
            word_count = len(cleaned_text.split())
            
            pages_data.append({
                'page_num': page_num + 1,
                'text': cleaned_text,
                'char_count': char_count,
                'word_count': word_count,
                'method': 'STANDARD',
                'is_empty': char_count < 100
            })
        
        return [p for p in pages_data if not p['is_empty']]
    
    def _pulisci_testo(self, text: str) -> str:
        """Pulisce il testo estratto"""
        if not text:
            return ""
        
        import re
        
        # Rimuovi caratteri di controllo
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Normalizza spazi
        text = re.sub(r'\s+', ' ', text)
        
        # Rimuovi spazi all'inizio e alla fine
        text = text.strip()
        
        return text

def test_ocr_forzato():
    """Test dell'estrazione con OCR forzato"""
    
    pdf_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\documents demo\[2003] MCS TS PAI_Sirio Analtix srl_ DA & AM1 (IND) - FE [2020-Evergreen].pdf"
    
    print("=" * 80)
    print("TEST ESTRATTORE CON OCR FORZATO")
    print("=" * 80)
    
    extractor = PDFExtractorOCRForzato()
    pages_data = extractor.estrai_con_ocr(pdf_path)
    
    print("\n" + "=" * 80)
    print("RISULTATI ESTRACTION CON OCR")
    print("=" * 80)
    
    total_chars = sum(p['char_count'] for p in pages_data)
    total_words = sum(p['word_count'] for p in pages_data)
    
    print(f"Pagine estratte: {len(pages_data)}")
    print(f"Caratteri totali: {total_chars:,}")
    print(f"Parole totali: {total_words:,}")
    
    print("\nDETTAGLIO PAGINE:")
    for page in pages_data:
        print(f"  Pagina {page['page_num']}: {page['char_count']:,} caratteri ({page['method']})")
    
    # Mostra anteprima di ogni pagina
    print("\n" + "=" * 80)
    print("ANTEPRIMA CONTENUTO COMPLETO")
    print("=" * 80)
    
    for i, page in enumerate(pages_data):
        print(f"\n--- PAGINA {page['page_num']} ---")
        preview = page['text'][:500] + "..." if len(page['text']) > 500 else page['text']
        print(preview)
        print(f"Metodo: {page['method']}")

if __name__ == "__main__":
    test_ocr_forzato()
