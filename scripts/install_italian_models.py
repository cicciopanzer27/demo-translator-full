#!/usr/bin/env python3
"""
Installazione Modelli di Traduzione - ITALIANO CENTRALE
========================================================

Installa i modelli di traduzione con focus sull'italiano:
- IT → EN (priorità massima)
- EN → IT (priorità massima)
- IT ↔ altre lingue

"""

import argostranslate.package
import argostranslate.translate
import sys

def install_italian_models():
    """Installa modelli con italiano come lingua centrale"""
    
    print("=" * 60)
    print("INSTALLAZIONE MODELLI - ITALIANO CENTRALE")
    print("=" * 60)
    print()
    
    # Aggiorna indice pacchetti
    print("[*] Aggiornamento indice pacchetti...")
    try:
        argostranslate.package.update_package_index()
        print("[OK] Indice aggiornato\n")
    except Exception as e:
        print(f"[ERROR] Errore aggiornamento indice: {e}")
        return False
    
    # Ottieni pacchetti disponibili
    available_packages = argostranslate.package.get_available_packages()
    print(f"[INFO] Pacchetti disponibili: {len(available_packages)}\n")
    
    # Modelli PRIORITARI (italiano centrale)
    priority_models = [
        ('it', 'en', 'Italiano -> Inglese'),  # IT->EN priorita 1
        ('en', 'it', 'Inglese -> Italiano'),  # EN->IT priorita 1
        ('it', 'es', 'Italiano -> Spagnolo'),
        ('es', 'it', 'Spagnolo -> Italiano'),
        ('it', 'fr', 'Italiano -> Francese'),
        ('fr', 'it', 'Francese -> Italiano'),
        ('it', 'de', 'Italiano -> Tedesco'),
        ('de', 'it', 'Tedesco -> Italiano'),
    ]
    
    installed_count = 0
    skipped_count = 0
    failed_count = 0
    
    for from_code, to_code, description in priority_models:
        print(f"[*] Cercando: {description} ({from_code}->{to_code})...")
        
        # Trova pacchetto
        package = next(
            (pkg for pkg in available_packages 
             if pkg.from_code == from_code and pkg.to_code == to_code),
            None
        )
        
        if not package:
            print(f"   [SKIP] Pacchetto non disponibile\n")
            skipped_count += 1
            continue
        
        # Verifica se già installato
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = next((l for l in installed_languages if l.code == from_code), None)
        
        if from_lang:
            # Trova l'oggetto lingua target
            to_lang = next((l for l in installed_languages if l.code == to_code), None)
            if to_lang:
                try:
                    translation = from_lang.get_translation(to_lang)
                    if translation:
                        print(f"   [OK] Gia installato\n")
                        installed_count += 1
                        continue
                except:
                    pass  # Non installato, procedi con installazione
        
        # Installa
        try:
            print(f"   [DOWNLOAD] Download in corso...")
            download_path = package.download()
            
            print(f"   [INSTALL] Installazione...")
            argostranslate.package.install_from_path(download_path)
            
            print(f"   [OK] Installato con successo!\n")
            installed_count += 1
            
        except Exception as e:
            print(f"   [ERROR] Errore: {e}\n")
            failed_count += 1
    
    # Riepilogo
    print("=" * 60)
    print("RIEPILOGO INSTALLAZIONE")
    print("=" * 60)
    print(f"[OK] Modelli installati/gia presenti: {installed_count}")
    print(f"[SKIP] Modelli non disponibili: {skipped_count}")
    print(f"[ERROR] Errori: {failed_count}")
    print()
    
    # Verifica modelli installati
    print("=" * 60)
    print("MODELLI ATTUALMENTE INSTALLATI")
    print("=" * 60)
    
    installed_languages = argostranslate.translate.get_installed_languages()
    
    if not installed_languages:
        print("[ERROR] NESSUN MODELLO INSTALLATO!")
        print("\nL'applicazione non potra tradurre senza modelli.")
        return False
    
    for lang in installed_languages:
        print(f"\n[*] {lang.name} ({lang.code})")
        translations = []
        try:
            for target in installed_languages:
                if target.code != lang.code:
                    translation = lang.get_translation(target.code)
                    if translation:
                        translations.append(f"{target.code}")
        except:
            pass
        
        if translations:
            print(f"   -> Puo tradurre verso: {', '.join(translations)}")
        else:
            print(f"   -> Nessuna traduzione disponibile")
    
    print()
    print("=" * 60)
    
    if installed_count > 0:
        print("[OK] INSTALLAZIONE COMPLETATA CON SUCCESSO!")
        print()
        print("Puoi ora avviare l'applicazione con:")
        print("  python src\\main.py")
        print("oppure:")
        print("  .\\run.bat")
        return True
    else:
        print("[ERROR] NESSUN MODELLO INSTALLATO")
        print()
        print("Verifica la connessione internet e riprova.")
        return False


if __name__ == '__main__':
    print()
    success = install_italian_models()
    print()
    
    if success:
        sys.exit(0)
    else:
        print("[ERROR] Installazione fallita o incompleta.")
        print("Riprova o controlla la connessione internet.")
        sys.exit(1)

