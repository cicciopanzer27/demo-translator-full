#!/bin/bash

echo "=========================================="
echo " Traduttore Documenti Legali Offline"
echo "=========================================="
echo ""

# Attiva virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "ERRORE: Virtual environment non trovato!"
    echo "Esegui prima: python3 -m venv venv"
    echo "              source venv/bin/activate"
    echo "              pip install -r requirements.txt"
    exit 1
fi

# Avvia applicazione
echo "Avvio applicazione..."
python src/main.py

# Se l'applicazione termina con errore
if [ $? -ne 0 ]; then
    echo ""
    echo "ERRORE durante l'esecuzione!"
    echo "Controlla i log in logs/translator.log"
    read -p "Premi INVIO per chiudere..."
fi

