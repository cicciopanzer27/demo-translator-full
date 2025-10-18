from PyQt6.QtCore import QThread, pyqtSignal
from pathlib import Path
import logging
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from extraction.pdf_extractor import PDFExtractor
from extraction.docx_extractor import DOCXExtractor
from translation.chunker import DocumentChunker
from generation.pdf_generator import PDFGenerator
from generation.docx_generator import DOCXGenerator

logger = logging.getLogger(__name__)

class TranslationWorker(QThread):
    """Worker per traduzione in background - VERSIONE SEMPLIFICATA E ROBUSTA"""
    
    progress = pyqtSignal(int, str)  # (percentuale, messaggio)
    finished = pyqtSignal(str)       # output_path
    error = pyqtSignal(str)          # error_message
    
    def __init__(self, input_path, output_path, from_code, to_code, engine):
        super().__init__()
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.from_code = from_code
        self.to_code = to_code
        self.engine = engine
        self._is_cancelled = False
    
    def cancel(self):
        """Cancella operazione"""
        self._is_cancelled = True
    
    def run(self):
        """Esegui traduzione completa - PIPELINE SEMPLICE"""
        try:
            logger.info(f"Inizio traduzione: {self.input_path}")
            logger.info(f"Da {self.from_code} a {self.to_code}")
            
            # FASE 1: Estrazione testo (0-20%)
            self.progress.emit(0, 'Estrazione testo dal documento...')
            pages_data = self._extract_text()
            
            if self._is_cancelled:
                return
            
            logger.info(f"Estratte {len(pages_data)} pagine")
            
            # FASE 2: Chunking (20-25%)
            self.progress.emit(20, 'Preparazione testo per traduzione...')
            chunked_pages = self._chunk_document(pages_data)
            total_chunks = sum(len(page['chunks']) for page in chunked_pages)
            
            if self._is_cancelled:
                return
            
            logger.info(f"Creati {total_chunks} chunks per traduzione")
            
            # FASE 3: Traduzione (25-85%)
            self.progress.emit(25, f'Traduzione in corso ({total_chunks} segmenti)...')
            translated_pages = self._translate_chunks(chunked_pages, total_chunks)
            
            if self._is_cancelled:
                return
            
            logger.info(f"Traduzione completata per {len(translated_pages)} pagine")
            
            # FASE 4: Generazione output (85-100%)
            self.progress.emit(85, 'Generazione documento tradotto...')
            self._generate_output(translated_pages)
            
            self.progress.emit(100, 'Completato!')
            logger.info(f"Documento salvato: {self.output_path}")
            self.finished.emit(str(self.output_path))
            
        except Exception as e:
            logger.exception("Errore traduzione")
            self.error.emit(str(e))
    
    def _extract_text(self):
        """Estrae testo da PDF o DOCX"""
        if self.input_path.suffix.lower() == '.pdf':
            extractor = PDFExtractor()
            return extractor.extract_text_with_layout(
                str(self.input_path),
                progress_callback=lambda p, t, m: self.progress.emit(
                    int(5 + (p/t) * 15), m
                )
            )
        else:
            extractor = DOCXExtractor()
            pages = extractor.extract_with_structure(
                str(self.input_path),
                progress_callback=lambda p, t, m: self.progress.emit(
                    int(5 + (p/t) * 15), m
                )
            )
            # Converti formato DOCX in "pagine" simulate
            return [{'page_num': 1, 'text': '\n\n'.join([e['text'] for e in pages]), 'elements': pages}]
    
    def _chunk_document(self, pages_data):
        """Split documento in chunk"""
        chunker = DocumentChunker(max_chunk_size=500)
        return chunker.chunk_document_pages(pages_data)
    
    def _translate_chunks(self, chunked_pages, total_chunks):
        """Traduci tutti i chunk"""
        translated_pages = []
        chunk_counter = 0
        
        for page_data in chunked_pages:
            if self._is_cancelled:
                break
            
            page_chunks = page_data['chunks']
            
            # Traduci chunk della pagina
            translated_chunks = []
            for chunk in page_chunks:
                if self._is_cancelled:
                    break
                
                chunk_counter += 1
                progress = 25 + int((chunk_counter / total_chunks) * 60)
                
                self.progress.emit(
                    progress,
                    f'Traduzione pagina {page_data["page_num"]} '
                    f'({chunk_counter}/{total_chunks} segmenti)'
                )
                
                # Traduci il chunk
                translated = self.engine.translate_text(
                    chunk,
                    self.from_code,
                    self.to_code
                )
                translated_chunks.append(translated)
            
            # Riunisci chunk tradotti
            translated_pages.append({
                'page_num': page_data['page_num'],
                'text': ' '.join(translated_chunks),
                'metadata': page_data.get('metadata', {})
            })
        
        return translated_pages
    
    def _generate_output(self, translated_pages):
        """Genera documento output"""
        if self.output_path.suffix.lower() == '.pdf':
            generator = PDFGenerator()
            generator.create_pdf(
                translated_pages,
                str(self.output_path),
                progress_callback=lambda p, m: self.progress.emit(
                    85 + int(p * 0.15), m
                )
            )
        else:
            generator = DOCXGenerator()
            generator.create_docx(
                translated_pages,
                str(self.output_path),
                progress_callback=lambda p, m: self.progress.emit(
                    85 + int(p * 0.15), m
                )
            )
