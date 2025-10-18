#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisi dettagliata dei documenti demo per progettare l'architettura
"""

import os
import sys
os.environ['PYTHONIOENCODING'] = 'utf-8'

import fitz  # PyMuPDF
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def analizza_documento_pdf(pdf_path):
    """Analizza un documento PDF in dettaglio"""
    
    print(f"\n{'='*80}")
    print(f"ANALISI: {Path(pdf_path).name}")
    print(f"{'='*80}")
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        print(f"Pagine totali: {total_pages}")
        
        pages_with_content = []
        total_chars = 0
        total_words = 0
        
        for page_num in range(total_pages):
            page = doc[page_num]
            
            # Metodo 1: Estrazione standard
            text_standard = page.get_text()
            
            # Metodo 2: Estrazione con layout
            text_dict = page.get_text("dict")
            text_layout = ""
            for block in text_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text_layout += span["text"] + " "
                        text_layout += "\n"
            
            # Metodo 3: Estrazione raw
            text_raw = page.get_text("text")
            
            # Scegli il migliore
            texts = [text_standard, text_layout, text_raw]
            best_text = max(texts, key=len)
            
            # Pulisci
            cleaned_text = best_text.strip()
            char_count = len(cleaned_text)
            word_count = len(cleaned_text.split())
            
            print(f"  Pagina {page_num + 1}: {char_count:,} caratteri, {word_count:,} parole")
            
            if char_count > 50:  # Pagina con contenuto
                pages_with_content.append({
                    'page_num': page_num + 1,
                    'text': cleaned_text,
                    'char_count': char_count,
                    'word_count': word_count
                })
                total_chars += char_count
                total_words += word_count
        
        doc.close()
        
        print(f"\nRIASSUNTO:")
        print(f"  - Pagine con contenuto: {len(pages_with_content)}/{total_pages}")
        print(f"  - Caratteri totali: {total_chars:,}")
        print(f"  - Parole totali: {total_words:,}")
        
        # Mostra anteprima prima pagina con contenuto
        if pages_with_content:
            first_page = pages_with_content[0]
            print(f"\nANTEPRIMA PRIMA PAGINA:")
            print("-" * 60)
            preview = first_page['text'][:400] + "..." if len(first_page['text']) > 400 else first_page['text']
            print(preview)
            print("-" * 60)
        
        return {
            'total_pages': total_pages,
            'pages_with_content': len(pages_with_content),
            'total_chars': total_chars,
            'total_words': total_words,
            'is_native': total_chars > 1000,  # Documento nativo se ha molto testo
            'is_scanned': total_chars < 500   # Documento scannerizzato se ha poco testo
        }
        
    except Exception as e:
        print(f"ERRORE: {e}")
        return None

def main():
    """Analizza tutti i documenti demo"""
    
    print("ANALISI DOCUMENTI DEMO PER PROGETTAZIONE ARCHITETTURA")
    print("=" * 80)
    
    demo_dir = Path("documents demo")
    pdf_files = list(demo_dir.glob("*.pdf"))
    
    print(f"Documenti trovati: {len(pdf_files)}")
    
    results = {}
    
    for pdf_file in pdf_files:
        result = analizza_documento_pdf(str(pdf_file))
        if result:
            results[pdf_file.name] = result
    
    # Riassunto finale
    print(f"\n{'='*80}")
    print("RIASSUNTO FINALE")
    print(f"{'='*80}")
    
    native_docs = []
    scanned_docs = []
    
    for name, data in results.items():
        if data['is_native']:
            native_docs.append((name, data))
        elif data['is_scanned']:
            scanned_docs.append((name, data))
        else:
            print(f"  {name}: Documento misto ({data['total_chars']:,} caratteri)")
    
    print(f"\nDOCUMENTI NATIVI ({len(native_docs)}):")
    for name, data in native_docs:
        print(f"  - {name}: {data['total_chars']:,} caratteri, {data['pages_with_content']} pagine")
    
    print(f"\nDOCUMENTI SCANNERIZZATI ({len(scanned_docs)}):")
    for name, data in scanned_docs:
        print(f"  - {name}: {data['total_chars']:,} caratteri, {data['pages_with_content']} pagine")
    
    print(f"\nREQUISITI ARCHITETTURA:")
    print(f"  - Gestire documenti nativi: {len(native_docs)} documenti")
    print(f"  - Gestire documenti scannerizzati: {len(scanned_docs)} documenti")
    print(f"  - Preservare layout originale")
    print(f"  - Traduzione offline completa")
    print(f"  - Generazione DOCX con formattazione")

if __name__ == "__main__":
    main()
