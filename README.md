# 🦄 Analisi e Pulizia del Dataset delle Aziende Unicorn

Questo progetto ha lo scopo di analizzare e pulire un dataset contenente informazioni sulle **aziende unicorn** (startup valutate oltre 1 miliardo di dollari), per poi ottenere una serie di statistiche utili e insight significativi.

---

## 🎯 Obiettivo

Attraverso un insieme di funzionalità, il programma:
- Pulisce il dataset da valori nulli e duplicati
- Arricchisce i dati mancanti
- Analizza la distribuzione e l’evoluzione delle valutazioni aziendali
- Genera statistiche per industria e paese

---

## 📚 Dataset atteso

Il programma parte da un file CSV chiamato `unicorns.csv`, che deve contenere almeno le seguenti colonne:

- `company`
- `industry`
- `city`
- `country`
- `valuation`
- `select_investors`
- `date_joined`

---

## 🧩 Funzionalità implementate

### 1. `carica_dati(percorso)`
Carica i dati da un file CSV e ne crea una copia indipendente.

### 2. `mostra_valori_nulli(df)`
Stampa il numero di valori nulli per ciascuna colonna.

### 3. `completa_city_con_country(df)`
Sostituisce i valori mancanti nella colonna `city` con quelli della colonna `country`.

### 4. `rimuovi_righe_senza_investitori(df)`
Rimuove le righe che non indicano investitori (`select_investors` nulli).

### 5. `rimuovi_duplicati(df)`
Rimuove eventuali righe duplicate nel dataset.

### 6. `pulisci_dati(percorso)`
Effettua l’intera pipeline di pulizia:
- Caricamento
- Visualizzazione dei nulli
- Completamento città
- Rimozione righe senza investitori
- Rimozione duplicati
- Conversione della colonna `valuation` in numerica
- Eliminazione righe con `valuation` mancante

### 7. `top_aziende(df, n=10)`
Restituisce le `n` aziende con la **valuation più alta**.

### 8. `down_aziende(df, n=10)`
Restituisce le `n` aziende con la **valuation più bassa**.

### 9. `aziende_top_per_paese(df)`
Restituisce la **azienda con la valutazione più alta per ogni paese**.

### 10. `industria_piu_frequente(df)`
Restituisce un conteggio delle aziende per industria, ordinato in ordine decrescente.

### 11. `andamento_annuale_per_industria(df)`
Restituisce un dataframe che mostra l’evoluzione annuale delle valutazioni aziendali per ogni industria e azienda.

---

## 🧪 Esecuzione del programma

```bash
python nome_script.py

 
