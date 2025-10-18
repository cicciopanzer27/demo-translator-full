#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Engine traduzione avanzato con supporto multilangue
"""

import logging
from typing import List, Dict, Optional
import requests
import json

logger = logging.getLogger(__name__)

class AdvancedTranslationEngine:
    """Engine traduzione avanzato"""
    
    def __init__(self):
        self.available_services = self._check_services()
        self.cache = {}
        
    def _check_services(self) -> Dict[str, bool]:
        """Verifica disponibilità servizi traduzione"""
        services = {}
        
        # LibreTranslate (opensource)
        try:
            response = requests.get("https://libretranslate.de/", timeout=5)
            services['libretranslate'] = response.status_code == 200
        except:
            services['libretranslate'] = False
        
        # MyMemory (gratuito)
        try:
            response = requests.get("https://api.mymemory.translated.net/", timeout=5)
            services['mymemory'] = response.status_code == 200
        except:
            services['mymemory'] = False
        
        return services
    
    def translate_with_libretranslate(self, text: str, from_lang: str, to_lang: str) -> Optional[str]:
        """Traduci usando LibreTranslate"""
        try:
            url = "https://libretranslate.de/translate"
            data = {
                'q': text,
                'source': from_lang,
                'target': to_lang,
                'format': 'text'
            }
            
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result.get('translatedText')
                
        except Exception as e:
            logger.error(f"Errore LibreTranslate: {e}")
        
        return None
    
    def translate_with_mymemory(self, text: str, from_lang: str, to_lang: str) -> Optional[str]:
        """Traduci usando MyMemory"""
        try:
            url = "https://api.mymemory.translated.net/get"
            params = {
                'q': text,
                'langpair': f"{from_lang}|{to_lang}"
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result['responseStatus'] == 200:
                    return result['responseData']['translatedText']
                    
        except Exception as e:
            logger.error(f"Errore MyMemory: {e}")
        
        return None
    
    def translate_text(self, text: str, from_lang: str, to_lang: str) -> str:
        """Traduci testo usando servizi disponibili"""
        
        # Controlla cache
        cache_key = f"{text}_{from_lang}_{to_lang}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Prova servizi in ordine di preferenza
        if self.available_services.get('libretranslate'):
            result = self.translate_with_libretranslate(text, from_lang, to_lang)
            if result:
                self.cache[cache_key] = result
                return result
        
        if self.available_services.get('mymemory'):
            result = self.translate_with_mymemory(text, from_lang, to_lang)
            if result:
                self.cache[cache_key] = result
                return result
        
        # Fallback: restituisci testo originale
        logger.warning("Nessun servizio traduzione disponibile")
        return text
    
    def translate_document(self, text_blocks: List[Dict], from_lang: str, to_lang: str) -> List[Dict]:
        """Traduci documento completo"""
        translated_blocks = []
        
        for block in text_blocks:
            original_text = block['text']
            translated_text = self.translate_text(original_text, from_lang, to_lang)
            
            translated_block = block.copy()
            translated_block['original_text'] = original_text
            translated_block['text'] = translated_text
            translated_block['translated'] = True
            
            translated_blocks.append(translated_block)
        
        return translated_blocks

if __name__ == "__main__":
    engine = AdvancedTranslationEngine()
    print(f"Servizi disponibili: {list(engine.available_services.keys())}")
