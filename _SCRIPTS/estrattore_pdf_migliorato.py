#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrattore PDF migliorato per documenti complessi
"""

import os
import sys
os.environ['PYTHONIOENCODING'] = 'utf-8'

import fitz  # PyMuPDF
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class PDFExtractorMigliorato:
    """Estrattore PDF robusto per documenti complessi"""
    
    def __init__(self):
        pass
    
    def estrai_tutto_il_contenuto(self, pdf_path: str) -> List[Dict]:
        """Estrae tutto il contenuto del PDF, anche da pagine 'vuote'"""
        
        print(f"Analisi PDF: {pdf_path}")
        
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        pages_data = []
        
        print(f"Pagine totali nel PDF: {total_pages}")
        
        for page_num in range(total_pages):
            page = doc[page_num]
            
            # Metodo 1: Estrazione standard
            text_standard = page.get_text()
            
            # Metodo 2: Estrazione con layout dettagliato
            text_dict = page.get_text("dict")
            text_blocks = ""
            for block in text_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text_blocks += span["text"] + " "
                        text_blocks += "\n"
            
            # Metodo 3: Estrazione raw
            text_raw = page.get_text("text")
            
            # Scegli il testo più lungo
            texts = [text_standard, text_blocks, text_raw]
            best_text = max(texts, key=len)
            
            # Pulisci il testo
            cleaned_text = self._pulisci_testo(best_text)
            
            # Conta caratteri e parole
            char_count = len(cleaned_text)
            word_count = len(cleaned_text.split())
            
            print(f"Pagina {page_num + 1}: {char_count} caratteri, {word_count} parole")
            
            # Salva anche se sembra "vuota" - potrebbe avere contenuto nascosto
            pages_data.append({
                'page_num': page_num + 1,
                'text': cleaned_text,
                'char_count': char_count,
                'word_count': word_count,
                'is_empty': char_count < 50
            })
        
        doc.close()
        
        # Filtra solo pagine con contenuto significativo
        pages_with_content = [p for p in pages_data if not p['is_empty']]
        
        print(f"Pagine con contenuto: {len(pages_with_content)}/{total_pages}")
        
        return pages_with_content
    
    def _pulisci_testo(self, text: str) -> str:
        """Pulisce il testo estratto"""
        if not text:
            return ""
        
        # Rimuovi caratteri di controllo
        import re
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Normalizza spazi
        text = re.sub(r'\s+', ' ', text)
        
        # Rimuovi spazi all'inizio e alla fine
        text = text.strip()
        
        return text

def test_estrazione():
    """Test dell'estrazione migliorata"""
    
    pdf_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\documents demo\[2003] MCS TS PAI_Sirio Analtix srl_ DA & AM1 (IND) - FE [2020-Evergreen].pdf"
    
    print("=" * 80)
    print("TEST ESTRATTORE PDF MIGLIORATO")
    print("=" * 80)
    
    extractor = PDFExtractorMigliorato()
    pages_data = extractor.estrai_tutto_il_contenuto(pdf_path)
    
    print("\n" + "=" * 80)
    print("RISULTATI ESTRACTION")
    print("=" * 80)
    
    total_chars = sum(p['char_count'] for p in pages_data)
    total_words = sum(p['word_count'] for p in pages_data)
    
    print(f"Pagine estratte: {len(pages_data)}")
    print(f"Caratteri totali: {total_chars:,}")
    print(f"Parole totali: {total_words:,}")
    
    print("\nDETTAGLIO PAGINE:")
    for page in pages_data:
        print(f"  Pagina {page['page_num']}: {page['char_count']:,} caratteri, {page['word_count']:,} parole")
    
    # Mostra anteprima di ogni pagina
    print("\n" + "=" * 80)
    print("ANTEPRIMA CONTENUTO")
    print("=" * 80)
    
    for i, page in enumerate(pages_data[:5]):  # Prime 5 pagine
        print(f"\n--- PAGINA {page['page_num']} ---")
        preview = page['text'][:300] + "..." if len(page['text']) > 300 else page['text']
        print(preview)
    
    if len(pages_data) > 5:
        print(f"\n... e altre {len(pages_data) - 5} pagine")

if __name__ == "__main__":
    test_estrazione()
