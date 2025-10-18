#!/usr/bin/env python3
"""
Worker pulito per traduzione documenti (nativi + scannerizzati)
Senza dipendenze problematiche
"""

import os
import logging
from PyQt6.QtCore import QThread, pyqtSignal
from typing import List, Dict, Optional

# Import moduli esistenti
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from extraction.pdf_extractor import PDFExtractor
from extraction.docx_extractor import DOCXExtractor
from generation.pdf_generator import PDFGenerator
from generation.docx_generator import DOCXGenerator
from translation.engine import TranslationEngine
from translation.chunker import DocumentChunker

logger = logging.getLogger(__name__)

class CleanWorker(QThread):
    """Worker pulito per traduzione documenti"""
    
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
        
        # Setup generatori
        self._setup_generators()
    
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
            logger.info(f"Avvio traduzione: {self.input_path}")
            
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
            
            if not self._is_cancelled:
                self.progress.emit(100, 'Completato!')
                self.finished.emit(str(self.output_path))
                
        except Exception as e:
            logger.exception("Errore traduzione")
            self.error.emit(str(e))
    
    def _extract_text(self) -> List[Dict]:
        """Estrae testo da documento"""
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
            # Gestisci sia 'page_number' che 'page_num'
            page_num = page.get('page_number', page.get('page_num', 1))
            
            if not page['text'].strip():
                chunked_pages.append({
                    'page_number': page_num,
                    'text': page['text'],
                    'chunks': ['']
                })
                continue
            
            # Chunking per paragrafi
            chunks = self.chunker.chunk_by_paragraphs(page['text'])
            
            chunked_pages.append({
                'page_number': page_num,
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
        # Genera DOCX
        generator = DOCXGenerator()
        generator.create_docx(
            pages_data=translated_pages,
            output_path=self.output_path,
            progress_callback=None
        )
        
        logger.info(f"Documento generato: {self.output_path}")

# Test del worker
if __name__ == "__main__":
    import sys
    from PyQt6.QtCore import QCoreApplication
    
    app = QCoreApplication(sys.argv)
    
    # Test worker
    worker = CleanWorker(
        input_path="test.pdf",
        output_dir="output",
        from_lang="en",
        to_lang="it"
    )
    
    print("Worker pulito inizializzato")
    print(f"   Engine traduzione: {'Si' if worker.engine else 'No'}")
