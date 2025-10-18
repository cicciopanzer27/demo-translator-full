# 🚀 Guida Veloce - Traduttore Documenti Legali

## Cosa fa questo software?

Traduce **documenti PDF e DOCX** tra diverse lingue in modo **100% offline** (nessuna connessione internet necessaria dopo l'installazione iniziale).

---

## ✅ Installazione (Prima Volta)

### 1. Installa Python
- Scarica Python 3.10 o 3.11 da: https://python.org
- ⚠️ Durante l'installazione, seleziona **"Add Python to PATH"**

### 2. Installa le dipendenze
Apri il terminale nella cartella del progetto e digita:

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Testa il sistema
```bash
python test_sistema.py
```

---

## 🎯 Uso del Software

### Avvio Rapido

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
# Attiva l'ambiente virtuale
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Avvia l'applicazione
python src/main.py
```

### Prima Traduzione

1. **Scarica i modelli di traduzione**
   - Clicca su `Gestisci Modelli`
   - Seleziona la coppia di lingue (es: `Italiano → Inglese`)
   - Clicca `📥 Scarica Selezionato`
   - Attendi il download (~50-200 MB per modello)

2. **Traduci un documento**
   - Seleziona lingua di partenza (es: Italiano)
   - Seleziona lingua di arrivo (es: Inglese)
   - Clicca `SELEZIONA FILE` e scegli il PDF o DOCX
   - Clicca `SELEZIONA CARTELLA` per l'output
   - Clicca `TRADUCI` ✨

3. **Attendi il completamento**
   - La barra di progresso mostra l'avanzamento
   - Al termine, il documento tradotto sarà nella cartella scelta

---

## 🔧 Modelli di Traduzione

### Lingue Supportate
- 🇮🇹 Italiano
- 🇬🇧 Inglese
- 🇪🇸 Spagnolo
- 🇫🇷 Francese
- 🇩🇪 Tedesco
- 🇵🇹 Portoghese
- 🇷🇺 Russo

### Traduzione Pivot (Automatica)
Se la coppia diretta non è disponibile, il sistema usa l'inglese come lingua intermedia:
- Esempio: Italiano → Russo = Italiano → Inglese → Russo

### Installare Modelli Aggiuntivi
1. Apri l'applicazione
2. Clicca `Gestisci Modelli`
3. Clicca `🔄 Aggiorna Lista`
4. Seleziona e scarica i modelli necessari

---

## 📊 Performance Attese

| Documento | Tempo Stimato |
|-----------|---------------|
| 5 pagine  | ~30 secondi   |
| 20 pagine | ~2 minuti     |
| 50 pagine | ~5 minuti     |

*I tempi variano in base alla lunghezza del testo e alla velocità del PC*

---

## 🐛 Risoluzione Problemi

### "Nessun modello installato"
**Soluzione:** Clicca su `Gestisci Modelli` e scarica almeno una coppia di lingue

### "Modello X→Y non disponibile"
**Soluzione:** Scarica il modello dalla finestra `Gestisci Modelli`

### Errore durante l'importazione
**Soluzione:** 
```bash
# Reinstalla dipendenze
pip install -r requirements.txt --force-reinstall
```

### GUI non si avvia
**Soluzione:**
1. Verifica Python versione: `python --version` (deve essere 3.10-3.11)
2. Reinstalla PyQt6: `pip install PyQt6 --force-reinstall`
3. Esegui: `python test_sistema.py`

---

## 📁 Struttura File Output

Il documento tradotto avrà nome:
```
[nome_originale]_translated_[lingua].[estensione]
```

Esempio:
- Input: `contratto_affitto.pdf`
- Output: `contratto_affitto_translated_en.pdf`

---

## 💡 Suggerimenti

1. **Per documenti lunghi (50+ pagine):**
   - Chiudi altre applicazioni per liberare RAM
   - Il processo può richiedere 5-10 minuti

2. **Per miglior qualità:**
   - Usa PDF nativi (non scansioni) quando possibile
   - Dividi documenti molto lunghi (100+ pagine) in parti più piccole

3. **Privacy:**
   - Tutto funziona offline, nessun dato viene inviato online
   - I modelli sono scaricati una sola volta e restano sul PC

---

## 🆘 Supporto

Per problemi o domande:
1. Esegui `python test_sistema.py` e condividi l'output
2. Controlla i log in `logs/translator.log`
3. Verifica che tutte le dipendenze siano installate: `pip list`

---

## 📝 Note Tecniche

- **Modelli:** Argos Translate (open source)
- **Formato supportato:** PDF, DOCX, DOC
- **Output:** Stesso formato dell'input (PDF→PDF, DOCX→DOCX)
- **Preservazione layout:** Limitata (mantiene paragrafi, heading base)
- **OCR:** Non incluso in questa versione (solo testo nativo)

---

## ✅ Checklist Installazione

- [ ] Python 3.10 o 3.11 installato
- [ ] Ambiente virtuale creato (`venv`)
- [ ] Dipendenze installate (`pip install -r requirements.txt`)
- [ ] Test sistema eseguito con successo (`python test_sistema.py`)
- [ ] Almeno un modello di traduzione scaricato
- [ ] Prima traduzione test completata

**Tutto funzionante? Sei pronto! 🎉**

