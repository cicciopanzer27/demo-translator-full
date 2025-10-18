#!/usr/bin/env python3
"""
Script per installare modelli di traduzione base
"""

import argostranslate.package
import argostranslate.translate

def install_language_pair(from_code, to_code):
    """Installa coppia di lingue"""
    print(f"\n📥 Installazione modello {from_code} → {to_code}...")
    
    try:
        available_packages = argostranslate.package.get_available_packages()
        
        package = next(
            filter(lambda x: x.from_code == from_code and x.to_code == to_code, available_packages),
            None
        )
        
        if not package:
            print(f"❌ Pacchetto {from_code} → {to_code} non trovato")
            return False
        
        print(f"   Download {package.package_version}...")
        download_path = package.download()
        
        print(f"   Installazione...")
        argostranslate.package.install_from_path(download_path)
        
        print(f"✅ Modello {from_code} → {to_code} installato")
        return True
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

def main():
    print("=" * 60)
    print("Setup Modelli di Traduzione - Traduttore Documenti Legali")
    print("=" * 60)
    
    print("\n🔄 Aggiornamento indice pacchetti...")
    argostranslate.package.update_package_index()
    print("✅ Indice aggiornato")
    
    # Installa coppie base
    pairs = [
        ('en', 'it'),  # Inglese → Italiano
        ('it', 'en'),  # Italiano → Inglese
        ('en', 'es'),  # Inglese → Spagnolo
        ('es', 'en'),  # Spagnolo → Inglese
        ('en', 'fr'),  # Inglese → Francese
        ('fr', 'en'),  # Francese → Inglese
    ]
    
    print(f"\n📦 Installazione {len(pairs)} coppie di lingue...")
    
    success = 0
    for from_code, to_code in pairs:
        if install_language_pair(from_code, to_code):
            success += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Installati {success}/{len(pairs)} modelli")
    print("=" * 60)
    
    if success > 0:
        print("\n✨ Setup completato! Ora puoi avviare l'applicazione con:")
        print("   python src/main.py")
    else:
        print("\n⚠️  Nessun modello installato. Verifica la connessione internet.")

if __name__ == '__main__':
    main()

