#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Estrattore OCR avanzato basato su progetti opensource
"""

import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import logging
from typing import List, Dict, Tuple
import io

logger = logging.getLogger(__name__)

class AdvancedOCRExtractor:
    """Estrattore OCR avanzato per documenti scansionati"""
    
    def __init__(self):
        self.available_engines = self._check_engines()
        self.preprocessing_enabled = True
        
    def _check_engines(self) -> Dict[str, bool]:
        """Verifica disponibilità engine OCR"""
        engines = {}
        
        try:
            import paddleocr
            engines['paddleocr'] = True
        except ImportError:
            engines['paddleocr'] = False
            
        try:
            import easyocr
            engines['easyocr'] = True
        except ImportError:
            engines['easyocr'] = False
            
        try:
            import pytesseract
            engines['tesseract'] = True
        except ImportError:
            engines['tesseract'] = False
            
        return engines
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocessa immagine per migliorare OCR"""
        if not self.preprocessing_enabled:
            return image
            
        # Converti in scala di grigi
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
            
        # Riduci rumore
        denoised = cv2.medianBlur(gray, 3)
        
        # Migliora contrasto
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # Binarizzazione adattiva
        binary = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        return binary
    
    def extract_with_paddleocr(self, image: np.ndarray) -> List[Dict]:
        """Estrai testo usando PaddleOCR"""
        try:
            from paddleocr import PaddleOCR
            
            ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
            
            # Preprocessa immagine
            processed = self.preprocess_image(image)
            
            # Esegui OCR
            results = ocr.ocr(processed, cls=True)
            
            text_blocks = []
            if results and results[0]:
                for line in results[0]:
                    if line and len(line) >= 2:
                        bbox, (text, confidence) = line
                        text_blocks.append({
                            'text': text,
                            'confidence': confidence,
                            'bbox': bbox,
                            'engine': 'paddleocr'
                        })
            
            return text_blocks
            
        except Exception as e:
            logger.error(f"Errore PaddleOCR: {e}")
            return []
    
    def extract_with_easyocr(self, image: np.ndarray) -> List[Dict]:
        """Estrai testo usando EasyOCR"""
        try:
            import easyocr
            
            reader = easyocr.Reader(['en', 'it'])
            
            # Preprocessa immagine
            processed = self.preprocess_image(image)
            
            # Esegui OCR
            results = reader.readtext(processed)
            
            text_blocks = []
            for bbox, text, confidence in results:
                if confidence > 0.5:  # Filtra risultati a bassa confidenza
                    text_blocks.append({
                        'text': text,
                        'confidence': confidence,
                        'bbox': bbox,
                        'engine': 'easyocr'
                    })
            
            return text_blocks
            
        except Exception as e:
            logger.error(f"Errore EasyOCR: {e}")
            return []
    
    def extract_with_tesseract(self, image: np.ndarray) -> List[Dict]:
        """Estrai testo usando Tesseract"""
        try:
            import pytesseract
            
            # Preprocessa immagine
            processed = self.preprocess_image(image)
            
            # Configurazione per migliore qualità
            config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,;:!?()- '
            
            # Estrai testo
            text = pytesseract.image_to_string(processed, config=config)
            
            # Ottieni dati dettagliati
            data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT)
            
            text_blocks = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 30:  # Filtra confidenza bassa
                    text_blocks.append({
                        'text': data['text'][i],
                        'confidence': int(data['conf'][i]) / 100.0,
                        'bbox': [data['left'][i], data['top'][i], 
                                data['width'][i], data['height'][i]],
                        'engine': 'tesseract'
                    })
            
            return text_blocks
            
        except Exception as e:
            logger.error(f"Errore Tesseract: {e}")
            return []
    
    def extract_text_ensemble(self, image: np.ndarray) -> List[Dict]:
        """Estrai testo usando ensemble di engine OCR"""
        all_results = []
        
        # Prova tutti gli engine disponibili
        if self.available_engines.get('paddleocr'):
            results = self.extract_with_paddleocr(image)
            all_results.extend(results)
            
        if self.available_engines.get('easyocr'):
            results = self.extract_with_easyocr(image)
            all_results.extend(results)
            
        if self.available_engines.get('tesseract'):
            results = self.extract_with_tesseract(image)
            all_results.extend(results)
        
        # Combina risultati (rimuovi duplicati)
        unique_results = []
        seen_texts = set()
        
        for result in all_results:
            text = result['text'].strip()
            if text and text not in seen_texts:
                unique_results.append(result)
                seen_texts.add(text)
        
        return unique_results
    
    def pdf_to_images_high_quality(self, pdf_path: str, dpi: int = 300) -> List[np.ndarray]:
        """Converte PDF in immagini ad alta qualità"""
        doc = fitz.open(pdf_path)
        images = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Matrice di zoom per DPI
            zoom = dpi / 72.0
            mat = fitz.Matrix(zoom, zoom)
            
            # Renderizza pagina
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            # Converti in array numpy
            img = Image.open(io.BytesIO(img_data))
            img_array = np.array(img)
            
            images.append(img_array)
            
        doc.close()
        return images
    
    def extract_from_pdf(self, pdf_path: str) -> List[Dict]:
        """Estrai testo da PDF scansionato"""
        logger.info(f"Estrazione OCR avanzata da: {pdf_path}")
        
        # Converti PDF in immagini
        images = self.pdf_to_images_high_quality(pdf_path)
        logger.info(f"Convertite {len(images)} pagine in immagini")
        
        all_results = []
        
        for i, image in enumerate(images):
            logger.info(f"Processando pagina {i+1}/{len(images)}...")
            
            # Estrai testo con ensemble
            page_results = self.extract_text_ensemble(image)
            
            # Aggiungi numero pagina
            for result in page_results:
                result['page_num'] = i + 1
            
            all_results.extend(page_results)
        
        logger.info(f"Estratti {len(all_results)} blocchi di testo")
        return all_results

if __name__ == "__main__":
    # Test
    extractor = AdvancedOCRExtractor()
    print(f"Engine disponibili: {list(extractor.available_engines.keys())}")
