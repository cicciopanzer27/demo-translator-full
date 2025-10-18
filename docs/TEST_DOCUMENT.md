# 📄 Come Testare l'Applicazione

## Creare un Documento di Test

### Metodo 1: Documento Word di Test

1. Apri Microsoft Word o LibreOffice Writer
2. Scrivi un testo di esempio in inglese:

```
SALES CONTRACT

This Sales Contract ("Contract") is entered into as of January 1, 2024, by and between:

Seller: ABC Company Ltd.
Address: 123 Main Street, London, UK

Buyer: XYZ Corporation
Address: 456 Oak Avenue, New York, USA

1. SUBJECT OF THE CONTRACT

The Seller agrees to sell and the Buyer agrees to purchase the following goods:
- Product: Industrial Equipment Model X500
- Quantity: 50 units
- Unit Price: $10,000 USD
- Total Value: $500,000 USD

2. PAYMENT TERMS

The Buyer shall pay the total amount in three installments:
- First installment: 30% upon signing this Contract
- Second installment: 40% upon delivery
- Third installment: 30% within 30 days of delivery

3. DELIVERY

Delivery shall be made within 60 days from the date of this Contract.
The goods shall be delivered to the Buyer's warehouse at the address specified above.

4. WARRANTIES

The Seller warrants that the goods are free from defects in material and workmanship
for a period of 12 months from the date of delivery.

5. FORCE MAJEURE

Neither party shall be liable for any failure to perform its obligations under this
Contract if such failure is caused by force majeure events including but not limited
to natural disasters, war, strikes, or government actions.

6. APPLICABLE LAW

This Contract shall be governed by and construed in accordance with the laws of England.

7. DISPUTE RESOLUTION

Any disputes arising from this Contract shall be resolved through arbitration in London.

IN WITNESS WHEREOF, the parties have executed this Contract as of the date first written above.

________________________          ________________________
ABC Company Ltd.                  XYZ Corporation
(Seller)                          (Buyer)
```

3. Salva come `test_contract.docx`

### Metodo 2: Converti in PDF

1. In Word/LibreOffice: File → Salva come → PDF
2. Salva come `test_contract.pdf`

### Metodo 3: Documento Multi-pagina

Per testare documenti lunghi, copia il testo sopra 10-20 volte cambiando i dettagli.

## 🧪 Procedura di Test

### Test Base

1. **Avvia applicazione**: `python src\main.py`
2. **Seleziona lingue**: en → it
3. **Carica documento**: `test_contract.docx`
4. **Output**: Desktop
5. **Traduci**: Verifica che completi senza errori
6. **Risultato atteso**: `test_contract_translated_it.docx` sul Desktop

### Test Avanzati

**Test 1: PDF → PDF**
- Input: `test_contract.pdf` (en)
- Output: `test_contract_translated_it.pdf` (it)
- Verifica: Apri il PDF, controlla formattazione

**Test 2: DOCX → DOCX**
- Input: `test_contract.docx` (en)
- Output: `test_contract_translated_es.docx` (es)
- Verifica: Apri in Word, controlla paragrafi

**Test 3: Documento Lungo (10+ pagine)**
- Crea documento con 15+ pagine
- Verifica: Barra progresso si aggiorna correttamente
- Tempo atteso: 3-5 minuti

**Test 4: Lingue Multiple**
Prova tutte le combinazioni:
- en → it ✓
- it → en ✓
- en → es ✓
- en → fr ✓
- en → de ✓

**Test 5: Caratteri Speciali**
Aggiungi al documento:
- Simboli: €, £, ¥, ©, ®, ™
- Accenti: à, è, é, ü, ñ
- Numeri: 1,000.00 | €15.000,00
- Date: 01/01/2024 | 2024-01-01

**Test 6: Errori**
- Seleziona lingua source = lingua target → Pulsante disabilitato ✓
- Non selezionare file → Pulsante disabilitato ✓
- Carica file corrotto → Errore gestito ✓
- Modello non installato → Warning chiaro ✓

## ✅ Checklist Validazione

- [ ] Installazione completata senza errori
- [ ] Almeno un modello linguistico installato
- [ ] GUI si apre correttamente
- [ ] Preview documento funziona
- [ ] Traduzione DOCX → DOCX completa
- [ ] Traduzione PDF → PDF completa
- [ ] Progress bar si aggiorna
- [ ] File output creato correttamente
- [ ] File output leggibile e formattato
- [ ] Traduzione ha senso (controllo manuale)
- [ ] Log creati in `logs/translator.log`
- [ ] Nessun crash durante traduzione
- [ ] Gestione errori funziona

## 📊 Risultati Attesi

### Qualità Traduzione

La traduzione con Argos Translate è **buona ma non perfetta**:

✅ **Buona per:**
- Testo generale
- Contratti standard
- Corrispondenza business
- Documenti tecnici base

⚠️ **Richiede revisione per:**
- Terminologia ultra-specifica
- Giochi di parole / idiomi
- Riferimenti culturali
- Testi creativi

### Performance

| Test | Tempo Atteso | Note |
|------|--------------|------|
| 1 pagina | 10-20 sec | Prima traduzione più lenta |
| 5 pagine | 1-2 min | Dipende dalla densità testo |
| 10 pagine | 2-4 min | Progress bar dovrebbe aggiornarsi |
| 50 pagine | 10-15 min | Test di stress |

## 🐛 Report Bug

Se trovi problemi, annota:

1. **Versione Python**: `python --version`
2. **Sistema Operativo**: Windows 10/11, Linux, macOS
3. **Tipo documento**: PDF o DOCX
4. **Dimensione**: Numero pagine / MB
5. **Lingue**: Coppia source → target
6. **Errore esatto**: Screenshot o testo da `logs/translator.log`
7. **Come riprodurre**: Passi esatti per causare l'errore

## 💡 Suggerimenti

- **Prima traduzione lenta**: Il primo avvio carica i modelli in RAM (30-60 sec)
- **Traduzioni successive**: Più veloci perché modelli già in memoria
- **RAM insufficiente**: Chiudi altri programmi durante traduzioni lunghe
- **Qualità variabile**: Normale - gli engine NMT open source hanno limiti

---

**Buon Testing! 🧪**

