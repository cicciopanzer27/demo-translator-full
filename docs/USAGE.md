# 📖 Guida Utente - Traduttore Documenti Legali

## 🚀 Avvio Rapido

### Windows
Doppio click su `run.bat` oppure:
```
python src\main.py
```

### Linux/Mac
```bash
./run.sh
```
o
```bash
python src/main.py
```

## 📋 Interfaccia Utente

### 1. Sezione Lingue

**Selezione Lingua Source (Da:)**
- Seleziona la lingua del documento originale
- Lingue disponibili: Inglese, Italiano, Spagnolo, Francese, Tedesco, ecc.

**Selezione Lingua Target (A:)**
- Seleziona la lingua di destinazione
- Non può essere uguale alla lingua source

**Pulsante "Gestisci Modelli"**
- Scarica nuovi modelli linguistici
- Visualizza modelli installati
- Aggiorna indice pacchetti

### 2. Sezione File

**Documento da tradurre:**
- Click su "📄 Seleziona PDF/DOCX"
- Seleziona il file PDF o DOCX da tradurre
- Formati supportati: `.pdf`, `.docx`, `.doc`

**Cartella output:**
- Click su "📁 Seleziona Cartella"
- Scegli dove salvare il documento tradotto
- Il file manterrà il formato originale con suffisso `_translated_[lingua]`

### 3. Anteprima Documento

Dopo aver selezionato un documento, viene mostrata un'anteprima delle prime righe per verificare che il file sia stato caricato correttamente.

### 4. Traduzione

**Pulsante "🌍 Avvia Traduzione"**
- Si abilita solo quando:
  - È selezionato un documento
  - È selezionata una cartella output
  - Le lingue source e target sono diverse
- Durante la traduzione mostra progresso in tempo reale

**Barra di Progresso**
Mostra 4 fasi:
1. **0-20%**: Estrazione testo dal documento
2. **20-25%**: Preparazione chunk per traduzione
3. **25-85%**: Traduzione effettiva (la parte più lunga)
4. **85-100%**: Generazione documento output

## 📝 Esempi di Utilizzo

### Esempio 1: Contratto Inglese → Italiano

1. Avvia applicazione
2. Imposta: Da "en (Inglese)" → A "it (Italiano)"
3. Seleziona file: `contract_en.pdf`
4. Scegli cartella: `C:\Documents\Traduzioni`
5. Click "Avvia Traduzione"
6. Attendi completamento (~2-3 min per 10 pagine)
7. Output: `C:\Documents\Traduzioni\contract_en_translated_it.pdf`

### Esempio 2: Documento DOCX Italiano → Inglese

1. Imposta: Da "it (Italiano)" → A "en (Inglese)"
2. Seleziona: `relazione_legale.docx`
3. Cartella output: `Desktop`
4. Avvia traduzione
5. Output: `Desktop\relazione_legale_translated_en.docx`

### Esempio 3: Documento Lungo (50+ pagine)

Per documenti molto lunghi:

1. **Preparazione**: Verifica che il PDF non sia scansionato (deve contenere testo selezionabile)
2. **Pazienza**: Un documento di 50 pagine può richiedere 10-15 minuti
3. **Risorse**: Chiudi altri programmi pesanti per liberare RAM
4. **Monitoraggio**: Osserva la barra di progresso - non chiudere l'applicazione!

## ⚙️ Gestione Modelli

### Scaricare Nuovi Modelli

1. Click su "📥 Gestisci Modelli"
2. Click su "🔄 Aggiorna Lista" (richiede internet)
3. Seleziona coppia linguistica desiderata (es. "French → Italian")
4. Click "📥 Scarica Selezionato"
5. Attendi download e installazione
6. Chiudi dialog

**Nota**: I modelli vengono scaricati solo una volta. Dopo l'installazione, funzionano offline.

### Modelli Preinstallati (se eseguito setup_models.py)

- Inglese ↔ Italiano
- Inglese ↔ Spagnolo  
- Inglese ↔ Francese

### Modelli Disponibili

Alcune coppie comuni:
- en ↔ it (Inglese-Italiano)
- en ↔ es (Inglese-Spagnolo)
- en ↔ fr (Inglese-Francese)
- en ↔ de (Inglese-Tedesco)
- en ↔ pt (Inglese-Portoghese)
- en ↔ ru (Inglese-Russo)
- en ↔ zh (Inglese-Cinese)
- it ↔ es (Italiano-Spagnolo)
- ...e molte altre

