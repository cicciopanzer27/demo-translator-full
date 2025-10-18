#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rilevamento tipo documento e gestione OCR
"""

import fitz  # PyMuPDF
import logging
from pathlib import Path
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class DocumentDetector:
    """Rileva se un documento è scansionato o contiene testo nativo"""
    
    def __init__(self):
        self.text_threshold = 100  # Caratteri minimi per considerare "con testo"
        self.page_sample = 3  # Pagine da analizzare
    
    def detect_document_type(self, pdf_path: str) -> Dict:
        """
        Rileva il tipo di documento
        
        Returns:
            {
                'type': 'text' | 'scanned' | 'mixed',
                'confidence': float,
                'text_ratio': float,
                'pages_analyzed': int,
                'total_text_length': int
            }
        """
        try:
            doc = fitz.open(pdf_path)
            total_text_length = 0
            pages_with_text = 0
            pages_analyzed = min(len(doc), self.page_sample)
            
            logger.info(f"Analizzando {pages_analyzed} pagine per tipo documento...")
            
            for page_num in range(pages_analyzed):
                page = doc[page_num]
                
                # Estrai testo
                text = page.get_text()
                text_length = len(text.strip())
                total_text_length += text_length
                
                if text_length > self.text_threshold:
                    pages_with_text += 1
                
                logger.debug(f"Pagina {page_num + 1}: {text_length} caratteri")
            
            doc.close()
            
            # Calcola metriche
            text_ratio = pages_with_text / pages_analyzed if pages_analyzed > 0 else 0
            avg_text_per_page = total_text_length / pages_analyzed if pages_analyzed > 0 else 0
            
            # Determina tipo
            if text_ratio >= 0.8 and avg_text_per_page > 200:
                doc_type = 'text'
                confidence = text_ratio
            elif text_ratio <= 0.2 or avg_text_per_page < 50:
                doc_type = 'scanned'
                confidence = 1.0 - text_ratio
            else:
                doc_type = 'mixed'
                confidence = 0.5
            
            result = {
                'type': doc_type,
                'confidence': confidence,
                'text_ratio': text_ratio,
                'pages_analyzed': pages_analyzed,
                'total_text_length': total_text_length,
                'avg_text_per_page': avg_text_per_page
            }
            
            logger.info(f"Tipo documento rilevato: {doc_type} (confidenza: {confidence:.2f})")
            logger.info(f"Testo medio per pagina: {avg_text_per_page:.0f} caratteri")
            
            return result
            
        except Exception as e:
            logger.error(f"Errore rilevamento tipo documento: {e}")
            return {
                'type': 'unknown',
                'confidence': 0.0,
                'text_ratio': 0.0,
                'pages_analyzed': 0,
                'total_text_length': 0,
                'avg_text_per_page': 0
            }
    
    def get_extraction_strategy(self, pdf_path: str) -> str:
        """
        Determina la strategia di estrazione migliore
        
        Returns:
            'text' - Estrazione testo nativo
            'ocr' - OCR per documenti scansionati
            'hybrid' - Combinazione di entrambi
        """
        doc_info = self.detect_document_type(pdf_path)
        
        if doc_info['type'] == 'text':
            return 'text'
        elif doc_info['type'] == 'scanned':
            return 'ocr'
        else:  # mixed o unknown
            return 'hybrid'
    
    def analyze_text_quality(self, text: str) -> Dict:
        """
        Analizza qualità del testo estratto
        
        Returns:
            {
                'quality_score': float,
                'issues': List[str],
                'readability': float
            }
        """
        issues = []
        quality_score = 1.0
        
        # Controlla problemi comuni
        if len(text.strip()) < 50:
            issues.append('Testo molto breve')
            quality_score -= 0.3
        
        # Controlla caratteri strani (possibili errori OCR)
        strange_chars = sum(1 for c in text if ord(c) > 127 and not c.isalpha())
        if strange_chars > len(text) * 0.1:
            issues.append('Troppi caratteri strani')
            quality_score -= 0.2
        
        # Controlla parole spezzate
        broken_words = text.count('- ') + text.count(' -\n')
        if broken_words > 5:
            issues.append('Parole spezzate')
            quality_score -= 0.1
        
        # Controlla spazi multipli
        multiple_spaces = sum(1 for line in text.split('\n') if '  ' in line)
        if multiple_spaces > 10:
            issues.append('Spaziatura irregolare')
            quality_score -= 0.1
        
        # Calcola leggibilità (rapporto parole/spazi)
        words = text.split()
        readability = len(words) / max(text.count(' '), 1)
        
        return {
            'quality_score': max(0.0, quality_score),
            'issues': issues,
            'readability': readability
        }
