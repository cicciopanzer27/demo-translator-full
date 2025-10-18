#!/usr/bin/env python3
"""
Script veloce per installare solo la coppia EN-IT (più veloce del setup completo)
"""

import argostranslate.package
import argostranslate.translate

print("=" * 60)
print("Installazione Modelli Base - Traduttore Documenti")
print("=" * 60)
print("\n🔄 Aggiornamento indice pacchetti...")

try:
    argostranslate.package.update_package_index()
    print("✅ Indice aggiornato")
    
    available = argostranslate.package.get_available_packages()
    
    # Installa solo EN → IT per test veloce
    print("\n📥 Download modello Inglese → Italiano...")
    pkg_en_it = next(filter(lambda x: x.from_code == 'en' and x.to_code == 'it', available), None)
    
    if pkg_en_it:
        download_path = pkg_en_it.download()
        print("   Installazione...")
        argostranslate.package.install_from_path(download_path)
        print("✅ Modello EN → IT installato!")
    else:
        print("❌ Pacchetto non trovato")
    
    print("\n" + "=" * 60)
    print("✅ Setup completato!")
    print("=" * 60)
    print("\n✨ Ora puoi tradurre documenti da Inglese a Italiano!")
    print("   Riavvia l'applicazione se è già aperta.")
    
except Exception as e:
    print(f"\n❌ Errore: {e}")
    print("\nVerifica la connessione internet e riprova.")

