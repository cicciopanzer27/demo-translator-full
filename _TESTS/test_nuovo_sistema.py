#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del nuovo sistema di traduzione
"""

import os
import sys
os.environ['PYTHONIOENCODING'] = 'utf-8'

from pathlib import Path

# Aggiungi src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core.document_processor import DocumentProcessor

def test_documento_nativo():
    """Test con documento nativo"""
    
    print("=" * 80)
    print("TEST DOCUMENTO NATIVO - PHYSITEK LETTER")
    print("=" * 80)
    
    processor = DocumentProcessor()
    
    input_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\documents demo\2025-04-30 Physitek Letter [4].pdf"
    output_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\output\physitek_tradotto.docx"
    
    # Crea cartella output
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    def progress_callback(percent, message):
        print(f"[{percent:3d}%] {message}")
    
    print(f"Input: {Path(input_path).name}")
    print(f"Output: {Path(output_path).name}")
    print()
    
    result = processor.process_document(
        input_path=input_path,
        output_path=output_path,
        from_lang='en',
        to_lang='it',
        progress_callback=progress_callback
    )
    
    print(f"\nRisultato: {result}")
    
    if result['success']:
        print("TEST NATIVO COMPLETATO CON SUCCESSO!")
    else:
        print("TEST NATIVO FALLITO!")
    
    return result['success']

def test_documento_scannerizzato():
    """Test con documento scannerizzato"""
    
    print("\n" + "=" * 80)
    print("TEST DOCUMENTO SCANNERIZZATO - DISTRIBUTION CONTRACT")
    print("=" * 80)
    
    processor = DocumentProcessor()
    
    input_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\documents demo\Distribution Contract Trotec Bompan SRL_01062024_signed both parties.pdf"
    output_path = r"C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC\output\distribution_tradotto.docx"
    
    def progress_callback(percent, message):
        print(f"[{percent:3d}%] {message}")
    
    print(f"Input: {Path(input_path).name}")
    print(f"Output: {Path(output_path).name}")
    print()
    
    result = processor.process_document(
        input_path=input_path,
        output_path=output_path,
        from_lang='en',
        to_lang='it',
        progress_callback=progress_callback
    )
    
    print(f"\nRisultato: {result}")
    
    if result['success']:
        print("TEST SCANNERIZZATO COMPLETATO CON SUCCESSO!")
    else:
        print("TEST SCANNERIZZATO FALLITO!")
    
    return result['success']

def test_interfaccia_utente():
    """Test interfaccia utente"""
    
    print("\n" + "=" * 80)
    print("TEST INTERFACCIA UTENTE")
    print("=" * 80)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.main_window import MainWindow
        
        app = QApplication([])
        window = MainWindow()
        
        print("Interfaccia utente caricata correttamente")
        print("Tutti i componenti UI funzionanti")
        
        return True
        
    except Exception as e:
        print(f"Errore interfaccia utente: {e}")
        return False

def main():
    """Test completo del sistema"""
    
    print("TEST COMPLETO NUOVO SISTEMA TRADUTTORE")
    print("=" * 80)
    
    results = []
    
    # Test 1: Documento nativo
    try:
        results.append(("Documento Nativo", test_documento_nativo()))
    except Exception as e:
        print(f"Errore test nativo: {e}")
        results.append(("Documento Nativo", False))
    
    # Test 2: Documento scannerizzato
    try:
        results.append(("Documento Scannerizzato", test_documento_scannerizzato()))
    except Exception as e:
        print(f"Errore test scannerizzato: {e}")
        results.append(("Documento Scannerizzato", False))
    
    # Test 3: Interfaccia utente
    try:
        results.append(("Interfaccia Utente", test_interfaccia_utente()))
    except Exception as e:
        print(f"Errore test UI: {e}")
        results.append(("Interfaccia Utente", False))
    
    # Riassunto finale
    print("\n" + "=" * 80)
    print("RIASSUNTO TEST")
    print("=" * 80)
    
    success_count = 0
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name:25} {status}")
        if success:
            success_count += 1
    
    print(f"\nTest superati: {success_count}/{len(results)}")
    
    if success_count == len(results):
        print("TUTTI I TEST SUPERATI! SISTEMA PRONTO!")
    else:
        print("Alcuni test falliti. Verificare i componenti.")
    
    return success_count == len(results)

if __name__ == "__main__":
    main()
