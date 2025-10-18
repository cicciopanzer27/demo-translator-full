#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test con documento più semplice per verificare il sistema
"""

import os
import sys
os.environ['PYTHONIOENCODING'] = 'utf-8'

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from extraction.pdf_extractor import PDFExtractor

def test_documento_semplice():
    """Test con Physitek Letter (documento più semplice)"""
    
    pdf_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\documents demo\2025-04-30 Physitek Letter [4].pdf"
    
    print("=" * 80)
    print("TEST DOCUMENTO SEMPLICE - PHYSITEK LETTER")
    print("=" * 80)
    print(f"File: {Path(pdf_path).name}")
    print()
    
    try:
        extractor = PDFExtractor()
        pages_data = extractor.extract_text_with_layout(pdf_path)
        
        print(f"Pagine estratte: {len(pages_data)}")
        
        total_chars = 0
        total_words = 0
        
        for i, page in enumerate(pages_data):
            text = page.get('text', '')
            char_count = len(text)
            word_count = len(text.split())
            
            total_chars += char_count
            total_words += word_count
            
            print(f"Pagina {i+1}: {char_count:,} caratteri, {word_count:,} parole")
            
            # Mostra anteprima prima pagina
            if i == 0:
                print()
                print("ANTEPRIMA PRIMA PAGINA:")
                print("-" * 60)
                preview = text[:500] + "..." if len(text) > 500 else text
                print(preview)
                print("-" * 60)
        
        print()
        print(f"TOTALE:")
        print(f"  - Caratteri: {total_chars:,}")
        print(f"  - Parole: {total_words:,}")
        
        if total_chars > 1000:
            print("DOCUMENTO RICCO DI CONTENUTO - PERFETTO PER TEST!")
        else:
            print("Documento con poco contenuto")
        
        return total_chars, total_words
        
    except Exception as e:
        print(f"Errore: {e}")
        return 0, 0

def test_traduzione_completa():
    """Test traduzione completa con Physitek Letter"""
    
    print("\n" + "=" * 80)
    print("TEST TRADUZIONE COMPLETA")
    print("=" * 80)
    
    # Simula il processo di traduzione
    from workers.clean_worker import CleanWorker
    from PyQt6.QtCore import QCoreApplication
    
    app = QCoreApplication([])
    
    # Percorsi
    input_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\documents demo\2025-04-30 Physitek Letter [4].pdf"
    output_dir = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\test_output"
    
    # Crea cartella output
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Input: {input_path}")
    print(f"Output: {output_dir}")
    print()
    
    # Crea worker
    worker = CleanWorker(
        input_path=input_path,
        output_dir=output_dir,
        from_lang='en',
        to_lang='it'
    )
    
    print("Avvio traduzione...")
    
    try:
        # Esegui traduzione
        worker.run()
        print("Traduzione completata!")
        
        # Verifica output
        output_file = os.path.join(output_dir, "2025-04-30 Physitek Letter [4]_tradotto.docx")
        if os.path.exists(output_file):
            print(f"File generato: {output_file}")
            
            # Analizza risultato
            from docx import Document
            doc = Document(output_file)
            
            total_text = ""
            for para in doc.paragraphs:
                total_text += para.text + "\n"
            
            char_count = len(total_text)
            word_count = len(total_text.split())
            
            print(f"Risultato: {char_count:,} caratteri, {word_count:,} parole")
            
            # Mostra anteprima
            print("\nANTEPRIMA TRADUZIONE:")
            print("-" * 60)
            preview = total_text[:500] + "..." if len(total_text) > 500 else total_text
            print(preview)
            print("-" * 60)
            
        else:
            print("File di output non trovato")
            
    except Exception as e:
        print(f"Errore nella traduzione: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("TEST SISTEMA CON DOCUMENTO SEMPLICE")
    print("=" * 80)
    
    # Test estrazione
    chars, words = test_documento_semplice()
    
    if chars > 1000:
        # Test traduzione completa
        test_traduzione_completa()
    else:
        print("\nDocumento troppo piccolo per test completo")

if __name__ == "__main__":
    main()
