#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motore di traduzione offline
"""

import logging
from typing import List, Dict, Optional, Callable
import argostranslate.package
import argostranslate.translate

logger = logging.getLogger(__name__)

class TranslationEngine:
    """Motore di traduzione offline con Argos Translate"""
    
    def __init__(self):
        self.available_models = self._get_available_models()
        logger.info(f"Modelli disponibili: {list(self.available_models.keys())}")
    
    def _get_available_models(self) -> Dict:
        """Ottiene i modelli di traduzione disponibili"""
        
        try:
            # Installa modelli se non presenti
            self._install_models_if_needed()
            
            # Lista modelli installati
            installed_packages = argostranslate.package.get_installed_packages()
            models = {}
            
            for package in installed_packages:
                key = f"{package.from_code}-{package.to_code}"
                models[key] = {
                    'from_code': package.from_code,
                    'to_code': package.to_code,
                    'package': package
                }
            
            return models
            
        except Exception as e:
            logger.error(f"Errore nel caricamento modelli: {e}")
            return {}
    
    def _install_models_if_needed(self):
        """Installa modelli di traduzione se necessari"""
        
        try:
            # Verifica se i modelli IT-EN sono installati
            installed_packages = argostranslate.package.get_installed_packages()
            
            has_it_en = any(p.from_code == 'it' and p.to_code == 'en' for p in installed_packages)
            has_en_it = any(p.from_code == 'en' and p.to_code == 'it' for p in installed_packages)
            
            if not has_it_en or not has_en_it:
                logger.info("Installazione modelli di traduzione...")
                
                # Scarica e installa modelli
                argostranslate.package.update_package_index()
                available_packages = argostranslate.package.get_available_packages()
                
                # Installa IT -> EN
                if not has_it_en:
                    it_en_packages = [p for p in available_packages if p.from_code == 'it' and p.to_code == 'en']
                    if it_en_packages:
                        it_en_packages[0].install()
                        logger.info("Installato modello IT -> EN")
                
                # Installa EN -> IT
                if not has_en_it:
                    en_it_packages = [p for p in available_packages if p.from_code == 'en' and p.to_code == 'it']
                    if en_it_packages:
                        en_it_packages[0].install()
                        logger.info("Installato modello EN -> IT")
                
                # Ricarica modelli
                self.available_models = self._get_available_models()
                
        except Exception as e:
            logger.error(f"Errore nell'installazione modelli: {e}")
    
    def translate_document(self, 
                          pages_data: List[Dict], 
                          from_lang: str, 
                          to_lang: str,
                          progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        Traduce un documento completo
        
        Args:
            pages_data: Lista di pagine con testo
            from_lang: Lingua sorgente
            to_lang: Lingua destinazione
            progress_callback: Callback per progress updates
            
        Returns:
            List[Dict]: Pagine tradotte
        """
        
        logger.info(f"Traduzione documento: {from_lang} -> {to_lang}")
        
        try:
            # Verifica se il modello è disponibile
            model_key = f"{from_lang}-{to_lang}"
            if model_key not in self.available_models:
                raise Exception(f"Modello di traduzione {model_key} non disponibile")
            
            translated_pages = []
            total_pages = len(pages_data)
            
            for i, page_data in enumerate(pages_data):
                if progress_callback:
                    progress_callback(
                        int((i / total_pages) * 100),
                        f"Traduzione pagina {i + 1}/{total_pages}"
                    )
                
                # Traduci la pagina
                translated_page = self._translate_page(page_data, from_lang, to_lang)
                translated_pages.append(translated_page)
                
                logger.debug(f"Pagina {i + 1} tradotta: {len(translated_page['translated_text'])} caratteri")
            
            logger.info(f"Traduzione completata: {len(translated_pages)} pagine")
            return translated_pages
            
        except Exception as e:
            logger.error(f"Errore nella traduzione: {e}")
            raise
    
    def _translate_page(self, page_data: Dict, from_lang: str, to_lang: str) -> Dict:
        """
        Traduce una singola pagina
        
        Args:
            page_data: Dati della pagina
            from_lang: Lingua sorgente
            to_lang: Lingua destinazione
            
        Returns:
            Dict: Pagina tradotta
        """
        
        try:
            text = page_data['text']
            
            if not text.strip():
                return {
                    **page_data,
                    'translated_text': '',
                    'translation_method': 'empty'
                }
            
            # Chunking per testi lunghi
            chunks = self._chunk_text(text)
            
            # Traduci ogni chunk
            translated_chunks = []
            for chunk in chunks:
                if chunk.strip():
                    translated_chunk = self._translate_text(chunk, from_lang, to_lang)
                    translated_chunks.append(translated_chunk)
                else:
                    translated_chunks.append(chunk)
            
            # Ricombina i chunk
            translated_text = '\n'.join(translated_chunks)
            
            return {
                **page_data,
                'translated_text': translated_text,
                'translation_method': 'argos_translate'
            }
            
        except Exception as e:
            logger.error(f"Errore traduzione pagina: {e}")
            return {
                **page_data,
                'translated_text': page_data['text'],  # Fallback al testo originale
                'translation_method': 'error'
            }
    
    def _translate_text(self, text: str, from_lang: str, to_lang: str) -> str:
        """
        Traduce un testo usando Argos Translate
        
        Args:
            text: Testo da tradurre
            from_lang: Lingua sorgente
            to_lang: Lingua destinazione
            
        Returns:
            str: Testo tradotto
        """
        
        try:
            # Usa Argos Translate per la traduzione
            translated_text = argostranslate.translate.translate(text, from_lang, to_lang)
            return translated_text
            
        except Exception as e:
            logger.error(f"Errore traduzione testo: {e}")
            return text  # Fallback al testo originale
    
    def _chunk_text(self, text: str, max_chunk_size: int = 1000) -> List[str]:
        """
        Divide il testo in chunk per traduzione
        
        Args:
            text: Testo da dividere
            max_chunk_size: Dimensione massima chunk
            
        Returns:
            List[str]: Lista di chunk
        """
        
        if len(text) <= max_chunk_size:
            return [text]
        
        # Dividi per paragrafi
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= max_chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

# Test del motore di traduzione
if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test con testo di esempio
    engine = TranslationEngine()
    
    test_pages = [
        {
            'page_num': 1,
            'text': "This is a test document for translation. It contains multiple sentences to verify the translation engine works correctly.",
            'char_count': 100,
            'word_count': 20
        },
        {
            'page_num': 2,
            'text': "The second page contains more complex content with technical terms and legal language that should be translated accurately.",
            'char_count': 120,
            'word_count': 25
        }
    ]
    
    def progress_callback(percent, message):
        print(f"[{percent:3d}%] {message}")
    
    translated_pages = engine.translate_document(
        test_pages, 
        'en', 
        'it', 
        progress_callback
    )
    
    print(f"\nRisultati traduzione:")
    for page in translated_pages:
        print(f"\nPagina {page['page_num']}:")
        print(f"Originale: {page['text'][:100]}...")
        print(f"Tradotto:  {page['translated_text'][:100]}...")
