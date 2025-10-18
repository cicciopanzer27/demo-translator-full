#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrattore per documenti PDF nativi (con testo selezionabile)
"""

import fitz  # PyMuPDF
import logging
from typing import List, Dict, Optional, Callable

logger = logging.getLogger(__name__)

class PDFNativeExtractor:
    """Estrattore per PDF nativi con preservazione layout"""
    
    def __init__(self):
        pass
    
    def extract_text_with_layout(self, pdf_path: str, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        Estrae testo da PDF nativo preservando layout
        
        Args:
            pdf_path: Percorso del PDF
            progress_callback: Callback per progress updates
            
        Returns:
            List[Dict]: Lista di pagine con testo e metadati
        """
        
        logger.info(f"Estrazione PDF nativo: {pdf_path}")
        
        try:
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            pages_data = []
            
            logger.info(f"Pagine totali: {total_pages}")
            
            for page_num in range(total_pages):
                if progress_callback:
                    progress_callback(
                        int((page_num / total_pages) * 100),
                        f"Estrazione pagina {page_num + 1}/{total_pages}"
                    )
                
                page = doc[page_num]
                
                # Estrazione con layout dettagliato
                page_data = self._extract_page_with_layout(page, page_num + 1)
                
                if page_data['text'].strip():  # Solo pagine con contenuto
                    pages_data.append(page_data)
                    logger.debug(f"Pagina {page_num + 1}: {len(page_data['text'])} caratteri")
            
            doc.close()
            
            logger.info(f"Estratte {len(pages_data)} pagine con contenuto")
            return pages_data
            
        except Exception as e:
            logger.error(f"Errore estrazione PDF nativo: {e}")
            raise
    
    def _extract_page_with_layout(self, page, page_num: int) -> Dict:
        """
        Estrae una singola pagina con preservazione layout
        
        Args:
            page: Pagina PyMuPDF
            page_num: Numero pagina
            
        Returns:
            Dict con dati della pagina
        """
        
        # Estrazione con layout dettagliato
        text_dict = page.get_text("dict")
        
        # Costruisci testo preservando struttura
        text_blocks = []
        blocks_info = []
        
        for block in text_dict["blocks"]:
            if "lines" in block:
                block_text = ""
                block_info = {
                    'bbox': block.get('bbox', [0, 0, 0, 0]),
                    'lines': []
                }
                
                for line in block["lines"]:
                    line_text = ""
                    line_info = {
                        'bbox': line.get('bbox', [0, 0, 0, 0]),
                        'spans': []
                    }
                    
                    for span in line["spans"]:
                        span_text = span["text"]
                        line_text += span_text
                        
                        line_info['spans'].append({
                            'text': span_text,
                            'bbox': span.get('bbox', [0, 0, 0, 0]),
                            'font': span.get('font', ''),
                            'size': span.get('size', 0),
                            'flags': span.get('flags', 0)
                        })
                    
                    if line_text.strip():
                        block_text += line_text + "\n"
                        block_info['lines'].append(line_info)
                
                if block_text.strip():
                    text_blocks.append(block_text)
                    blocks_info.append(block_info)
        
        # Combina tutto il testo
        full_text = "\n".join(text_blocks)
        
        # Pulisci testo
        cleaned_text = self._clean_text(full_text)
        
        return {
            'page_num': page_num,
            'text': cleaned_text,
            'blocks': blocks_info,
            'char_count': len(cleaned_text),
            'word_count': len(cleaned_text.split())
        }
    
    def _clean_text(self, text: str) -> str:
        """
        Pulisce il testo estratto
        
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

# Test dell'estrattore
if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test con documento demo
    extractor = PDFNativeExtractor()
    
    pdf_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\documents demo\2025-04-30 Physitek Letter [4].pdf"
    
    def progress_callback(percent, message):
        print(f"[{percent:3d}%] {message}")
    
    pages_data = extractor.extract_text_with_layout(pdf_path, progress_callback)
    
    print(f"\nRisultati estrazione:")
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
