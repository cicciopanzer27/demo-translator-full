from typing import List
import re

class DocumentChunker:
    """Split documenti lunghi in chunk ottimali per traduzione"""
    
    def __init__(self, max_chunk_size: int = 500):
        """
        Args:
            max_chunk_size: Numero massimo caratteri per chunk
        """
        self.max_chunk_size = max_chunk_size
    
    def chunk_by_sentences(self, text: str) -> List[str]:
        """
        Split per frasi (ottimale per traduzione)
        
        Mantiene contesto: non spezza mai a metà frase
        """
        # Split per punteggiatura: . ! ? seguito da spazio/newline
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Se aggiungere questa frase supera il limite
            if len(current_chunk) + len(sentence) > self.max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = sentence
                else:
                    # Frase singola troppo lunga, split forzato
                    chunks.append(sentence)
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def chunk_by_paragraphs(self, text: str) -> List[str]:
        """Split per paragrafi (preserva struttura)"""
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if not para.strip():
                continue
            
            if len(current_chunk) + len(para) > self.max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = para
                else:
                    # Paragrafo troppo lungo, split per frasi
                    para_chunks = self.chunk_by_sentences(para)
                    chunks.extend(para_chunks)
            else:
                current_chunk += "\n\n" + para if current_chunk else para
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def chunk_document_pages(self, pages_data: List[dict]) -> List[dict]:
        """
        Chunk documento estratto da PDF/DOCX
        Preserva metadati pagina
        """
        chunked_pages = []
        
        for page_data in pages_data:
            text = page_data['text']
            
            if len(text) <= self.max_chunk_size:
                # Pagina intera come singolo chunk
                chunked_pages.append({
                    'page_num': page_data['page_num'],
                    'chunks': [text],
                    'metadata': page_data
                })
            else:
                # Split pagina in chunk
                chunks = self.chunk_by_sentences(text)
                chunked_pages.append({
                    'page_num': page_data['page_num'],
                    'chunks': chunks,
                    'metadata': page_data
                })
        
        return chunked_pages

