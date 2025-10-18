#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Parser layout avanzato per documenti
"""

import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import logging
from typing import List, Dict, Tuple
import io

logger = logging.getLogger(__name__)

class LayoutParser:
    """Parser layout per documenti scansionati"""
    
    def __init__(self):
        self.available_models = self._check_models()
        
    def _check_models(self) -> Dict[str, bool]:
        """Verifica disponibilità modelli layout"""
        models = {}
        
        try:
            import layoutparser
            models['layoutparser'] = True
        except ImportError:
            models['layoutparser'] = False
            
        try:
            import transformers
            models['transformers'] = True
        except ImportError:
            models['transformers'] = False
            
        return models
    
    def detect_layout_opencv(self, image: np.ndarray) -> List[Dict]:
        """Rileva layout usando OpenCV"""
        # Converti in scala di grigi
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # Rileva contorni
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        layout_elements = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Filtra elementi piccoli
                x, y, w, h = cv2.boundingRect(contour)
                
                # Classifica elemento basato su dimensioni
                aspect_ratio = w / h
                if aspect_ratio > 2:
                    element_type = "paragraph"
                elif aspect_ratio < 0.5:
                    element_type = "title"
                else:
                    element_type = "block"
                
                layout_elements.append({
                    'type': element_type,
                    'bbox': [x, y, w, h],
                    'area': area,
                    'confidence': 0.8
                })
        
        return layout_elements
    
    def detect_layout_ml(self, image: np.ndarray) -> List[Dict]:
        """Rileva layout usando modelli ML"""
        if not self.available_models.get('layoutparser'):
            return self.detect_layout_opencv(image)
        
        try:
            import layoutparser as lp
            
            # Carica modello (se disponibile)
            model = lp.Detectron2LayoutModel(
                'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config'
            )
            
            # Rileva layout
            layout = model.detect(image)
            
            layout_elements = []
            for element in layout:
                layout_elements.append({
                    'type': element.type.lower(),
                    'bbox': [element.block.x_1, element.block.y_1, 
                            element.block.x_2 - element.block.x_1,
                            element.block.y_2 - element.block.y_1],
                    'confidence': element.score
                })
            
            return layout_elements
            
        except Exception as e:
            logger.error(f"Errore layout ML: {e}")
            return self.detect_layout_opencv(image)
    
    def parse_document_structure(self, pdf_path: str) -> List[Dict]:
        """Analizza struttura documento"""
        doc = fitz.open(pdf_path)
        document_structure = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Converti pagina in immagine
            mat = fitz.Matrix(2.0, 2.0)  # Zoom 2x
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            img_array = np.array(img)
            
            # Rileva layout
            layout_elements = self.detect_layout_ml(img_array)
            
            page_structure = {
                'page_num': page_num + 1,
                'width': img.width,
                'height': img.height,
                'elements': layout_elements
            }
            
            document_structure.append(page_structure)
        
        doc.close()
        return document_structure

if __name__ == "__main__":
    parser = LayoutParser()
    print(f"Modelli disponibili: {list(parser.available_models.keys())}")
