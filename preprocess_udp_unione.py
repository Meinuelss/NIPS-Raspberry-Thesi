import pandas as pd
import os

print("[*] Caricamento dati UDP...")
# Carichiamo saltando le righe sporche
df_udp = pd.read_csv('dataset_udp.csv', 
                    names=['time_epoch', 'ip_src', 'ip_dst', 'len', 'flags'], 
                    header=0, on_bad_lines='skip', low_memory=False)

df_udp = df_udp.dropna(subset=['ip_src', 'time_epoch'])
df_udp['second'] = df_udp['time_epoch'].astype(float).astype(int)
df_udp['is_syn'] = 0 

print("[*] Elaborazione statistiche UDP...")
grouped_udp = df_udp.groupby(['ip_src', 'second']).agg(
    pkt_count=('time_epoch', 'count'),
    syn_count=('is_syn', 'sum'),
    total_len=('len', 'sum')
).reset_index()

grouped_udp['avg_len'] = grouped_udp['total_len'] / grouped_udp['pkt_count']

# --- LA CORREZIONE ---
# Sappiamo che questo file è un attacco. 
# Etichettiamo come 1 tutto ciò che ha più di 5 pacchetti al secondo (escludendo il rumore di fondo minimo)
grouped_udp['Label'] = grouped_udp['pkt_count'].apply(lambda x: 1 if x > 5 else 0)

nuovi_dati = grouped_udp[['pkt_count', 'syn_count', 'avg_len', 'Label']]

print(f"[*] Recupero vecchi dati (nping + ab)...")
if os.path.exists('dataset_pulito.csv'):
    vecchi_dati = pd.read_csv('dataset_pulito.csv')
    dataset_finale = pd.concat([vecchi_dati, nuovi_dati], ignore_index=True)
    print(f"[+] Unione completata!")
else:
    dataset_finale = nuovi_dati

print("\n[*] STATISTICHE FINALI DEL SUPER-DATASET:")
counts = dataset_finale['Label'].value_counts()
print(counts)

dataset_finale.to_csv('dataset_ultra.csv', index=False)
print(f"\n[++] 'dataset_ultra.csv' salvato. Totale campioni: {len(dataset_finale)}")
