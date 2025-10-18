#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generatore DOCX con preservazione layout
"""

import logging
from typing import List, Dict
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

logger = logging.getLogger(__name__)

class DOCXGenerator:
    """Generatore DOCX con preservazione layout"""
    
    def __init__(self):
        pass
    
    def generate_document(self, translated_pages: List[Dict], output_path: str) -> None:
        """
        Genera documento DOCX da pagine tradotte
        
        Args:
            translated_pages: Lista di pagine tradotte
            output_path: Percorso di output
        """
        
        logger.info(f"Generazione DOCX: {output_path}")
        
        try:
            # Crea nuovo documento
            doc = Document()
            
            # Setup margini e stili
            self._setup_document_styles(doc)
            
            # Aggiungi contenuto per ogni pagina
            for page_data in translated_pages:
                self._add_page_content(doc, page_data)
            
            # Salva documento
            doc.save(output_path)
            
            logger.info(f"Documento salvato: {output_path}")
            
        except Exception as e:
            logger.error(f"Errore generazione DOCX: {e}")
            raise
    
    def _setup_document_styles(self, doc: Document) -> None:
        """Setup stili del documento"""
        
        # Margini
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
        
        # Stile per titoli
        try:
            title_style = doc.styles.add_style('CustomTitle', WD_STYLE_TYPE.PARAGRAPH)
            title_style.font.name = 'Arial'
            title_style.font.size = Pt(14)
            title_style.font.bold = True
            title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        except:
            pass  # Stile già esistente
        
        # Stile per testo normale
        try:
            normal_style = doc.styles.add_style('CustomNormal', WD_STYLE_TYPE.PARAGRAPH)
            normal_style.font.name = 'Arial'
            normal_style.font.size = Pt(11)
            normal_style.paragraph_format.space_after = Pt(6)
        except:
            pass  # Stile già esistente
    
    def _add_page_content(self, doc: Document, page_data: Dict) -> None:
        """Aggiunge contenuto di una pagina al documento"""
        
        try:
            translated_text = page_data.get('translated_text', '')
            
            if not translated_text.strip():
                return
            
            # Dividi in paragrafi
            paragraphs = translated_text.split('\n\n')
            
            for para_text in paragraphs:
                if para_text.strip():
                    # Crea paragrafo
                    para = doc.add_paragraph()
                    
                    # Applica stile appropriato
                    if self._is_title(para_text):
                        para.style = 'CustomTitle'
                    else:
                        para.style = 'CustomNormal'
                    
                    # Aggiungi testo
                    para.add_run(para_text.strip())
            
            # Aggiungi separatore tra pagine (se non è l'ultima pagina)
            if page_data.get('page_num', 0) > 0:
                doc.add_paragraph()
                doc.add_paragraph("─" * 50)
                doc.add_paragraph()
            
        except Exception as e:
            logger.error(f"Errore aggiunta contenuto pagina: {e}")
    
    def _is_title(self, text: str) -> bool:
        """
        Determina se un testo è un titolo
        
        Args:
            text: Testo da analizzare
            
        Returns:
            bool: True se è un titolo
        """
        
        text = text.strip()
        
        # Criteri per identificare titoli
        if len(text) < 5:
            return False
        
        if len(text) > 100:
            return False
        
        # Controlla se è tutto maiuscolo
        if text.isupper() and len(text) > 10:
            return True
        
        # Controlla se inizia con numeri (es. "1. TITOLO")
        if text[0].isdigit() and '.' in text[:10]:
            return True
        
        # Controlla parole chiave comuni nei titoli
        title_keywords = [
            'AGREEMENT', 'CONTRACT', 'AMENDMENT', 'TERMS', 'CONDITIONS',
            'WARRANTY', 'LIABILITY', 'PAYMENT', 'DELIVERY', 'TERMINATION'
        ]
        
        for keyword in title_keywords:
            if keyword in text.upper():
                return True
        
        return False

# Test del generatore
if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test con dati di esempio
    generator = DOCXGenerator()
    
    test_pages = [
        {
            'page_num': 1,
            'translated_text': "CONTRATTO DI DISTRIBUZIONE\n\nQuesto contratto stabilisce i termini e le condizioni per la distribuzione dei prodotti.",
            'char_count': 100,
            'word_count': 20
        },
        {
            'page_num': 2,
            'translated_text': "TERMINI E CONDIZIONI\n\n1. Il distributore si impegna a vendere i prodotti secondo le specifiche tecniche.\n\n2. Il pagamento deve essere effettuato entro 30 giorni dalla consegna.",
            'char_count': 150,
            'word_count': 30
        }
    ]
    
    output_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\output\test_generazione.docx"
    
    # Crea cartella output se non esiste
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    generator.generate_document(test_pages, output_path)
    
    print(f"Documento generato: {output_path}")
