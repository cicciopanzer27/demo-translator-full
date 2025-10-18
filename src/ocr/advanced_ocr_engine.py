#!/usr/bin/env python3
"""
Sistema OCR avanzato per documenti scannerizzati
Basato su blueprint.md per documenti legali
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import logging
from typing import List, Dict, Tuple, Optional
import tempfile
import shutil

# OCR engines
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logging.warning("Tesseract non disponibile")

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    logging.warning("EasyOCR non disponibile")

# LayoutParser (opzionale)
try:
    import layoutparser
    LAYOUTPARSER_AVAILABLE = True
except ImportError:
    LAYOUTPARSER_AVAILABLE = False
    logging.warning("LayoutParser non disponibile")

# PDF processing
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False
    logging.warning("pdf2image non disponibile")

logger = logging.getLogger(__name__)

class AdvancedOCREngine:
    """Engine OCR avanzato per documenti scannerizzati"""
    
    def __init__(self):
        self.easyocr_reader = None
        self._init_engines()
    
    def _init_engines(self):
        """Inizializza engine OCR"""
        if EASYOCR_AVAILABLE:
            try:
                # EasyOCR per italiano e inglese
                self.easyocr_reader = easyocr.Reader(['it', 'en'], gpu=False)
                logger.info("EasyOCR inizializzato")
            except Exception as e:
                logger.error(f"Errore inizializzazione EasyOCR: {e}")
                self.easyocr_reader = None
        
        if TESSERACT_AVAILABLE:
            # Configurazione Tesseract per italiano
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            logger.info("Tesseract configurato")
    
    def extract_images_from_pdf(self, pdf_path: str, dpi: int = 300) -> List[np.ndarray]:
        """Estrae immagini da PDF scannerizzato"""
        if not PDF2IMAGE_AVAILABLE:
            raise ImportError("pdf2image non disponibile")
        
        logger.info(f"Estrazione immagini da PDF: {pdf_path}")
        
        try:
            # Estrai immagini dal PDF
            images = convert_from_path(
                pdf_path,
                dpi=dpi,
                fmt='PNG',
                thread_count=os.cpu_count(),
                grayscale=False,
                use_pdftocairo=True
            )
            
            # Converti PIL Images in numpy arrays
            cv_images = []
            for i, pil_image in enumerate(images):
                # Converti PIL -> numpy array -> OpenCV
                cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                cv_images.append(cv_image)
                logger.debug(f"Pagina {i+1}: {cv_image.shape}")
            
            logger.info(f"Estratte {len(cv_images)} pagine")
            return cv_images
            
        except Exception as e:
            logger.error(f"Errore estrazione PDF: {e}")
            raise
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Pre-processing avanzato per migliorare qualità OCR"""
        logger.debug("Pre-processing immagine...")
        
        # 1. Converti in scala di grigi
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # 2. Raddrizzamento (deskewing)
        gray = self._deskew_image(gray)
        
        # 3. Denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # 4. Enhancement contrasto
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # 5. Binarizzazione adattiva
        binary = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # 6. Morfologia per pulire il testo
        kernel = np.ones((1,1), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def _deskew_image(self, image: np.ndarray) -> np.ndarray:
        """Raddrizza immagine inclinata"""
        try:
            # Trova contorni
            coords = np.column_stack(np.where(image > 0))
            if len(coords) == 0:
                return image
            
            # Calcola angolo di inclinazione
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = 90 + angle
            
            # Ruota immagine
            if abs(angle) > 0.5:  # Solo se inclinazione significativa
                (h, w) = image.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                return rotated
            
            return image
        except Exception as e:
            logger.warning(f"Errore deskewing: {e}")
            return image
    
    def extract_text_easyocr(self, image: np.ndarray) -> List[Dict]:
        """Estrae testo usando EasyOCR"""
        if not self.easyocr_reader:
            return []
        
        try:
            results = self.easyocr_reader.readtext(image)
            
            text_blocks = []
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # Filtra risultati a bassa confidenza
                    text_blocks.append({
                        'text': text.strip(),
                        'confidence': confidence,
                        'bbox': bbox,
                        'engine': 'easyocr'
                    })
            
            return text_blocks
        except Exception as e:
            logger.error(f"Errore EasyOCR: {e}")
            return []
    
    def extract_text_tesseract(self, image: np.ndarray) -> List[Dict]:
        """Estrae testo usando Tesseract"""
        if not TESSERACT_AVAILABLE:
            return []
        
        try:
            # Configurazione Tesseract per italiano
            custom_config = r'--oem 3 --psm 6 -l ita+eng'
            
            # Estrai testo con posizione
            data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
            
            text_blocks = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                text = data['text'][i].strip()
                conf = int(data['conf'][i])
                
                if text and conf > 30:  # Filtra testo a bassa confidenza
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    bbox = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
                    
                    text_blocks.append({
                        'text': text,
                        'confidence': conf / 100.0,
                        'bbox': bbox,
                        'engine': 'tesseract'
                    })
            
            return text_blocks
        except Exception as e:
            logger.error(f"Errore Tesseract: {e}")
            return []
    
    def extract_text_from_image(self, image: np.ndarray) -> List[Dict]:
        """Estrae testo da immagine usando tutti gli engine disponibili"""
        logger.debug("Estrazione testo da immagine...")
        
        # Pre-processing
        processed_image = self.preprocess_image(image)
        
        all_text_blocks = []
        
        # EasyOCR
        if EASYOCR_AVAILABLE and self.easyocr_reader:
            easyocr_blocks = self.extract_text_easyocr(processed_image)
            all_text_blocks.extend(easyocr_blocks)
            logger.debug(f"EasyOCR: {len(easyocr_blocks)} blocchi")
        
        # Tesseract
        if TESSERACT_AVAILABLE:
            tesseract_blocks = self.extract_text_tesseract(processed_image)
            all_text_blocks.extend(tesseract_blocks)
            logger.debug(f"Tesseract: {len(tesseract_blocks)} blocchi")
        
        # Se nessun engine disponibile, fallback
        if not all_text_blocks:
            logger.warning("Nessun engine OCR disponibile")
            return []
        
        # Ordina per posizione (top to bottom, left to right)
        all_text_blocks.sort(key=lambda x: (x['bbox'][0][1], x['bbox'][0][0]))
        
        logger.info(f"Estratti {len(all_text_blocks)} blocchi di testo")
        return all_text_blocks
    
    def process_scanned_document(self, pdf_path: str) -> List[Dict]:
        """Processa documento scannerizzato completo"""
        logger.info(f"Processamento documento scannerizzato: {pdf_path}")
        
        # 1. Estrai immagini dal PDF
        images = self.extract_images_from_pdf(pdf_path)
        
        # 2. Processa ogni pagina
        all_pages = []
        for page_num, image in enumerate(images, 1):
            logger.info(f"Processamento pagina {page_num}/{len(images)}")
            
            # Estrai testo
            text_blocks = self.extract_text_from_image(image)
            
            # Organizza testo per paragrafi
            page_text = self._organize_text_blocks(text_blocks)
            
            all_pages.append({
                'page_number': page_num,
                'text_blocks': text_blocks,
                'organized_text': page_text,
                'image_shape': image.shape
            })
        
        logger.info(f"Processamento completato: {len(all_pages)} pagine")
        return all_pages
    
    def _organize_text_blocks(self, text_blocks: List[Dict]) -> str:
        """Organizza blocchi di testo in paragrafi"""
        if not text_blocks:
            return ""
        
        # Raggruppa per righe (stessa altezza Y)
        lines = {}
        for block in text_blocks:
            y = block['bbox'][0][1]
            line_key = round(y / 20) * 20  # Raggruppa per righe vicine
            
            if line_key not in lines:
                lines[line_key] = []
            lines[line_key].append(block)
        
        # Ordina righe e blocchi
        organized_lines = []
        for y in sorted(lines.keys()):
            line_blocks = lines[y]
            line_blocks.sort(key=lambda x: x['bbox'][0][0])  # Ordina per X
            
            line_text = ' '.join(block['text'] for block in line_blocks)
            organized_lines.append(line_text)
        
        return '\n'.join(organized_lines)
    
    def is_scanned_document(self, pdf_path: str) -> bool:
        """Verifica se PDF è scannerizzato (non nativo)"""
        try:
            # Estrai prima pagina
            images = self.extract_images_from_pdf(pdf_path, dpi=150)
            if not images:
                return False
            
            first_page = images[0]
            
            # Analizza se contiene molto testo (indicatore di scansione)
            text_blocks = self.extract_text_from_image(first_page)
            
            # Se trova poco testo, probabilmente è nativo
            if len(text_blocks) < 5:
                return False
            
            # Se trova molto testo, probabilmente è scannerizzato
            return len(text_blocks) > 10
            
        except Exception as e:
            logger.warning(f"Errore verifica documento scannerizzato: {e}")
            return False

# Test del sistema
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    engine = AdvancedOCREngine()
    print("🔍 Sistema OCR avanzato inizializzato")
    print(f"   EasyOCR: {'✅' if EASYOCR_AVAILABLE else '❌'}")
    print(f"   Tesseract: {'✅' if TESSERACT_AVAILABLE else '❌'}")
    print(f"   pdf2image: {'✅' if PDF2IMAGE_AVAILABLE else '❌'}")
