"""
Parser intelligente per documenti legali
Analizza struttura, titoli, paragrafi, tabelle prima della traduzione
"""

import re
from typing import List, Dict, Any, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ElementType(Enum):
    """Tipi di elementi nel documento"""
    TITLE = "title"           # Titolo principale
    HEADING = "heading"       # Titoli di sezione (1.1, 2.3, etc.)
    SUBHEADING = "subheading" # Sottotitoli
    PARAGRAPH = "paragraph"   # Paragrafi normali
    LIST_ITEM = "list_item"   # Elementi di lista
    TABLE_HEADER = "table_header"
    TABLE_ROW = "table_row"
    FOOTNOTE = "footnote"     # Note a piè di pagina
    HEADER = "header"         # Intestazioni
    FOOTER = "footer"         # Piè di pagina
    SIGNATURE = "signature"   # Firme/date
    METADATA = "metadata"     # Metadati (date, numeri, etc.)

class DocumentParser:
    """Parser intelligente per documenti legali"""
    
    def __init__(self):
        # Pattern per riconoscere elementi
        self.patterns = {
            'title': [
                r'^[A-Z][A-Z\s]+$',  # Tutto maiuscolo
                r'^[A-Z][^.]*$',     # Inizia con maiuscola, no punti
            ],
            'heading': [
                r'^\d+\.?\s+[A-Z]',  # 1. Titolo, 2.1 Sezione
                r'^[IVX]+\.?\s+[A-Z]', # Numerazione romana
                r'^[A-Z]\.?\s+[A-Z]',  # A. Sezione
            ],
            'subheading': [
                r'^\d+\.\d+\.?\s+[A-Z]', # 1.1.1 Sottosezione
                r'^[a-z]\)\s+[A-Z]',     # a) Sottotitolo
                r'^\([a-z]+\)\s+[A-Z]',  # (a) Sottotitolo
            ],
            'list_item': [
                r'^[\-\*•]\s+',      # Lista con bullet
                r'^\d+\)\s+',        # Lista numerata
                r'^[a-z]\.\s+',      # Lista alfabetica
            ],
            'signature': [
                r'^[A-Z][a-z]+\s+[A-Z][a-z]+$', # Nome Cognome
                r'^\d{1,2}/\d{1,2}/\d{4}$',     # Date
                r'^Data:\s*\d',                  # Data:
            ],
            'metadata': [
                r'^\d{1,2}/\d{1,2}/\d{4}$',     # Date
                r'^\d{4}$',                      # Anni
                r'^[A-Z]{2,4}-\d+$',            # Codici
                r'^Art\.\s*\d+',                # Articoli
                r'^§\s*\d+',                    # Paragrafi legali
            ]
        }
    
    def parse_document(self, pages_data: List[Dict]) -> List[Dict]:
        """
        Parsa documento e classifica ogni elemento
        
        Args:
            pages_data: Lista pagine con testo
            
        Returns:
            Lista elementi classificati con tipo e metadati
        """
        logger.info("Inizio parsing documento...")
        
        elements = []
        page_num = 1
        
        for page_data in pages_data:
            page_text = page_data.get('text', '')
            page_elements = self._parse_page(page_text, page_num)
            elements.extend(page_elements)
            page_num += 1
        
        # Post-processing per migliorare classificazione
        elements = self._post_process_elements(elements)
        
        logger.info(f"Parsing completato: {len(elements)} elementi classificati")
        return elements
    
    def _parse_page(self, page_text: str, page_num: int) -> List[Dict]:
        """Parsa una singola pagina"""
        lines = page_text.split('\n')
        elements = []
        
        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            element_type = self._classify_line(line)
            
            element = {
                'type': element_type,
                'text': line,
                'page': page_num,
                'line': line_num,
                'length': len(line),
                'metadata': self._extract_metadata(line, element_type)
            }
            
            elements.append(element)
        
        return elements
    
    def _classify_line(self, line: str) -> ElementType:
        """Classifica una riga di testo"""
        # Rimuovi spazi extra
        line = line.strip()
        
        if not line:
            return ElementType.PARAGRAPH
        
        # Controlla pattern in ordine di priorità
        for pattern_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.match(pattern, line):
                    return ElementType(pattern_type)
        
        # Euristics aggiuntive
        if self._is_title_heuristic(line):
            return ElementType.TITLE
        elif self._is_heading_heuristic(line):
            return ElementType.HEADING
        elif self._is_paragraph_heuristic(line):
            return ElementType.PARAGRAPH
        
        # Default
        return ElementType.PARAGRAPH
    
    def _is_title_heuristic(self, line: str) -> bool:
        """Euristics per riconoscere titoli"""
        # Titolo se: tutto maiuscolo + breve + no punteggiatura
        if (line.isupper() and 
            len(line) < 100 and 
            not line.endswith('.') and
            not line.endswith(',') and
            len(line.split()) > 2):
            return True
        
        # Titolo se: inizia con numero romano
        if re.match(r'^[IVX]+\.?\s+', line):
            return True
            
        return False
    
    def _is_heading_heuristic(self, line: str) -> bool:
        """Euristics per riconoscere heading"""
        # Heading se: inizia con numero + punto
        if re.match(r'^\d+\.\s+', line):
            return True
        
        # Heading se: breve + no punteggiatura finale
        if (len(line) < 80 and 
            not line.endswith('.') and
            not line.endswith(',') and
            line[0].isupper()):
            return True
            
        return False
    
    def _is_paragraph_heuristic(self, line: str) -> bool:
        """Euristics per riconoscere paragrafi normali"""
        # Paragrafo se: lungo + punteggiatura
        if (len(line) > 50 and 
            (line.endswith('.') or line.endswith(',') or line.endswith(';'))):
            return True
        
        return False
    
    def _extract_metadata(self, line: str, element_type: ElementType) -> Dict[str, Any]:
        """Estrae metadati specifici dal tipo di elemento"""
        metadata = {}
        
        if element_type == ElementType.HEADING:
            # Estrai numero di sezione
            match = re.match(r'^(\d+(?:\.\d+)*)', line)
            if match:
                metadata['section_number'] = match.group(1)
        
        elif element_type == ElementType.METADATA:
            # Estrai date
            date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', line)
            if date_match:
                metadata['date'] = date_match.group(1)
            
            # Estrai articoli
            art_match = re.search(r'Art\.\s*(\d+)', line)
            if art_match:
                metadata['article'] = art_match.group(1)
        
        elif element_type == ElementType.SIGNATURE:
            # Estrai nomi
            name_match = re.match(r'^([A-Z][a-z]+)\s+([A-Z][a-z]+)', line)
            if name_match:
                metadata['name'] = f"{name_match.group(1)} {name_match.group(2)}"
        
        return metadata
    
    def _post_process_elements(self, elements: List[Dict]) -> List[Dict]:
        """Post-processing per migliorare classificazione"""
        # Raggruppa elementi correlati
        processed = []
        i = 0
        
        while i < len(elements):
            current = elements[i]
            
            # Se è un heading, cerca il paragrafo che segue
            if current['type'] == ElementType.HEADING:
                processed.append(current)
                
                # Raggruppa paragrafi successivi sotto questo heading
                j = i + 1
                while (j < len(elements) and 
                       elements[j]['type'] == ElementType.PARAGRAPH):
                    # Aggiungi riferimento al heading padre
                    elements[j]['parent_heading'] = current['text']
                    processed.append(elements[j])
                    j += 1
                
                i = j
            else:
                processed.append(current)
                i += 1
        
        return processed
    
    def get_translation_groups(self, elements: List[Dict]) -> List[Dict]:
        """
        Raggruppa elementi per traduzione ottimale
        
        Returns:
            Gruppi di elementi da tradurre insieme
        """
        groups = []
        current_group = []
        
        for element in elements:
            # Elementi che devono essere tradotti da soli
            if element['type'] in [ElementType.TITLE, ElementType.HEADING, ElementType.SUBHEADING]:
                if current_group:
                    groups.append({
                        'type': 'paragraph_group',
                        'elements': current_group,
                        'translation_strategy': 'preserve_structure'
                    })
                    current_group = []
                
                groups.append({
                    'type': 'single_element',
                    'element': element,
                    'translation_strategy': 'preserve_formatting'
                })
            
            # Elementi che possono essere raggruppati
            elif element['type'] == ElementType.PARAGRAPH:
                current_group.append(element)
            
            # Altri elementi
            else:
                if current_group:
                    groups.append({
                        'type': 'paragraph_group',
                        'elements': current_group,
                        'translation_strategy': 'preserve_structure'
                    })
                    current_group = []
                
                groups.append({
                    'type': 'single_element',
                    'element': element,
                    'translation_strategy': 'preserve_formatting'
                })
        
        # Aggiungi ultimo gruppo se presente
        if current_group:
            groups.append({
                'type': 'paragraph_group',
                'elements': current_group,
                'translation_strategy': 'preserve_structure'
            })
        
        return groups
