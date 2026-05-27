import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
import joblib

print("[*] Caricamento del dataset pulito...")
df = pd.read_csv('../dataset/dataset.csv')

# Separiamo le statistiche (X) dall'etichetta (y)
X = df[['pkt_count', 'syn_count', 'avg_len']]
y = df['Label']

print("[*] Divisione dei dati (80% studio, 20% esame)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 1. RANDOM FOREST ---
print("[*] Addestramento del Random Forest...")
modello_rf = RandomForestClassifier(n_estimators=100, random_state=42)
modello_rf.fit(X_train, y_train)
print("[*] Salvataggio di random_forest.sav...")
joblib.dump(modello_rf, '../modelli/random_forest.sav')


print("\n[*] Inizio addestramento ed esportazione degli altri 3 modelli...")

# --- 2. DECISION TREE ---
print("- Addestramento Decision Tree...")
modello_dt = DecisionTreeClassifier(random_state=42)
modello_dt.fit(X_train, y_train)
joblib.dump(modello_dt, '../modelli/decision_tree.sav')

# --- 3. K-NEAREST NEIGHBORS (KNN) ---
print("- Addestramento K-Nearest Neighbors (KNN)...")
modello_knn = KNeighborsClassifier(n_neighbors=5)
modello_knn.fit(X_train, y_train)
joblib.dump(modello_knn, '../modelli/knn.sav')

# --- 4. LOGISTIC REGRESSION ---
print("- Addestramento Logistic Regression...")
modello_lr = LogisticRegression(max_iter=1000, random_state=42)
modello_lr.fit(X_train, y_train)
joblib.dump(modello_lr, '../modelli/logistic_regression.sav')

print("\n[+] Successo! Tutti i file .sav sono stati generati con Joblib e sono pronti per i test sul campo.")
