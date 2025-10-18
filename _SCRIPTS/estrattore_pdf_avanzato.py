#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrattore PDF avanzato per documenti con formato complesso
"""

import os
import sys
os.environ['PYTHONIOENCODING'] = 'utf-8'

import fitz  # PyMuPDF
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class PDFExtractorAvanzato:
    """Estrattore PDF per documenti con formato complesso"""
    
    def __init__(self):
        pass
    
    def estrai_con_metodi_multipli(self, pdf_path: str) -> List[Dict]:
        """Prova diversi metodi di estrazione per ogni pagina"""
        
        print(f"Analisi PDF avanzata: {pdf_path}")
        
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        pages_data = []
        
        print(f"Pagine totali: {total_pages}")
        
        for page_num in range(total_pages):
            page = doc[page_num]
            
            # Prova TUTTI i metodi di estrazione
            methods = {
                'standard': page.get_text(),
                'dict': self._estrai_con_dict(page),
                'raw': page.get_text("text"),
                'html': page.get_text("html"),
                'xml': page.get_text("xml"),
                'blocks': self._estrai_con_blocks(page),
                'words': self._estrai_con_words(page)
            }
            
            # Trova il metodo che estrae più testo
            best_method = max(methods.items(), key=lambda x: len(x[1]))
            best_text = best_method[1]
            
            # Pulisci il testo
            cleaned_text = self._pulisci_testo(best_text)
            
            char_count = len(cleaned_text)
            word_count = len(cleaned_text.split())
            
            print(f"Pagina {page_num + 1}: {char_count} caratteri ({best_method[0]})")
            
            pages_data.append({
                'page_num': page_num + 1,
                'text': cleaned_text,
                'char_count': char_count,
                'word_count': word_count,
                'method_used': best_method[0],
                'is_empty': char_count < 100
            })
        
        doc.close()
        
        # Filtra pagine con contenuto
        pages_with_content = [p for p in pages_data if not p['is_empty']]
        
        print(f"Pagine con contenuto: {len(pages_with_content)}/{total_pages}")
        
        return pages_with_content
    
    def _estrai_con_dict(self, page):
        """Estrazione usando get_text('dict')"""
        try:
            text_dict = page.get_text("dict")
            text = ""
            for block in text_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text += span["text"] + " "
                        text += "\n"
            return text
        except:
            return ""
    
    def _estrai_con_blocks(self, page):
        """Estrazione usando blocchi di testo"""
        try:
            blocks = page.get_text("blocks")
            text = ""
            for block in blocks:
                if len(block) >= 5:  # Blocco con testo
                    text += block[4] + "\n"
            return text
        except:
            return ""
    
    def _estrai_con_words(self, page):
        """Estrazione usando parole individuali"""
        try:
            words = page.get_text("words")
            text = ""
            for word in words:
                text += word[4] + " "
            return text
        except:
            return ""
    
    def _pulisci_testo(self, text: str) -> str:
        """Pulisce il testo estratto"""
        if not text:
            return ""
        
        import re
        
        # Rimuovi tag HTML se presenti
        text = re.sub(r'<[^>]+>', '', text)
        
        # Rimuovi caratteri di controllo
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Normalizza spazi
        text = re.sub(r'\s+', ' ', text)
        
        # Rimuovi spazi all'inizio e alla fine
        text = text.strip()
        
        return text

def test_estrazione_avanzata():
    """Test dell'estrazione avanzata"""
    
    pdf_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\documents demo\[2003] MCS TS PAI_Sirio Analtix srl_ DA & AM1 (IND) - FE [2020-Evergreen].pdf"
    
    print("=" * 80)
    print("TEST ESTRATTORE PDF AVANZATO")
    print("=" * 80)
    
    extractor = PDFExtractorAvanzato()
    pages_data = extractor.estrai_con_metodi_multipli(pdf_path)
    
    print("\n" + "=" * 80)
    print("RISULTATI ESTRACTION AVANZATA")
    print("=" * 80)
    
    total_chars = sum(p['char_count'] for p in pages_data)
    total_words = sum(p['word_count'] for p in pages_data)
    
    print(f"Pagine estratte: {len(pages_data)}")
    print(f"Caratteri totali: {total_chars:,}")
    print(f"Parole totali: {total_words:,}")
    
    print("\nDETTAGLIO PAGINE:")
    for page in pages_data:
        print(f"  Pagina {page['page_num']}: {page['char_count']:,} caratteri ({page['method_used']})")
    
    # Mostra anteprima di ogni pagina
    print("\n" + "=" * 80)
    print("ANTEPRIMA CONTENUTO COMPLETO")
    print("=" * 80)
    
    for i, page in enumerate(pages_data):
        print(f"\n--- PAGINA {page['page_num']} ---")
        preview = page['text'][:500] + "..." if len(page['text']) > 500 else page['text']
        print(preview)
        print(f"Metodo: {page['method_used']}")

if __name__ == "__main__":
    test_estrazione_avanzata()
