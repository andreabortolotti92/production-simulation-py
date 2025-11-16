Project Work – Simulazione della produzione in un’azienda metalmeccanica mediante Python

OBIETTIVI
Gli obiettivi richiesti dal project work erano i seguenti: sviluppare competenze di programmazione applicata specifiche per la simulazione di sistemi, applicare principi di gestione per configurare un processo produttivo realistico.
Nel dettaglio veniva richiesto di:
-	Sviluppare un codice Python che:
    o	Presenti una funzione per generare casualmente le quantità da produrre per ogni prodotto (minimo 3 prodotti differenti);
    o	Presenti una funzione per generare casualmente i parametri da configurare, come tempi di produzione per prodotto, capacità massima di produzione giornaliera per prodotto e complessiva;
    o	Restituisca in output il tempo di produzione complessivo dell’intero lotto di produzione;
-	Il tutto andava corredato poi di:
    o	Descrizione del contesto in cui opera l’azienda e il suo processo produttivo;
    o	Il codice Python sviluppato per la simulazione;
    o	Un resoconto che descrivesse il processo seguito per lo sviluppo del codice

```
STRUTTURA DEL PROGETTO
│
├── constants.py    # Costanti di configurazione (seed, prodotti, range)
├── params.py       # Generazione casuale dei parametri (quantità, tempi, capacità)
├── schedule.py     # Simulazione della produzione giorno per giorno
├── report.py       # Riepilogo dei risultati (analisi e tabelle)
├── UI.py           # Funzioni per User Interface
├── main.py         # File principale per l’esecuzione del programma
└── README.md       # Documentazione del progetto
```

LOGICA DI SIMULAZIONE
Il programma simula giorno per giorno la produzione dei lotti, rispettando:
- il limite di capacità per prodotto
- la capacità complessiva giornaliera
- la produzione a pezzi interi


CONVENZIONI
Nel presente progetto è stata utilizzata la lingua inglese per le parole chiave (nomi variabili/costanti/funzioni), mentre i commenti sono stati scritti in lingua italiana.
Si è scelto, per semplicità, di gestire ciclicamente la produzione dei prodotti in ordine alfabetico.

REQUISITI TECNICI
Librerie:
- numpy
- pandas

ESECUZIONE DEL PROGRAMMA
python main.py

DESCRIZIONE DEL FUNZIONAMENTO
Durante l’esecuzione, il programma chiederà se si desidera impostare un seed personalizzato. Non inserendo nulla (o inserendo un valore non valido) verrà utilizzato il seed predefinito (3753092).
L’output include:
- i parametri casuali generati (quantità, tempi, capacità);
- il piano giornaliero di produzione (una volta implementato);
- i riepiloghi statistici dei risultati.

