#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processore principale per documenti legali
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Callable

# Aggiungi il percorso src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from extractors.pdf_native_extractor import PDFNativeExtractor
from extractors.pdf_ocr_extractor import PDFOCRExtractor
from translation_engine import TranslationEngine
from generators.docx_generator import DOCXGenerator

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Processore principale per documenti legali"""
    
    def __init__(self):
        self.native_extractor = PDFNativeExtractor()
        self.ocr_extractor = PDFOCRExtractor()
        self.translation_engine = TranslationEngine()
        self.docx_generator = DOCXGenerator()
        
    def process_document(self, 
                        input_path: str, 
                        output_path: str, 
                        from_lang: str, 
                        to_lang: str,
                        progress_callback: Optional[Callable] = None) -> Dict:
        """
        Processa un documento completo
        
        Args:
            input_path: Percorso del documento PDF
            output_path: Percorso di output DOCX
            from_lang: Lingua sorgente (es. 'en')
            to_lang: Lingua destinazione (es. 'it')
            progress_callback: Callback per progress updates
            
        Returns:
            Dict con risultati del processing
        """
        
        logger.info(f"Avvio processing: {input_path}")
        
        try:
            # 1. Rileva tipo documento
            if progress_callback:
                progress_callback(10, "Rilevamento tipo documento...")
            
            doc_type = self._detect_document_type(input_path)
            logger.info(f"Tipo documento rilevato: {doc_type}")
            
            # 2. Estrai contenuto
            if progress_callback:
                progress_callback(20, f"Estrazione contenuto ({doc_type})...")
            
            if doc_type == "native":
                pages_data = self.native_extractor.extract_text_with_layout(input_path, progress_callback)
            else:  # scanned
                pages_data = self.ocr_extractor.extract_text_with_ocr(input_path, progress_callback)
            
            if not pages_data:
                raise Exception("Nessun contenuto estratto dal documento")
            
            logger.info(f"Estratte {len(pages_data)} pagine con contenuto")
            
            # 3. Traduci contenuto
            if progress_callback:
                progress_callback(60, "Traduzione in corso...")
            
            translated_pages = self.translation_engine.translate_document(
                pages_data, from_lang, to_lang, progress_callback
            )
            
            # 4. Genera documento finale
            if progress_callback:
                progress_callback(90, "Generazione documento finale...")
            
            self.docx_generator.generate_document(translated_pages, output_path)
            
            if progress_callback:
                progress_callback(100, "Completato!")
            
            # Calcola statistiche
            total_chars = sum(len(page.get('translated_text', '')) for page in translated_pages)
            total_words = sum(len(page.get('translated_text', '').split()) for page in translated_pages)
            
            result = {
                'success': True,
                'input_path': input_path,
                'output_path': output_path,
                'doc_type': doc_type,
                'pages_processed': len(translated_pages),
                'total_chars': total_chars,
                'total_words': total_words,
                'from_lang': from_lang,
                'to_lang': to_lang
            }
            
            logger.info(f"Processing completato: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Errore nel processing: {e}")
            if progress_callback:
                progress_callback(0, f"Errore: {str(e)}")
            
            return {
                'success': False,
                'error': str(e),
                'input_path': input_path,
                'output_path': output_path
            }
    
    def _detect_document_type(self, pdf_path: str) -> str:
        """
        Rileva se il documento è nativo o scannerizzato
        
        Args:
            pdf_path: Percorso del PDF
            
        Returns:
            'native' o 'scanned'
        """
        
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            
            # Conta pagine con contenuto significativo
            pages_with_content = 0
            total_chars = 0
            
            for page_num in range(min(total_pages, 5)):  # Controlla prime 5 pagine
                page = doc[page_num]
                text = page.get_text().strip()
                char_count = len(text)
                total_chars += char_count
                
                if char_count > 100:  # Pagina con contenuto significativo
                    pages_with_content += 1
            
            doc.close()
            
            # Se meno del 20% delle pagine ha contenuto, probabilmente è scannerizzato
            content_ratio = pages_with_content / min(total_pages, 5)
            
            if content_ratio < 0.2 or total_chars < 500:
                return "scanned"
            else:
                return "native"
                
        except Exception as e:
            logger.warning(f"Errore nel rilevamento tipo: {e}")
            return "native"  # Default a native se errore

# Test del processore
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test con documento demo
    processor = DocumentProcessor()
    
    input_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\documents demo\2025-04-30 Physitek Letter [4].pdf"
    output_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\output\test_traduzione.docx"
    
    def progress_callback(percent, message):
        print(f"[{percent:3d}%] {message}")
    
    result = processor.process_document(
        input_path=input_path,
        output_path=output_path,
        from_lang='en',
        to_lang='it',
        progress_callback=progress_callback
    )
    
    print(f"\nRisultato: {result}")
