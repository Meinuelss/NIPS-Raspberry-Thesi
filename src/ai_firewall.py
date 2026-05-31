#!/usr/bin/env python3
from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import joblib
import time
import os
import sys     # NUOVO IMPORT: Per leggere i comandi dal terminale
from collections import defaultdict

# --- INIZIO GESTIONE DINAMICA DEL MODELLO ---
# Controlliamo se l'utente ha scritto il nome del file .sav
if len(sys.argv) != 2:
    print("[-] Errore: Devi specificare quale modello usare!")
    print("[-] Esempio: sudo python3 src/ai_firewall.py modelli/random_forest.sav")
    sys.exit(1)

MODELLO_IA = sys.argv[1]
# --- FINE GESTIONE DINAMICA ---

# Configurazione
INTERFACCIA = "wlan0"
TEMPO_BAN = 30 # Secondi di quarantena per l'IP attaccante prima dello sblocco

print("[*] Inizializzazione dell'Agente NIPS...")
print(f"[*] Modello selezionato: {MODELLO_IA}")

try:
    # Caricamento diretto con joblib
    modello = joblib.load(MODELLO_IA)
    print("[+] Cervello IA caricato con successo.")
except FileNotFoundError:
    print(f"[-] Errore: Il file '{MODELLO_IA}' non esiste in questa cartella.")
    sys.exit(1)
except Exception as e:
    print(f"[-] Errore durante il caricamento: {e}")
    sys.exit(1)

ultimo_secondo = int(time.time())
traffico = defaultdict(lambda: {'pkt_count': 0, 'syn_count': 0, 'total_len': 0})

# Dizionario per ricordare QUANDO sbloccare l'IP
# Formato: { '192.168.1.187': timestamp_di_sblocco }
ip_bloccati = {}

def analizza_pacchetto(pkt):
    global ultimo_secondo, traffico, ip_bloccati
    secondo_attuale = int(time.time())

    # === CONTROLLO SBLOCCHI (QUARANTENA) ===
    for ip_bannato in list(ip_bloccati.keys()):
        if secondo_attuale > ip_bloccati[ip_bannato]:
            print(f"\n[*] Quarantena finita. Rimuovo il blocco per {ip_bannato}...")
            os.system(f"iptables -D INPUT -s {ip_bannato} -j DROP")
            del ip_bloccati[ip_bannato]
            print("[+] Accesso ripristinato al sito web per quell'IP!")

    # === ANALISI DEL TRAFFICO ===
    if secondo_attuale > ultimo_secondo:
        for ip_src, stats in traffico.items():
            if ip_src in ip_bloccati:
                continue # Se è già in castigo, ignoriamo le sue statistiche

            pkt_count = stats['pkt_count']
            syn_count = stats['syn_count']
            avg_len = stats['total_len'] / pkt_count if pkt_count > 0 else 0

            df = pd.DataFrame([{'pkt_count': pkt_count, 'syn_count': syn_count, 'avg_len': avg_len}])
            previsione = modello.predict(df)[0]

            # --- RIGA DI DEBUG ---
            print(f"[DEBUG] IA valuta {ip_src} -> Pkt: {pkt_count}, SYN: {syn_count}. Risultato: {previsione}")

            if previsione == 1:
                print(f"\n[!!!] MINACCIA RILEVATA: Attacco da {ip_src} (Pkt/s: {pkt_count}, SYN/s: {syn_count})")
                print(f"[*] Metto in quarantena {ip_src} per {TEMPO_BAN} secondi...")

                # Inseriamo la regola di blocco
                os.system(f"iptables -A INPUT -s {ip_src} -j DROP")

                # Registriamo l'orario in cui dovrà essere sbloccato
                ip_bloccati[ip_src] = secondo_attuale + TEMPO_BAN
                print("[+] IP Neutralizzato temporaneamente!\n")

        traffico.clear()
        ultimo_secondo = secondo_attuale

    # === LETTURA DEI PACCHETTI IN DIRETTA ===
    if IP in pkt and (TCP in pkt or UDP in pkt):
        ip_src = pkt[IP].src

        if ip_src == "127.0.0.1" or ip_src == "192.168.1.201" or ip_src.startswith("100."):
            return

        traffico[ip_src]['pkt_count'] += 1
        traffico[ip_src]['total_len'] += len(pkt)

        if TCP in pkt:
            if pkt[TCP].flags & 0x02:
                traffico[ip_src]['syn_count'] += 1

print(f"[*] Radar attivo sull'interfaccia {INTERFACCIA}...")
print("[*] In attesa di attacchi. Premi Ctrl+C per fermare.")
sniff(iface=INTERFACCIA, prn=analizza_pacchetto, store=False)
