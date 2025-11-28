import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

print("="*60)
print(" Training CYBER-DEF25 Medium Malware Classifier ")
print("="*60)

np.random.seed(101)
n_samples = 12000   

data = {
    'packet_size':        np.random.randint(60, 1600, n_samples),
    'duration':           np.random.uniform(0.05, 250, n_samples),
    'src_bytes':          np.random.randint(0, 20000, n_samples),
    'dst_bytes':          np.random.randint(0, 20000, n_samples),
    'wrong_fragment':     np.random.randint(0, 4, n_samples),
    'urgent':             np.random.randint(0, 3, n_samples),
    'num_failed_logins':  np.random.randint(0, 6, n_samples),
    'num_access_files':   np.random.randint(0, 12, n_samples),
    'num_compromised':    np.random.randint(0, 8, n_samples),
    'srv_count':          np.random.randint(0, 600, n_samples)
}

df = pd.DataFrame(data)

df['malicious'] = (
    (df['wrong_fragment'] >= 3) |
    (df['num_failed_logins'] >= 4) |
    (df['num_compromised'] >= 3) |
    ((df['duration'] > 200) & (df['src_bytes'] > 15000))
).astype(int)

print(f"\n Dataset created: {len(df)} samples")
print(" Malware ratio:", df['malicious'].mean())

X = df.drop(columns=['malicious'])
y = df['malicious']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

print("\n Splitting complete!")
print(f" Train size: {len(X_train)}")
print(f" Test size:  {len(X_test)}")

print("\n Training RandomForest model...")
model = RandomForestClassifier(
    n_estimators=130,
    max_depth=18,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print(" Training complete!")

joblib.dump(model, 'model.pkl')
print("\n Saved model as model.pkl")

print("="*60)
print(" MODEL TRAINING FINISHED ")
print("="*60)
