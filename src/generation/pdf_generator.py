from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from typing import List, Dict
import logging
import fitz  # PyMuPDF per analisi layout originale

logger = logging.getLogger(__name__)

class PDFGenerator:
    """Genera PDF da testo tradotto con preservazione layout"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        
        # Style custom per testo legale
        self.styles.add(ParagraphStyle(
            name='LegalText',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=14,
            spaceBefore=6,
            spaceAfter=6,
            alignment=4  # Justify
        ))
    
    def create_pdf(self, pages_data: List[Dict], output_path: str, progress_callback=None):
        """
        Crea PDF da pagine tradotte con layout migliorato
        
        Args:
            pages_data: [{page_num, text, metadata}, ...]
        """
        # Verifica se abbiamo metadati per preservare layout
        has_layout_metadata = any('blocks' in page or 'width' in page for page in pages_data)
        
        if has_layout_metadata:
            self._create_pdf_with_layout(pages_data, output_path, progress_callback)
        else:
            self._create_pdf_simple(pages_data, output_path, progress_callback)
    
    def _create_pdf_simple(self, pages_data: List[Dict], output_path: str, progress_callback=None):
        """Creazione PDF standard (fallback)"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        story = []
        total_pages = len(pages_data)
        
        for i, page_data in enumerate(pages_data):
            if progress_callback:
                progress_callback(
                    (i / total_pages) * 100,
                    f"Generazione pagina {i+1}/{total_pages}"
                )
            
            # Testo pagina
            text = page_data['text']
            
            # Split in paragrafi
            paragraphs = text.split('\n\n')
            
            for para_text in paragraphs:
                if para_text.strip():
                    para = Paragraph(para_text, self.styles['LegalText'])
                    story.append(para)
                    story.append(Spacer(1, 0.2*inch))
            
            # Page break (tranne ultima pagina)
            if i < total_pages - 1:
                story.append(PageBreak())
        
        # Build PDF
        if progress_callback:
            progress_callback(90, "Finalizzazione PDF...")
        
        doc.build(story)
        
        logger.info(f"PDF generato (modalità standard): {output_path}")
    
    def _create_pdf_with_layout(self, pages_data: List[Dict], output_path: str, progress_callback=None):
        """Creazione PDF con preservazione layout (quando disponibile)"""
        # Usa SimpleDocTemplate con parametri preservati dall'originale
        first_page = pages_data[0]
        page_width = first_page.get('width', A4[0])
        page_height = first_page.get('height', A4[1])
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=(page_width, page_height),
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=30
        )
        
        story = []
        total_pages = len(pages_data)
        
        for i, page_data in enumerate(pages_data):
            if progress_callback:
                progress_callback(
                    (i / total_pages) * 100,
                    f"Generazione pagina {i+1}/{total_pages} (con layout)"
                )
            
            # Usa struttura paragrafi preservata quando disponibile
            text = page_data['text']
            
            # Split in paragrafi mantenendo struttura
            paragraphs = text.split('\n\n')
            
            for para_text in paragraphs:
                if para_text.strip():
                    # Mantieni spaziatura originale
                    para = Paragraph(para_text, self.styles['LegalText'])
                    story.append(para)
                    story.append(Spacer(1, 0.15*inch))
            
            # Page break (tranne ultima pagina)
            if i < total_pages - 1:
                story.append(PageBreak())
        
        # Build PDF
        if progress_callback:
            progress_callback(90, "Finalizzazione PDF con layout...")
        
        doc.build(story)
        
        logger.info(f"PDF generato (con preservazione layout): {output_path}")

