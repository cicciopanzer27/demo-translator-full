# 📄 Traduttore Documenti Legali Offline

Sistema di traduzione documenti PDF/DOCX completamente **offline** per documenti legali e professionali.

## ✨ Caratteristiche

- ✅ **100% Offline** - Nessuna connessione internet richiesta dopo installazione
- 📄 **Formati Supportati** - PDF, DOCX, DOC
- 🌍 **Multilingua** - Italiano, Inglese, Spagnolo, Francese, Tedesco, Portoghese, Russo
- 🎯 **Preservazione Layout** - Mantiene struttura base dei documenti
- 🚀 **Performance** - ~30 sec per 5 pagine, ~2 min per 20 pagine
- 🔒 **Privacy** - Tutti i dati restano sul tuo PC

---

## 🚀 Quick Start

### 1. Requisiti
- **Python 3.10 o 3.11**
- **Windows 10/11, Linux, o macOS**

### 2. Installazione

```bash
# Clona o scarica il progetto
cd TRANSLATOR_LAC

# Crea ambiente virtuale
python -m venv venv

# Attiva ambiente
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac

# Installa dipendenze
pip install -r requirements.txt
```

### 3. Test Sistema

```bash
python test_sistema.py
```

Se vedi `[SUCCESS] TUTTI I TEST COMPLETATI CON SUCCESSO!`, sei pronto!

### 4. Avvia l'Applicazione

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
./run.sh
```

**Manualmente:**
```bash
# Assicurati che l'ambiente virtuale sia attivo
python src/main.py
```

---

## 📖 Guida Utilizzo

### Prima Traduzione

1. **Scarica Modelli di Traduzione**
   - Clicca su `Gestisci Modelli`
   - Seleziona coppia lingua (es: `Italiano → Inglese`)
   - Clicca `📥 Scarica Selezionato`
   - Attendi download (50-200 MB)

2. **Traduci Documento**
   - Seleziona lingua sorgente e destinazione
   - Clicca `SELEZIONA FILE` (PDF o DOCX)
   - Clicca `SELEZIONA CARTELLA` per output
   - Clicca `TRADUCI`
   - Attendi completamento

3. **Risultato**
   - Il documento tradotto sarà nella cartella scelta
   - Nome formato: `[originale]_translated_[lingua].[ext]`

---

## 🔧 Modelli di Traduzione

### Lingue Disponibili
- 🇮🇹 Italiano
- 🇬🇧 Inglese
- 🇪🇸 Spagnolo
- 🇫🇷 Francese
- 🇩🇪 Tedesco
- 🇵🇹 Portoghese
- 🇷🇺 Russo

### Installare Modelli

I modelli sono scaricati da **Argos Translate** (open source).

**Modelli Consigliati:**
- `it → en` (Italiano → Inglese)
- `en → it` (Inglese → Italiano)
- `en → [altra lingua]` per traduzione tramite pivot

**Nota:** Se una coppia diretta non è disponibile, il sistema usa automaticamente l'inglese come lingua intermedia (es: IT→RU = IT→EN→RU)

---

## 📊 Performance

| Documento | Tempo Stimato | Note |
|-----------|---------------|------|
| 5 pagine  | ~30 secondi   | Dipende da CPU |
| 20 pagine | ~2 minuti     | |
| 50 pagine | ~5 minuti     | Chiudi altre app |
| 100+ pagine | ~10+ minuti  | Dividi in parti |

---

## 🐛 Troubleshooting

### "Nessun modello installato"
**Soluzione:** Apri `Gestisci Modelli` e scarica almeno una coppia di lingue

### "Modello X→Y non disponibile"
**Soluzione:** 
1. Scarica il modello mancante da `Gestisci Modelli`
2. Oppure il sistema userà traduzione tramite pivot (automatico)

### Errori di importazione
```bash
# Reinstalla dipendenze
pip install -r requirements.txt --force-reinstall
```

### GUI non si avvia
```bash
# Verifica Python
python --version  # Deve essere 3.10 o 3.11

# Reinstalla PyQt6
pip install PyQt6 --force-reinstall

# Test sistema
python test_sistema.py
```

### Log degli errori
Controlla i log in:
- `logs/translator.log`

---

## 📁 Struttura Progetto

```
TRANSLATOR_LAC/
├── src/
│   ├── extraction/         # Estrazione testo da PDF/DOCX
│   ├── translation/        # Engine traduzione e chunking
│   ├── generation/         # Generazione PDF/DOCX output
│   ├── ui/                 # Interfaccia PyQt6
│   ├── workers/            # Thread background
│   └── main.py             # Entry point
│
├── glossaries/             # Terminologia legale custom
├── logs/                   # Log applicazione
├── test_sistema.py         # Script test
├── requirements.txt        # Dipendenze Python
├── run.bat / run.sh        # Script avvio
├── GUIDA_VELOCE.md         # Guida dettagliata
└── README.md               # Questo file
```

---

## 🛠️ Tecnologie

- **GUI:** PyQt6
- **PDF:** PyMuPDF (fitz), pdf2docx, ReportLab
- **DOCX:** python-docx
- **Traduzione:** Argos Translate (modelli NMT offline)
- **Backend:** Python 3.10+

---

## 📝 Note

### Limitazioni
- **Layout:** Preservazione base (paragrafi, heading). Layout complessi potrebbero essere semplificati
- **OCR:** Moduli OCR disponibili ma opzionali. Questa versione funziona meglio con PDF nativi
- **Dimensioni:** Documenti 100+ pagine richiedono più tempo e RAM

### Privacy e Sicurezza
- ✅ **Nessun dato inviato online**
- ✅ **Tutto elaborato localmente**
- ✅ **Modelli open source**
- ✅ **Codice verificabile**

---

## 🤝 Supporto

Per problemi:
1. Esegui `python test_sistema.py` e verifica output
2. Controlla `logs/translator.log`
3. Verifica dipendenze: `pip list`

---

## 📄 Licenza

Questo progetto usa componenti open source:
- **Argos Translate** - MIT License
- **PyQt6** - GPL v3
- **PyMuPDF** - AGPL v3
- **python-docx** - MIT License

---

## 🎯 Roadmap Futura

Il blueprint completo per sistema OCR avanzato è disponibile in `blueprint.md`.

Funzionalità future potrebbero includere:
- OCR avanzato per documenti scannerizzati
- Preservazione layout pixel-perfect
- Glossari legali personalizzati
- Batch processing multipli file
- API server locale

---

**Versione:** 1.0.0 (Pulita e Funzionante)  
**Data:** Ottobre 2024  
**Status:** ✅ Pronto per produzione
