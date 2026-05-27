import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

print("[*] Caricamento del Dataset (dataset.csv)...")
df = pd.read_csv("../dataset/dataset.csv")

# Utilizziamo esattamente le colonne estratte dal CSV
X = df[['pkt_count', 'syn_count', 'avg_len']] 
y = df['Label']

# Impostiamo la Cross-Validation a 10 Folds
print("[*] Preparazione K-Fold Cross-Validation (10 splits)...")
kf = KFold(n_splits=10, shuffle=True, random_state=42)

# I modelli che andiamo a mettere a confronto
modelli = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
    "Logistic Regression": LogisticRegression(max_iter=1000)
}

print("\n" + "="*45)
print("   RISULTATI CROSS-VALIDATION (10-Fold)")
print("="*45)

# Addestriamo e testiamo ogni modello per 10 volte
for nome, modello in modelli.items():
    risultati = cross_val_score(modello, X, y, cv=kf, scoring='accuracy')
    
    media = risultati.mean() * 100
    deviazione = risultati.std() * 100
    
    print(f"[+] {nome}:")
    print(f"    -> Accuratezza Media : {media:.2f}%")
    print(f"    -> Deviazione Std    : ± {deviazione:.2f}%")
    print("-" * 45)

print("\n[*] Valutazione completata. Dati pronti per la Tesi!")
