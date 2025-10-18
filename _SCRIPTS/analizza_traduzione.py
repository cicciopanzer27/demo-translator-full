#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per analizzare la qualità della traduzione
"""

import os
import sys
os.environ['PYTHONIOENCODING'] = 'utf-8'

from pathlib import Path
from docx import Document
import re

def analizza_documento_tradotto(docx_path):
    """Analizza il documento tradotto e mostra statistiche"""
    
    if not os.path.exists(docx_path):
        print(f"❌ File non trovato: {docx_path}")
        return
    
    print("=" * 80)
    print("ANALISI QUALITA TRADUZIONE")
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
        
        # Statistiche base
        total_paragraphs = len(paragraphs)
        total_chars = len(full_text)
        total_words = len(full_text.split())
        
        print(f"STATISTICHE DOCUMENTO:")
        print(f"   - Paragrafi: {total_paragraphs}")
        print(f"   - Caratteri: {total_chars:,}")
        print(f"   - Parole: {total_words:,}")
        print()
        
        # Controlla problemi comuni
        print("ANALISI QUALITA:")
        
        # 1. Controlla se il testo è vuoto
        if total_chars < 100:
            print("   PROBLEMA: Documento quasi vuoto!")
            print("   Possibili cause:")
            print("      - Errore nell'estrazione del testo originale")
            print("      - Problema nel processo di traduzione")
            print("      - Errore nella generazione DOCX")
            return
        
        # 2. Controlla caratteri strani
        strange_chars = re.findall(r'[^\w\s\.\,\;\:\!\?\(\)\[\]\{\}\-\+\=\/\@\#\$\%\&\*]', full_text)
        if strange_chars:
            print(f"   Caratteri strani trovati: {len(set(strange_chars))} tipi")
            print(f"      Esempi: {list(set(strange_chars))[:10]}")
        
        # 3. Controlla se ci sono solo caratteri inglesi (possibile problema traduzione)
        italian_chars = re.findall(r'[àèéìíîòóùú]', full_text, re.IGNORECASE)
        english_chars = re.findall(r'[a-zA-Z]', full_text)
        
        if len(english_chars) > len(italian_chars) * 10:
            print("   Testo principalmente in inglese (traduzione riuscita)")
        elif len(italian_chars) > len(english_chars) * 10:
            print("   Testo principalmente in italiano (possibile problema traduzione)")
        else:
            print("   Mix di lingue (verificare qualita)")
        
        # 4. Mostra primi paragrafi per valutazione
        print()
        print("ANTEPRIMA CONTENUTO:")
        print("-" * 60)
        
        for i, para in enumerate(paragraphs[:5]):
            if len(para) > 100:
                preview = para[:100] + "..."
            else:
                preview = para
            print(f"{i+1:2d}. {preview}")
        
        if len(paragraphs) > 5:
            print(f"    ... e altri {len(paragraphs) - 5} paragrafi")
        
        print("-" * 60)
        
        # 5. Controlla struttura
        print()
        print("STRUTTURA DOCUMENTO:")
        
        # Conta titoli (paragrafi con stile)
        titles = 0
        for para in doc.paragraphs:
            if para.style.name.startswith('Heading') or para.style.name.startswith('Title'):
                titles += 1
        
        print(f"   - Titoli/Intestazioni: {titles}")
        print(f"   - Paragrafi normali: {total_paragraphs - titles}")
        
        # 6. Suggerimenti per miglioramenti
        print()
        print("SUGGERIMENTI:")
        
        if total_chars < 1000:
            print("   - Documento molto breve - verificare estrazione originale")
        
        if titles == 0:
            print("   - Nessun titolo rilevato - possibile perdita di struttura")
        
        if len(strange_chars) > 50:
            print("   - Molti caratteri strani - verificare encoding")
        
        print("   - Controllare manualmente la qualita della traduzione")
        print("   - Verificare che i numeri e date siano corretti")
        print("   - Controllare che la terminologia legale sia appropriata")
        
    except Exception as e:
        print(f"Errore nell'analisi: {e}")
        print("Possibili cause:")
        print("   - File DOCX corrotto")
        print("   - Problema con python-docx")
        print("   - File non e un DOCX valido")

def main():
    # Percorso del documento tradotto
    docx_path = r"C:\Users\jecho\Documents\[2003] MCS TS PAI_Sirio Analtix srl_ DA & AM1 (IND) - FE [2020-Evergreen]_tradotto.docx"
    
    print("ANALISI DOCUMENTO TRADOTTO")
    print("=" * 50)
    
    analizza_documento_tradotto(docx_path)
    
    print()
    print("=" * 80)
    print("ANALISI COMPLETATA")
    print("=" * 80)

if __name__ == "__main__":
    main()
