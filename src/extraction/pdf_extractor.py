import fitz  # PyMuPDF
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

# Import OCR modules
try:
    from ..ocr.document_detector import DocumentDetector
    from ..ocr.ocr_engine import OCREngine
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logger.warning("Moduli OCR non disponibili")

class PDFExtractor:
    """Estrae testo da PDF preservando struttura"""
    
    def __init__(self):
        if OCR_AVAILABLE:
            self.detector = DocumentDetector()
            self.ocr_engine = OCREngine()
        else:
            self.detector = None
            self.ocr_engine = None
    
    def extract_text_with_layout(self, pdf_path: str, progress_callback=None) -> List[Dict]:
        """
        Estrae testo pagina per pagina con metadati layout
        
        Returns:
            List[Dict]: [{
                'page_num': int,
                'text': str,
                'blocks': List[Dict],  # Blocchi di testo con posizioni
                'images': List[Dict]
            }]
        """
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        pages_data = []
        
        logger.info(f"Estrazione da PDF: {total_pages} pagine")
        
        for page_num, page in enumerate(doc, 1):
            if progress_callback:
                progress_callback(page_num, total_pages, f"Estrazione pagina {page_num}/{total_pages}")
            
            # Estrai testo con posizioni
            blocks = page.get_text("dict")["blocks"]
            
            # Testo completo della pagina
            page_text = page.get_text("text")
            
            # Metadati immagini (se presenti)
            images = page.get_images()
            
            pages_data.append({
                'page_num': page_num,
                'text': page_text,
                'blocks': blocks,
                'images': images,
                'width': page.rect.width,
                'height': page.rect.height
            })
        
        doc.close()
        logger.info(f"Estratte {total_pages} pagine")
        return pages_data
    
    def extract_simple(self, pdf_path: str) -> str:
        """Estrazione semplice tutto il testo"""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n\n"
        doc.close()
        return text
    
    def extract_intelligent(self, pdf_path: str, progress_callback=None) -> List[Dict]:
        """
        Estrazione intelligente: usa OCR se necessario
        
        Returns:
            List[Dict]: Pagine con testo estratto
        """
        if not OCR_AVAILABLE:
            logger.warning("OCR non disponibile, uso estrazione standard")
            return self.extract_text_with_layout(pdf_path, progress_callback)
        
        # Rileva tipo documento
        logger.info("Rilevamento tipo documento...")
        doc_info = self.detector.detect_document_type(pdf_path)
        
        if progress_callback:
            progress_callback(0, 100, f"Tipo documento: {doc_info['type']} (confidenza: {doc_info['confidence']:.2f})")
        
        if doc_info['type'] == 'text':
            logger.info("Documento con testo nativo - uso estrazione standard")
            return self.extract_text_with_layout(pdf_path, progress_callback)
        
        elif doc_info['type'] == 'scanned':
            logger.info("Documento scansionato - uso OCR")
            return self.extract_with_ocr(pdf_path, progress_callback)
        
        else:  # mixed o unknown
            logger.info("Documento misto - provo estrazione standard, poi OCR se necessario")
            
            # Prova prima estrazione standard
            pages_data = self.extract_text_with_layout(pdf_path, progress_callback)
            
            # Controlla qualità testo estratto
            total_text = sum(len(page['text']) for page in pages_data)
            if total_text < 500:  # Poco testo estratto
                logger.info("Poco testo estratto - uso OCR come backup")
                ocr_pages = self.extract_with_ocr(pdf_path, progress_callback)
                
                # Combina risultati (preferisci OCR se ha più testo)
                ocr_total = sum(len(page['text']) for page in ocr_pages)
                if ocr_total > total_text:
                    logger.info("OCR ha prodotto più testo - uso risultati OCR")
                    return ocr_pages
            
            return pages_data
    
    def extract_with_ocr(self, pdf_path: str, progress_callback=None) -> List[Dict]:
        """Estrazione usando OCR"""
        if not self.ocr_engine or not self.ocr_engine.is_available():
            logger.error("OCR non disponibile")
            return []
        
        logger.info("Inizio estrazione OCR...")
        
        if progress_callback:
            progress_callback(0, 100, "Avvio OCR...")
        
        # Estrai testo con OCR
        ocr_results = self.ocr_engine.extract_text_from_pdf(pdf_path)
        
        if progress_callback:
            progress_callback(50, 100, f"OCR completato: {len(ocr_results)} pagine")
        
        # Converti in formato standard
        pages_data = []
        for result in ocr_results:
            pages_data.append({
                'page_num': result['page_num'],
                'text': result['text'],
                'blocks': [],  # OCR non fornisce layout dettagliato
                'images': [],
                'width': 0,  # Da determinare se necessario
                'height': 0,
                'extraction_method': 'ocr',
                'confidence': result['confidence'],
                'engine': result['engine']
            })
        
        if progress_callback:
            progress_callback(100, 100, f"OCR completato: {len(pages_data)} pagine")
        
        logger.info(f"OCR completato: {len(pages_data)} pagine estratte")
        return pages_data

