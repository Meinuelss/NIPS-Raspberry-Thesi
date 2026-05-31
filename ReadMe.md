#  Edge-NIPS: Network Intrusion Prevention System su Raspberry Pi

**Sviluppo di un sistema intelligente di prevenzione delle intrusioni su 
architettura Edge.** *Progetto di Tesi - Dipartimento di Informatica, 
Università degli Studi di Torino (A.A. 2025-2026).*

---

##  Panoramica del Progetto
Questo repository contiene il codice sorgente, i modelli pre-addestrati e 
la documentazione di un **Network Intrusion Prevention System (NIPS) 
Lightweight**. 

Il sistema è progettato per operare su dispositivi con risorse limitate 
(come un Raspberry Pi) e utilizza un modello di Machine Learning (Random 
Forest) per analizzare il traffico di rete ai livelli L3/L4 in tempo 
reale. È in grado di identificare e bloccare istantaneamente minacce 
automatizzate come **attacchi DoS volumetrici e HTTPS Flood**, isolando 
gli agenti malevoli prima che possano saturare le risorse di sistema o 
causare il crash dei servizi esposti.

## Risultati Principali
Rispetto a soluzioni pesanti basate su Deep Learning (es. Graph Neural 
Networks, che impiegano oltre 2 secondi per l'inferenza), l'approccio 
adottato in questo progetto ha garantito:
- **Accuratezza Elevata:** `99.60%` in fase di validazione 
(Cross-Validation a 10 Fold con Random Forest).
- **Latenza di Rilevamento:** Tempi di inferenza nell'ordine dei **pochi 
millisecondi**, permettendo un drop tempestivo e dinamico dei pacchetti 
ostili.

## Struttura del Repository
Il progetto è modulare e organizzato nelle seguenti directory:

* `src/` — Contiene gli script Python principali per l'esecuzione e 
l'addestramento:
  * `ai_firewall.py`: Il motore NIPS principale per il monitoraggio e il 
drop dei pacchetti in tempo reale.
  * `crea_dataset.py`: Script per la cattura e l'estrazione delle feature 
dal traffico di rete.
  * `addestra_agente_ia.py`: Script per l'addestramento del modello Random 
Forest e l'esportazione del modello.
  * `valutazione_modelli.py`: Script per l'esecuzione della 
Cross-Validation e il confronto prestazionale tra algoritmi (RF, DT, LR, 
KNN).
* `modelli/` — Modelli di Machine Learning già addestrati e salvati in 
formato `.sav`, pronti per l'inferenza immediata.
* `dataset/` — Dati di rete in formato CSV utilizzati per le fasi di 
training e testing.
* `certificate/` — Certificati per il deployment locale dell'ambiente di 
test.
* `Paper/` — Articoli scientifici di riferimento analizzati per lo stato 
dell'arte.

 ## Prerequisiti e Installazione
Per eseguire il progetto, è richiesto un ambiente Linux (es. Raspberry Pi 
OS) e Python 3.

1. **Clona il repository:**
   ```bash
   git clone https://github.com/Meinuelss/NIPS-Raspberry-Thesi.git
   cd NIPS-Raspberry-Thesi
   ```

2. **Installa le dipendenze richieste:**
   ```bash
   pip install -r requirements.txt
   ```

## Utilizzo

### Avvio del NIPS in tempo reale
Per avviare il firewall intelligente, esegui lo script principale. 
> **Nota:** È strettamente necessario eseguire lo script con privilegi di 
`root` (`sudo`), in quanto il sistema richiede i permessi di 
amministrazione per l'intercettazione dei pacchetti tramite la libreria 
`scapy` e per l'applicazione dinamica delle regole di blocco sul firewall 
(iptables).

```bash
sudo python3 src/ai_firewall.py modelli/random_forest.sav
```

### Valutazione dei Modelli
Se desideri ricalcolare le metriche di accuratezza e deviazione standard 
sui vari algoritmi utilizzando il dataset fornito:

```bash
python3 src/valutazione_modelli.py
```

## Nota di Sicurezza sui Certificati
All'interno della cartella `certificate/` sono presenti file chiave (es. 
`key.pem`). Si precisa formalmente che si tratta di **certificati 
autofirmati e fittizi**, generati esclusivamente in ambito locale per 
testare lo stress computazionale dell'handshake TLS sul Raspberry Pi 
durante l'attività di tirocinio. Questi certificati non hanno alcuna 
validità esterna, non appartengono a sistemi di produzione reali e la loro 
esposizione non comporta alcun rischio di sicurezza.

---
## Autore
* **Manuel Serranò** (Matricola: 1118868)
* **Relatore:** Prof. Marco Botta
