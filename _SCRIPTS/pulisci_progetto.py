#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per pulizia e riorganizzazione del progetto
"""

import os
import shutil
from pathlib import Path

def pulisci_progetto():
    """Pulisce e riorganizza il progetto"""
    
    base_dir = Path(__file__).parent.parent
    
    print("🧹 PULIZIA PROGETTO IN CORSO...")
    print("=" * 50)
    
    # 1. Pulisci file temporanei
    print("1. Rimozione file temporanei...")
    temp_files = [
        "*.pyc", "__pycache__", "*.log", "*.tmp", "*.temp"
    ]
    
    for pattern in temp_files:
        for file_path in base_dir.rglob(pattern):
            if file_path.is_file():
                file_path.unlink()
                print(f"   Rimosso: {file_path.name}")
            elif file_path.is_dir():
                shutil.rmtree(file_path)
                print(f"   Rimosso: {file_path.name}")
    
    # 2. Pulisci cartelle vuote
    print("\n2. Rimozione cartelle vuote...")
    for dir_path in base_dir.rglob("*"):
        if dir_path.is_dir() and not any(dir_path.iterdir()):
            if dir_path.name != "venv":  # Non rimuovere venv
                dir_path.rmdir()
                print(f"   Rimosso: {dir_path.name}")
    
    # 3. Organizza file di output
    print("\n3. Organizzazione file di output...")
    output_dir = base_dir / "output"
    if output_dir.exists():
        for file_path in output_dir.glob("*"):
            if file_path.is_file():
                # Crea sottocartelle per data
                date_str = file_path.stat().st_mtime
                date_dir = output_dir / f"output_{int(date_str)}"
                date_dir.mkdir(exist_ok=True)
                
                # Sposta file
                new_path = date_dir / file_path.name
                file_path.rename(new_path)
                print(f"   Spostato: {file_path.name}")
    
    # 4. Pulisci log vecchi
    print("\n4. Pulizia log vecchi...")
    logs_dir = base_dir / "logs"
    if logs_dir.exists():
        for log_file in logs_dir.glob("*.log"):
            if log_file.stat().st_size > 10 * 1024 * 1024:  # > 10MB
                log_file.unlink()
                print(f"   Rimosso log grande: {log_file.name}")
    
    print("\n✅ PULIZIA COMPLETATA!")
    print("=" * 50)

if __name__ == "__main__":
    pulisci_progetto()
