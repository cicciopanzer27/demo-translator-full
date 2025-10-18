import argostranslate.package
import argostranslate.translate
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class TranslationEngine:
    """Engine traduzione offline con Argos Translate"""
    
    def __init__(self):
        self.installed_languages = None
        self._load_installed_languages()
    
    def _load_installed_languages(self):
        """Carica lingue installate"""
        self.installed_languages = argostranslate.translate.get_installed_languages()
        logger.info(f"Lingue installate: {len(self.installed_languages)}")
    
    def is_language_pair_available(self, from_code: str, to_code: str) -> bool:
        """Verifica se coppia lingue è disponibile (diretta o tramite pivot EN)"""
        try:
            # Verifica che entrambe le lingue siano installate
            from_lang = next((l for l in self.installed_languages if l.code == from_code), None)
            to_lang = next((l for l in self.installed_languages if l.code == to_code), None)
            
            if not from_lang:
                logger.warning(f"Lingua source {from_code} non trovata")
                return False
                
            if not to_lang:
                logger.warning(f"Lingua target {to_code} non trovata")
                return False
            
            # Test traduzione diretta
            try:
                test_result = argostranslate.translate.translate("test", from_code, to_code)
                if test_result is not None:
                    logger.debug(f"Coppia diretta {from_code}->{to_code} disponibile")
                    return True
            except Exception:
                pass
            
            # Se diretta non funziona, prova tramite pivot inglese
            if from_code != 'en' and to_code != 'en':
                try:
                    # Test IT->EN->FR (esempio)
                    step1 = argostranslate.translate.translate("test", from_code, 'en')
                    step2 = argostranslate.translate.translate(step1, 'en', to_code)
                    if step1 and step2:
                        logger.info(f"Coppia {from_code}->{to_code} disponibile tramite pivot EN")
                        return True
                except Exception as pivot_e:
                    logger.debug(f"Pivot EN fallito per {from_code}->{to_code}: {pivot_e}")
            
            logger.warning(f"Coppia {from_code}->{to_code} non disponibile")
            return False
                
        except Exception as e:
            logger.debug(f"Errore verifica coppia {from_code}->{to_code}: {e}")
            return False
    
    def translate_text(self, text: str, from_code: str, to_code: str) -> str:
        """Traduci singolo testo (diretta o tramite pivot EN)"""
        # Prova traduzione diretta
        try:
            result = argostranslate.translate.translate(text, from_code, to_code)
            if result:
                return result
        except Exception:
            pass
        
        # Se diretta fallisce, prova tramite pivot inglese
        if from_code != 'en' and to_code != 'en':
            try:
                logger.debug(f"Usando pivot EN per {from_code}->{to_code}")
                # Step 1: FROM -> EN
                intermediate = argostranslate.translate.translate(text, from_code, 'en')
                # Step 2: EN -> TO
                result = argostranslate.translate.translate(intermediate, 'en', to_code)
                if result:
                    return result
            except Exception as pivot_e:
                logger.error(f"Errore traduzione pivot {from_code}->EN->{to_code}: {pivot_e}")
        
        # Se arriviamo qui, la traduzione non è disponibile
        logger.error(f"Traduzione {from_code}->{to_code} non disponibile")
        raise ValueError(f"Impossibile tradurre da {from_code} a {to_code}")
    
    def translate_chunks(
        self, 
        chunks: List[str], 
        from_code: str, 
        to_code: str,
        progress_callback=None
    ) -> List[str]:
        """Traduci lista di chunk con progress"""
        translated = []
        total = len(chunks)
        
        for i, chunk in enumerate(chunks, 1):
            if progress_callback:
                progress_callback(i, total, f"Traduzione chunk {i}/{total}")
            
            if not chunk.strip():
                translated.append(chunk)
                continue
            
            try:
                # Usa il metodo translate_text che abbiamo sistemato
                translated_chunk = self.translate_text(chunk, from_code, to_code)
                translated.append(translated_chunk)
            except Exception as e:
                logger.error(f"Errore traduzione chunk {i}: {e}")
                translated.append(chunk)  # Fallback: testo originale
        
        return translated
    
    def get_available_languages(self) -> List[Dict]:
        """Lista lingue disponibili (include lingue con pivot EN)"""
        languages = []
        lang_codes = {lang.code for lang in self.installed_languages}
        
        for lang in self.installed_languages:
            # Gestisci sia Translation che IdentityTranslation
            translations_to = []
            try:
                for t in lang.translations_to:
                    # t può essere un oggetto Language o un CachedTranslation
                    if isinstance(t, str):
                        translations_to.append(t)
                    elif hasattr(t, 'code'):
                        translations_to.append(t.code)
                    elif hasattr(t, 'target') and hasattr(t.target, 'code'):
                        translations_to.append(t.target.code)
            except Exception as e:
                logger.warning(f"Errore parsing translations_to per {lang.code}: {e}")
            
            # NUOVO: Aggiungi lingue raggiungibili tramite pivot EN
            if lang.code != 'en':
                # Se questa lingua può andare verso EN, aggiungi tutte le lingue raggiungibili da EN
                can_go_to_en = 'en' in translations_to
                if can_go_to_en:
                    # Trova lingue raggiungibili da EN
                    en_lang = next((l for l in self.installed_languages if l.code == 'en'), None)
                    if en_lang:
                        try:
                            for t in en_lang.translations_to:
                                target_code = None
                                if isinstance(t, str):
                                    target_code = t
                                elif hasattr(t, 'code'):
                                    target_code = t.code
                                elif hasattr(t, 'target') and hasattr(t.target, 'code'):
                                    target_code = t.target.code
                                
                                if target_code and target_code not in translations_to and target_code != lang.code:
                                    translations_to.append(target_code)
                                    logger.debug(f"Aggiunta lingua {target_code} per {lang.code} tramite pivot EN")
                        except Exception as e:
                            logger.warning(f"Errore aggiunta pivot EN per {lang.code}: {e}")
            
            languages.append({
                'code': lang.code,
                'name': lang.name,
                'translations_to': sorted(set(translations_to))  # Rimuovi duplicati e ordina
            })
        return languages


class ModelManager:
    """Gestisce download e installazione modelli"""
    
    @staticmethod
    def update_package_index():
        """Aggiorna indice pacchetti disponibili"""
        argostranslate.package.update_package_index()
    
    @staticmethod
    def get_available_packages() -> List:
        """Lista pacchetti scaricabili"""
        return argostranslate.package.get_available_packages()
    
    @staticmethod
    def install_language_pair(from_code: str, to_code: str, progress_callback=None):
        """Installa coppia di lingue"""
        available = argostranslate.package.get_available_packages()
        
        package = next(
            filter(lambda x: x.from_code == from_code and x.to_code == to_code, available),
            None
        )
        
        if not package:
            raise ValueError(f"Pacchetto {from_code}→{to_code} non disponibile")
        
        logger.info(f"Download pacchetto {from_code}→{to_code}...")
        if progress_callback:
            progress_callback(0, 100, f"Download {package.package_version}...")
        
        download_path = package.download()
        
        if progress_callback:
            progress_callback(50, 100, "Installazione...")
        
        argostranslate.package.install_from_path(download_path)
        
        if progress_callback:
            progress_callback(100, 100, "Completato")
        
        logger.info(f"Installato {from_code}→{to_code}")