**Importante**: Non tutte le coppie dirette sono disponibili. Se vuoi tradurre da Italiano a Cinese e il modello diretto non esiste, dovrai:
1. Tradurre IT → EN
2. Tradurre EN → ZH

## 🔍 Formato Output

### Naming Convention

Il file tradotto avrà il nome:
```
[nome_originale]_translated_[codice_lingua_target].[estensione]
```

Esempi:
- `contract.pdf` → `contract_translated_it.pdf`
- `report.docx` → `report_translated_en.docx`

### Formato Documento

Il documento tradotto:
- ✅ Mantiene la struttura in paragrafi
- ✅ Preserva le interruzioni di pagina (dove possibile)
- ✅ Mantiene lo stesso formato del documento originale (PDF→PDF, DOCX→DOCX)
- ⚠️ Può perdere formattazioni complesse (tabelle elaborate, immagini con testo)

## ⚠️ Limitazioni

### Cosa NON viene tradotto

1. **Immagini**: Il testo nelle immagini non viene estratto né tradotto
2. **Tabelle complesse**: Potrebbero non mantenere la formattazione originale
3. **Intestazioni/Piè di pagina**: Potrebbero non essere processati correttamente
4. **Font speciali**: Vengono sostituiti con font standard

### PDF Scansionati

Se il PDF è una scansione (immagine), il software **non funzionerà**. 

**Test rapido**: Prova a selezionare il testo nel PDF. Se non puoi selezionarlo, è una scansione.

**Soluzione**: Usa un software OCR prima di tradurre.

## 💡 Tips & Tricks

### Performance

**Per documenti lunghi:**
- Chiudi altri programmi
- Aumenta RAM disponibile
- Usa SSD invece di HDD

**Per velocizzare:**
- Documenti più piccoli (divide documenti lunghi)
- Rimuovi immagini non necessarie prima di tradurre
- Usa formato DOCX invece di PDF (più veloce da processare)

### Qualità Traduzione

**Per migliorare la qualità:**
1. ✅ Assicurati che il testo source sia ben formattato
2. ✅ Evita abbreviazioni troppo specifiche
3. ✅ Rivedi sempre la traduzione (nessuna IA è perfetta)
4. ✅ Per terminologia ultra-specifica, considera post-editing manuale

**Termini legali:**
Alcuni termini legali potrebbero essere tradotti letteralmente. Per terminologia critica:
- Annota i termini chiave prima di tradurre
- Verifica manualmente dopo la traduzione
- Considera l'uso di glossari personalizzati (feature avanzata)

### Risoluzione Problemi

**Errore: "Modello non installato"**
→ Vai su "Gestisci Modelli" e scarica la coppia linguistica necessaria

**Anteprima vuota**
→ Il PDF potrebbe essere corrotto o scansionato. Verifica il file.

**Traduzione lenta**
→ Normale per documenti lunghi. Un documento di 50 pagine può richiedere 15 minuti.

**Caratteri strani nell'output**
→ Problema di encoding. Riprova con formato DOCX invece di PDF.

## 📊 Tempi Stimati

| Pagine | Tempo Stimato | RAM Usata |
|--------|---------------|-----------|
| 1-5    | 30-60 sec     | ~500 MB   |
| 10     | 2-3 min       | ~600 MB   |
| 25     | 5-7 min       | ~800 MB   |
| 50     | 10-15 min     | ~1 GB     |
| 100+   | 20-30 min     | ~1.5 GB   |

*Tempi indicativi su PC moderno (i5/8GB RAM). Possono variare.*

## 🔒 Privacy & Sicurezza

### Dati Locali

- ✅ **Nessun dato inviato online** durante la traduzione
- ✅ **Documenti rimangono sul tuo PC**
- ✅ **Nessun log remoto**
- ✅ **Nessuna telemetria**

### Log Locali

L'applicazione salva log in `logs/translator.log` per debug. Questi log:
- Rimangono sul tuo computer
- Non contengono il testo dei documenti
- Contengono solo info tecniche (nomi file, errori, timestamp)

## 📞 Supporto

Per assistenza:
1. Consulta questa guida
2. Leggi `README.md`
3. Verifica `logs/translator.log` per errori
4. Apri issue su GitHub con dettagli

---

**Buon lavoro! 📄✨**

