#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Engine OCR per documenti scansionati
"""

import fitz  # PyMuPDF
import logging
from pathlib import Path
from typing import List, Dict, Optional
import io
from PIL import Image

logger = logging.getLogger(__name__)

class OCREngine:
    """Engine OCR per estrazione testo da documenti scansionati"""
    
    def __init__(self):
        self.available_engines = self._check_available_engines()
        self.primary_engine = self._select_best_engine()
        
        logger.info(f"Engine OCR disponibili: {list(self.available_engines.keys())}")
        logger.info(f"Engine primario: {self.primary_engine}")
    
    def _check_available_engines(self) -> Dict[str, bool]:
        """Verifica quali engine OCR sono disponibili"""
        engines = {}
        
        # Tesseract
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            engines['tesseract'] = True
        except ImportError:
            engines['tesseract'] = False
        except Exception:
            engines['tesseract'] = False
        
        # PaddleOCR
        try:
            import paddleocr
            engines['paddleocr'] = True
        except ImportError:
            engines['paddleocr'] = False
        
        # EasyOCR
        try:
            import easyocr
            engines['easyocr'] = True
        except ImportError:
            engines['easyocr'] = False
        
        return engines
    
    def _select_best_engine(self) -> Optional[str]:
        """Seleziona il miglior engine disponibile"""
        # Priorità: PaddleOCR > EasyOCR > Tesseract
        if self.available_engines.get('paddleocr'):
            return 'paddleocr'
        elif self.available_engines.get('easyocr'):
            return 'easyocr'
        elif self.available_engines.get('tesseract'):
            return 'tesseract'
        else:
            return None
    
    def pdf_to_images(self, pdf_path: str, dpi: int = 300) -> List[Image.Image]:
        """Converte PDF in immagini ad alta risoluzione"""
        try:
            doc = fitz.open(pdf_path)
            images = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Crea matrice di zoom per DPI
                zoom = dpi / 72.0  # 72 DPI è il default di PDF
                mat = fitz.Matrix(zoom, zoom)
                
                # Renderizza pagina come immagine
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                
                # Converti in PIL Image
                img = Image.open(io.BytesIO(img_data))
                images.append(img)
                
                logger.debug(f"Pagina {page_num + 1} convertita in immagine ({img.size})")
            
            doc.close()
            logger.info(f"Convertite {len(images)} pagine in immagini")
            return images
            
        except Exception as e:
            logger.error(f"Errore conversione PDF in immagini: {e}")
            return []
    
    def extract_text_tesseract(self, images: List[Image.Image]) -> List[Dict]:
        """Estrai testo usando Tesseract"""
        try:
            import pytesseract
            
            results = []
            
            for i, img in enumerate(images):
                logger.debug(f"OCR Tesseract pagina {i + 1}...")
                
                # Configurazione per migliore qualità
                custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,;:!?()- '
                
                text = pytesseract.image_to_string(img, config=custom_config)
                
                # Ottieni anche informazioni di layout
                data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                
                results.append({
                    'page_num': i + 1,
                    'text': text.strip(),
                    'confidence': self._calculate_confidence(data),
                    'engine': 'tesseract'
                })
            
            logger.info(f"OCR Tesseract completato: {len(results)} pagine")
            return results
            
        except Exception as e:
            logger.error(f"Errore OCR Tesseract: {e}")
            return []
    
    def extract_text_paddleocr(self, images: List[Image.Image]) -> List[Dict]:
        """Estrai testo usando PaddleOCR"""
        try:
            from paddleocr import PaddleOCR
            
            # Inizializza OCR (inglese + italiano)
            ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
            
            results = []
            
            for i, img in enumerate(images):
                logger.debug(f"OCR PaddleOCR pagina {i + 1}...")
                
                # Converti PIL Image in array numpy
                import numpy as np
                img_array = np.array(img)
                
                # Esegui OCR
                ocr_results = ocr.ocr(img_array, cls=True)
                
                # Estrai testo e confidenza
                text_parts = []
                confidences = []
                
                if ocr_results and ocr_results[0]:
                    for line in ocr_results[0]:
                        if line and len(line) >= 2:
                            text = line[1][0]
                            confidence = line[1][1]
                            text_parts.append(text)
                            confidences.append(confidence)
                
                full_text = '\n'.join(text_parts)
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
                
                results.append({
                    'page_num': i + 1,
                    'text': full_text,
                    'confidence': avg_confidence,
                    'engine': 'paddleocr'
                })
            
            logger.info(f"OCR PaddleOCR completato: {len(results)} pagine")
            return results
            
        except Exception as e:
            logger.error(f"Errore OCR PaddleOCR: {e}")
            return []
    
    def extract_text_easyocr(self, images: List[Image.Image]) -> List[Dict]:
        """Estrai testo usando EasyOCR"""
        try:
            import easyocr
            
            # Inizializza OCR (inglese + italiano)
            reader = easyocr.Reader(['en', 'it'])
            
            results = []
            
            for i, img in enumerate(images):
                logger.debug(f"OCR EasyOCR pagina {i + 1}...")
                
                # Converti PIL Image in array numpy
                import numpy as np
                img_array = np.array(img)
                
                # Esegui OCR
                ocr_results = reader.readtext(img_array)
                
                # Estrai testo e confidenza
                text_parts = []
                confidences = []
                
                for (bbox, text, confidence) in ocr_results:
                    if confidence > 0.5:  # Filtra risultati a bassa confidenza
                        text_parts.append(text)
                        confidences.append(confidence)
                
                full_text = '\n'.join(text_parts)
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
                
                results.append({
                    'page_num': i + 1,
                    'text': full_text,
                    'confidence': avg_confidence,
                    'engine': 'easyocr'
                })
            
            logger.info(f"OCR EasyOCR completato: {len(results)} pagine")
            return results
            
        except Exception as e:
            logger.error(f"Errore OCR EasyOCR: {e}")
            return []
    
    def _calculate_confidence(self, tesseract_data: Dict) -> float:
        """Calcola confidenza media da dati Tesseract"""
        try:
            confidences = []
            for i in range(len(tesseract_data['conf'])):
                conf = int(tesseract_data['conf'][i])
                if conf > 0:  # Ignora confidenze negative
                    confidences.append(conf / 100.0)  # Normalizza 0-1
            
            return sum(confidences) / len(confidences) if confidences else 0.0
            
        except Exception:
            return 0.0
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Estrai testo da PDF usando il miglior engine disponibile
        
        Returns:
            List[Dict]: [
                {
                    'page_num': int,
                    'text': str,
                    'confidence': float,
                    'engine': str
                }
            ]
        """
        if not self.primary_engine:
            logger.error("Nessun engine OCR disponibile")
            return []
        
        logger.info(f"Estrazione OCR con {self.primary_engine}...")
        
        # Converti PDF in immagini
        images = self.pdf_to_images(pdf_path)
        if not images:
            return []
        
        # Estrai testo usando engine primario
        if self.primary_engine == 'paddleocr':
            results = self.extract_text_paddleocr(images)
        elif self.primary_engine == 'easyocr':
            results = self.extract_text_easyocr(images)
        elif self.primary_engine == 'tesseract':
            results = self.extract_text_tesseract(images)
        else:
            logger.error(f"Engine {self.primary_engine} non supportato")
            return []
        
        # Calcola statistiche
        if results:
            total_text = sum(len(r['text']) for r in results)
            avg_confidence = sum(r['confidence'] for r in results) / len(results)
            
            logger.info(f"OCR completato: {len(results)} pagine, {total_text} caratteri, confidenza media: {avg_confidence:.2f}")
        
        return results
    
    def is_available(self) -> bool:
        """Verifica se almeno un engine OCR è disponibile"""
        return self.primary_engine is not None
