import pandas as pd
from scapy.all import rdpcap, TCP, UDP, IP
import numpy as np

def extract_features_from_pcap(pcap_file, label, window_size=1.0):
    """
    Legge un file PCAP, divide i pacchetti in finestre temporali (es. 1 secondo)
    ed estrae le feature per il NIPS.
    label: 0 per traffico Normale, 1 per traffico Malevolo
    """
    print(f"Leggendo {pcap_file}...")
    packets = rdpcap(pcap_file)
    
    if len(packets) == 0:
        return pd.DataFrame()

    # Prendi il timestamp del primo pacchetto come tempo zero
    start_time = float(packets[0].time)
    
    windows = {} # Dizionario per raggruppare i pacchetti per finestra temporale

    for pkt in packets:
        if IP in pkt:
            # Calcola in quale "finestra" di tempo cade il pacchetto
            current_time = float(pkt.time)
            window_index = int((current_time - start_time) // window_size)
            
            if window_index not in windows:
                windows[window_index] = {
                    'packet_count': 0,
                    'syn_count': 0,
                    'total_payload_size': 0
                }
            
            # 1. Aggiorna il conteggio dei pacchetti
            windows[window_index]['packet_count'] += 1
            
            # 2. Aggiorna il conteggio dei flag SYN (solo se è TCP)
            if TCP in pkt:
                # Il flag SYN in Scapy corrisponde al bit 2 (valore 2) o 'S'
                if pkt[TCP].flags & 0x02:
                    windows[window_index]['syn_count'] += 1
                    
            # 3. Somma la dimensione del payload per poi fare la media
            # Lunghezza totale IP - lunghezza header IP - lunghezza header TCP/UDP
            payload_len = len(pkt[IP].payload)
            if TCP in pkt:
                payload_len -= len(pkt[TCP])
            elif UDP in pkt:
                payload_len -= len(pkt[UDP])
                
            windows[window_index]['total_payload_size'] += max(0, payload_len)

    # Ora trasformiamo il dizionario in una lista di righe per il CSV
    dataset_rows = []
    for w_idx, data in windows.items():
        avg_payload = data['total_payload_size'] / data['packet_count'] if data['packet_count'] > 0 else 0
        
        dataset_rows.append({
            'packet_count': data['packet_count'],
            'syn_count': data['syn_count'],
            'avg_payload_size': round(avg_payload, 2),
            'label': label
        })
        
    return pd.DataFrame(dataset_rows)

if __name__ == "__main__":
    # 1. Estrai le feature dal traffico NORMALE (Label = 0)
    # Sostituisci con il nome del tuo file pcap di traffico pulito
    df_normal = extract_features_from_pcap("traffico_normale.pcap", label=0)
    
    # 2. Estrai le feature dal traffico di ATTACCO (Label = 1)
    # Sostituisci con il nome del tuo file pcap di traffico malevolo (UDP Flood, SYN Flood, ecc.)
    df_attack = extract_features_from_pcap("traffico_attacco.pcap", label=1)
    
    # 3. Unisci i due dataframe
    df_finale = pd.concat([df_normal, df_attack], ignore_index=True)
    
    df_finale = df_finale.sample(frac=1).reset_index(drop=True)
    
    df_finale.to_csv("dataset/dataset.csv", index=False)
    
    print("\nDataset creato con successo! File salvato come 'dataset_nips_finale.csv'.")
    print(df_finale.head())
