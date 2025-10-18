#!/usr/bin/env python3
"""
Worker avanzato per traduzione documenti (nativi + scannerizzati)
Integra OCR per documenti scannerizzati
"""

import os
import logging
from PyQt6.QtCore import QThread, pyqtSignal
from typing import List, Dict, Optional

# Import moduli esistenti
from ..extraction.pdf_extractor import PDFExtractor
from ..extraction.docx_extractor import DOCXExtractor
from ..generation.pdf_generator import PDFGenerator
from ..generation.docx_generator import DOCXGenerator
from ..translation.engine import TranslationEngine
from ..translation.chunker import DocumentChunker

# Import OCR
try:
    from ..ocr.advanced_ocr_engine import AdvancedOCREngine
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logging.warning("Sistema OCR non disponibile")

logger = logging.getLogger(__name__)

class AdvancedTranslationWorker(QThread):
    """Worker avanzato per traduzione documenti con supporto OCR"""
    
    # Segnali
    progress = pyqtSignal(int, str)  # percentuale, messaggio
    finished = pyqtSignal(str)      # path file output
    error = pyqtSignal(str)         # messaggio errore
    
    def __init__(self, input_path: str, output_dir: str, from_lang: str, to_lang: str):
        super().__init__()
        self.input_path = input_path
        self.output_dir = output_dir
        self.from_lang = from_lang
        self.to_lang = to_lang
        self._is_cancelled = False
        
        # Inizializza componenti
        self.engine = TranslationEngine()
        self.chunker = DocumentChunker()
        
        # Inizializza OCR se disponibile
        self.ocr_engine = None
        if OCR_AVAILABLE:
            try:
                self.ocr_engine = AdvancedOCREngine()
                logger.info("Sistema OCR inizializzato")
            except Exception as e:
                logger.error(f"Errore inizializzazione OCR: {e}")
                self.ocr_engine = None
        
        # Determina tipo documento
        self.is_scanned = self._detect_document_type()
        
        # Setup generatori
        self._setup_generators()
    
    def _detect_document_type(self) -> bool:
        """Rileva se documento è scannerizzato"""
        if not self.ocr_engine:
            return False
        
        try:
            if self.input_path.lower().endswith('.pdf'):
                return self.ocr_engine.is_scanned_document(self.input_path)
            return False
        except Exception as e:
            logger.warning(f"Errore rilevamento tipo documento: {e}")
            return False
    
    def _setup_generators(self):
        """Setup generatori output"""
        base_name = os.path.splitext(os.path.basename(self.input_path))[0]
        self.output_filename = f"{base_name}_tradotto"
        self.output_path = os.path.join(self.output_dir, f"{self.output_filename}.docx")
    
    def cancel(self):
        """Annulla operazione"""
        self._is_cancelled = True
    
    def run(self):
        """Esegue traduzione completa"""
        try:
            logger.info(f"Avvio traduzione avanzata: {self.input_path}")
            logger.info(f"Tipo documento: {'Scannerizzato' if self.is_scanned else 'Nativo'}")
            
            if self.is_scanned and self.ocr_engine:
                self._process_scanned_document()
            else:
                self._process_native_document()
            
            if not self._is_cancelled:
                self.progress.emit(100, 'Completato!')
                self.finished.emit(str(self.output_path))
                
        except Exception as e:
            logger.exception("Errore traduzione avanzata")
            self.error.emit(str(e))
    
    def _process_scanned_document(self):
        """Processa documento scannerizzato con OCR"""
        logger.info("Processamento documento scannerizzato...")
        
        # 1. OCR
        self.progress.emit(10, 'Analisi documento scannerizzato...')
        if self._is_cancelled:
            return
        
        ocr_pages = self.ocr_engine.process_scanned_document(self.input_path)
        
        if self._is_cancelled:
            return
        
        # 2. Organizza testo per traduzione
        self.progress.emit(30, 'Preparazione testo per traduzione...')
        pages_data = []
        for page in ocr_pages:
            pages_data.append({
                'page_number': page['page_number'],
                'text': page['organized_text'],
                'chunks': []
            })
        
        # 3. Chunking
        self.progress.emit(40, 'Suddivisione testo in segmenti...')
        chunked_pages = self._chunk_document(pages_data)
        total_chunks = sum(len(page['chunks']) for page in chunked_pages)
        
        if self._is_cancelled:
            return
        
        # 4. Traduzione
        self.progress.emit(50, f'Traduzione in corso ({total_chunks} segmenti)...')
        translated_pages = self._translate_chunks(chunked_pages, total_chunks)
        
        if self._is_cancelled:
            return
        
        # 5. Generazione output
        self.progress.emit(85, 'Generazione documento tradotto...')
        self._generate_output(translated_pages)
    
    def _process_native_document(self):
        """Processa documento nativo (PDF/DOCX)"""
        logger.info("Processamento documento nativo...")
        
        # 1. Estrazione testo
        self.progress.emit(10, 'Estrazione testo dal documento...')
        pages_data = self._extract_text()
        
        if self._is_cancelled:
            return
        
        # 2. Chunking
        self.progress.emit(30, 'Preparazione testo per traduzione...')
        chunked_pages = self._chunk_document(pages_data)
        total_chunks = sum(len(page['chunks']) for page in chunked_pages)
        
        if self._is_cancelled:
            return
        
        # 3. Traduzione
        self.progress.emit(50, f'Traduzione in corso ({total_chunks} segmenti)...')
        translated_pages = self._translate_chunks(chunked_pages, total_chunks)
        
        if self._is_cancelled:
            return
        
        # 4. Generazione output
        self.progress.emit(85, 'Generazione documento tradotto...')
        self._generate_output(translated_pages)
    
    def _extract_text(self) -> List[Dict]:
        """Estrae testo da documento nativo"""
        if self.input_path.lower().endswith('.pdf'):
            extractor = PDFExtractor()
            return extractor.extract_intelligent(self.input_path)
        elif self.input_path.lower().endswith('.docx'):
            extractor = DOCXExtractor()
            return extractor.extract(self.input_path)
        else:
            raise ValueError(f"Formato non supportato: {self.input_path}")
    
    def _chunk_document(self, pages_data: List[Dict]) -> List[Dict]:
        """Suddivide documento in chunk per traduzione"""
        chunked_pages = []
        
        for page in pages_data:
            if not page['text'].strip():
                chunked_pages.append({
                    'page_number': page['page_number'],
                    'text': page['text'],
                    'chunks': ['']
                })
                continue
            
            # Chunking per paragrafi
            chunks = self.chunker.chunk_by_paragraphs(page['text'])
            
            chunked_pages.append({
                'page_number': page['page_number'],
                'text': page['text'],
                'chunks': chunks
            })
        
        return chunked_pages
    
    def _translate_chunks(self, chunked_pages: List[Dict], total_chunks: int) -> List[Dict]:
        """Traduce tutti i chunk"""
        translated_pages = []
        current_chunk = 0
        
        for page in chunked_pages:
            if self._is_cancelled:
                return []
            
            translated_chunks = []
            
            for chunk in page['chunks']:
                if not chunk.strip():
                    translated_chunks.append(chunk)
                    continue
                
                try:
                    # Traduci chunk
                    translated = self.engine.translate_text(
                        chunk, self.from_lang, self.to_lang
                    )
                    translated_chunks.append(translated)
                    
                except Exception as e:
                    logger.error(f"Errore traduzione chunk: {e}")
                    translated_chunks.append(chunk)  # Fallback: testo originale
                
                current_chunk += 1
                
                # Aggiorna progresso
                progress = 50 + int((current_chunk / total_chunks) * 35)
                self.progress.emit(progress, f'Traduzione {current_chunk}/{total_chunks}...')
            
            translated_pages.append({
                'page_number': page['page_number'],
                'text': page['text'],
                'chunks': translated_chunks,
                'translated_text': '\n'.join(translated_chunks)
            })
        
        return translated_pages
    
    def _generate_output(self, translated_pages: List[Dict]):
        """Genera documento di output"""
        # Combina tutto il testo tradotto
        full_text = '\n\n'.join(page['translated_text'] for page in translated_pages)
        
        # Genera DOCX
        generator = DOCXGenerator()
        generator.generate(
            text=full_text,
            output_path=self.output_path,
            title=f"Documento Tradotto ({self.from_lang} → {self.to_lang})"
        )
        
        logger.info(f"Documento generato: {self.output_path}")

# Test del worker
if __name__ == "__main__":
    import sys
    from PyQt6.QtCore import QCoreApplication
    
    app = QCoreApplication(sys.argv)
    
    # Test worker
    worker = AdvancedTranslationWorker(
        input_path="test.pdf",
        output_dir="output",
        from_lang="en",
        to_lang="it"
    )
    
    print("🔧 Worker avanzato inizializzato")
    print(f"   OCR disponibile: {'✅' if OCR_AVAILABLE else '❌'}")
    print(f"   Engine traduzione: {'✅' if worker.engine else '❌'}")