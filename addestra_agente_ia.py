import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
import pickle
import joblib

print("[*] Caricamento del dataset pulito...")
df = pd.read_csv('dataset.csv')

# Il nostro CSV è già perfetto: separiamo le statistiche (X) dall'etichetta (y)
X = df[['pkt_count', 'syn_count', 'avg_len']]
y = df['Label']

print("[*] Divisione dei dati (80% studio, 20% esame)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("[*] Addestramento del Super-Cervello NIPS...")
# Creiamo una "foresta" di 100 alberi decisionali
modello = RandomForestClassifier(n_estimators=100, random_state=42)
modello.fit(X_train, y_train)

print("[*] Svolgimento dell'esame finale (test di accuratezza)...")
previsioni = modello.predict(X_test)
accuratezza = accuracy_score(y_test, previsioni)
print(f"\n[+] ACCURATEZZA DEL MODELLO: {accuratezza * 100:.2f}%\n")

print("[*] Salvataggio del file .sav (sovrascrittura)...")
with open('random_forest.sav', 'wb') as f:
    pickle.dump(modello, f)
print("[+] Fatto! Il nuovo 'random_forest.sav' è pronto per la battaglia.")

print("\n[*] Inizio addestramento ed esportazione dei 4 modelli per il NIPS...")

# 2. Decision Tree (L'albero singolo)
print("- Addestramento Decision Tree...")
modello_dt = DecisionTreeClassifier(random_state=42)
modello_dt.fit(X, y)
joblib.dump(modello_dt, 'decision_tree.sav')

# 3. K-Nearest Neighbors (L'algoritmo basato sulle distanze)
print("- Addestramento K-Nearest Neighbors (KNN)...")
modello_knn = KNeighborsClassifier(n_neighbors=5)
modello_knn.fit(X, y)
joblib.dump(modello_knn, 'knn.sav')

# 4. Logistic Regression (L'approccio probabilistico)
print("- Addestramento Logistic Regression...")
# Nota: max_iter=1000 serve per evitare avvisi se il modello impiega tanto a convergere
modello_lr = LogisticRegression(max_iter=1000, random_state=42)
modello_lr.fit(X, y)
joblib.dump(modello_lr, 'logistic_regression.sav')

print("\n[+] Successo! Tutti i file .sav sono stati generati e sono pronti per i test sul campo.")

