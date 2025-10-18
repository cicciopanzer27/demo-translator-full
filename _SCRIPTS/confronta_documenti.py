#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per confrontare documento originale e tradotto
"""

import os
import sys
os.environ['PYTHONIOENCODING'] = 'utf-8'

from pathlib import Path
from docx import Document
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from extraction.pdf_extractor import PDFExtractor

def analizza_documento_originale(pdf_path):
    """Analizza il documento PDF originale"""
    
    print("=" * 80)
    print("ANALISI DOCUMENTO ORIGINALE")
    print("=" * 80)
    print(f"File: {Path(pdf_path).name}")
    print(f"Percorso: {pdf_path}")
    print()
    
    try:
        # Estrai testo dal PDF
        extractor = PDFExtractor()
        pages_data = extractor.extract_text_with_layout(pdf_path)
        
        # Statistiche
        total_pages = len(pages_data)
        total_chars = 0
        total_words = 0
        paragraphs = 0
        
        print(f"STATISTICHE DOCUMENTO ORIGINALE:")
        print(f"   - Pagine: {total_pages}")
        
        for i, page in enumerate(pages_data):
            page_text = page.get('text', '')
            page_chars = len(page_text)
            page_words = len(page_text.split())
            page_paras = len([p for p in page_text.split('\n\n') if p.strip()])
            
            total_chars += page_chars
            total_words += page_words
            paragraphs += page_paras
            
            print(f"   - Pagina {i+1}: {page_chars:,} caratteri, {page_words:,} parole, {page_paras} paragrafi")
            
            # Mostra anteprima prima pagina
            if i == 0:
                print()
                print("ANTEPRIMA PRIMA PAGINA:")
                print("-" * 60)
                preview = page_text[:500] + "..." if len(page_text) > 500 else page_text
                print(preview)
                print("-" * 60)
        
        print()
        print(f"TOTALE ORIGINALE:")
        print(f"   - Caratteri: {total_chars:,}")
        print(f"   - Parole: {total_words:,}")
        print(f"   - Paragrafi: {paragraphs}")
        
        return {
            'pages': total_pages,
            'chars': total_chars,
            'words': total_words,
            'paragraphs': paragraphs
        }
        
    except Exception as e:
        print(f"Errore nell'analisi: {e}")
        return None

def analizza_documento_tradotto(docx_path):
    """Analizza il documento tradotto"""
    
    print("=" * 80)
    print("ANALISI DOCUMENTO TRADOTTO")
    print("=" * 80)
    print(f"File: {Path(docx_path).name}")
    print(f"Percorso: {docx_path}")
    print()
    
    try:
        # Carica documento
        doc = Document(docx_path)
        
        # Estrai tutto il testo
        full_text = ""
        paragraphs = []
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                paragraphs.append(text)
                full_text += text + "\n"
        
        # Statistiche
        total_paragraphs = len(paragraphs)
        total_chars = len(full_text)
        total_words = len(full_text.split())
        
        print(f"STATISTICHE DOCUMENTO TRADOTTO:")
        print(f"   - Paragrafi: {total_paragraphs}")
        print(f"   - Caratteri: {total_chars:,}")
        print(f"   - Parole: {total_words:,}")
        
        # Mostra anteprima
        print()
        print("ANTEPRIMA CONTENUTO TRADOTTO:")
        print("-" * 60)
        for i, para in enumerate(paragraphs[:3]):
            preview = para[:200] + "..." if len(para) > 200 else para
            print(f"{i+1}. {preview}")
        print("-" * 60)
        
        return {
            'chars': total_chars,
            'words': total_words,
            'paragraphs': total_paragraphs
        }
        
    except Exception as e:
        print(f"Errore nell'analisi: {e}")
        return None

def confronta_risultati(originale, tradotto):
    """Confronta i risultati"""
    
    print("=" * 80)
    print("CONFRONTO RISULTATI")
    print("=" * 80)
    
    if not originale or not tradotto:
        print("Impossibile confrontare - dati mancanti")
        return
    
    # Calcola percentuali
    char_ratio = (tradotto['chars'] / originale['chars']) * 100 if originale['chars'] > 0 else 0
    word_ratio = (tradotto['words'] / originale['words']) * 100 if originale['words'] > 0 else 0
    para_ratio = (tradotto['paragraphs'] / originale['paragraphs']) * 100 if originale['paragraphs'] > 0 else 0
    
    print(f"CONFRONTO CONTENUTO:")
    print(f"   - Caratteri: {tradotto['chars']:,} / {originale['chars']:,} ({char_ratio:.1f}%)")
    print(f"   - Parole: {tradotto['words']:,} / {originale['words']:,} ({word_ratio:.1f}%)")
    print(f"   - Paragrafi: {tradotto['paragraphs']} / {originale['paragraphs']} ({para_ratio:.1f}%)")
    print()
    
    # Diagnosi
    print("DIAGNOSI PROBLEMI:")
    
    if char_ratio < 50:
        print("   PROBLEMA GRAVE: Meno del 50% del contenuto e stato tradotto!")
        print("   Possibili cause:")
        print("      - Errore nell'estrazione del testo PDF")
        print("      - Problema nel chunking del documento")
        print("      - Errore nel processo di traduzione")
        print("      - Problema nella generazione DOCX")
    elif char_ratio < 80:
        print("   PROBLEMA MODERATO: Circa il 70-80% del contenuto e stato tradotto")
        print("   Verificare:")
        print("      - Se alcune pagine sono state saltate")
        print("      - Se il chunking ha funzionato correttamente")
    else:
        print("   OK: La maggior parte del contenuto e stata tradotta")
    
    if para_ratio < 30:
        print("   PROBLEMA STRUTTURA: Perdita significativa di struttura del documento")
        print("   Verificare:")
        print("      - Se i paragrafi sono stati preservati correttamente")
        print("      - Se il layout e stato mantenuto")
    
    print()
    print("RACCOMANDAZIONI:")
    if char_ratio < 50:
        print("   1. Verificare l'estrazione del PDF originale")
        print("   2. Controllare i log di traduzione")
        print("   3. Testare con un documento piu semplice")
        print("   4. Verificare che il modello di traduzione sia installato")
    else:
        print("   1. Verificare la qualita della traduzione manualmente")
        print("   2. Controllare che i numeri e date siano corretti")
        print("   3. Verificare la terminologia legale")

def main():
    # Percorsi
    pdf_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\documents demo\[2003] MCS TS PAI_Sirio Analtix srl_ DA & AM1 (IND) - FE [2020-Evergreen].pdf"
    docx_path = r"C:\Users\jecho\Documents\[2003] MCS TS PAI_Sirio Analtix srl_ DA & AM1 (IND) - FE [2020-Evergreen]_tradotto.docx"
    
    print("CONFRONTO DOCUMENTO ORIGINALE VS TRADOTTO")
    print("=" * 80)
    
    # Analizza originale
    originale = analizza_documento_originale(pdf_path)
    
    # Analizza tradotto
    tradotto = analizza_documento_tradotto(docx_path)
    
    # Confronta
    confronta_risultati(originale, tradotto)
    
    print()
    print("=" * 80)
    print("ANALISI COMPLETATA")
    print("=" * 80)

if __name__ == "__main__":
    main()
