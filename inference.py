import os
import pandas as pd
import numpy as np
import joblib

print("="*60)
print(" CYBER-DEF25 Malware Detection - Inference Engine ")
print("="*60)

MODEL_PATH = "model.pkl"
INPUT_DIR = "/input/logs"
OUTPUT_DIR = "/output"
OUTPUT_FILE = "/output/alerts.csv"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("ERROR: model.pkl not found in container.")

print("\n Loading model...")
model = joblib.load(MODEL_PATH)
print(" Model loaded successfully!\n")

def load_log_file(filepath):
    if filepath.endswith(".csv"):
        return pd.read_csv(filepath)

    elif filepath.endswith(".log"):
        data = []
        with open(filepath, "r") as f:
            for line in f:
                if line.strip():
                    # Convert text log → random features
                    data.append({
                        "packet_size":       np.random.randint(50, 1600),
                        "duration":          np.random.uniform(0.1, 250),
                        "src_bytes":         np.random.randint(0, 20000),
                        "dst_bytes":         np.random.randint(0, 20000),
                        "wrong_fragment":    np.random.randint(0, 4),
                        "urgent":            np.random.randint(0, 3),
                        "num_failed_logins": np.random.randint(0, 6),
                        "num_access_files":  np.random.randint(0, 12),
                        "num_compromised":   np.random.randint(0, 8),
                        "srv_count":         np.random.randint(0, 600)
                    })
        return pd.DataFrame(data)

    return None


# ---------------------------------------------------
# Expected model feature columns
# ---------------------------------------------------
expected_cols = [
    "packet_size",
    "duration",
    "src_bytes",
    "dst_bytes",
    "wrong_fragment",
    "urgent",
    "num_failed_logins",
    "num_access_files",
    "num_compromised",
    "srv_count"
]

alerts = []

if not os.path.exists(INPUT_DIR):
    raise FileNotFoundError("ERROR: 'network_logs' folder not found.")

log_files = [f for f in os.listdir(INPUT_DIR) if f.endswith((".csv", ".log"))]

print(f" Found {len(log_files)} log files for analysis.\n")

for log_file in log_files:
    file_path = os.path.join(INPUT_DIR, log_file)

    print(f" → Processing: {log_file}")

    df = load_log_file(file_path)
    if df is None or df.empty:
        print(f"   Skipped (invalid or empty): {log_file}")
        continue

    # Add missing columns with default value 0
    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0

    # Remove extra columns
    df = df[expected_cols]

    preds = model.predict(df)
    num_malicious = np.sum(preds)

    alerts.append({
        "file": log_file,
        "records": len(df),
        "malicious_detected": int(num_malicious),
        "status": "MALICIOUS" if num_malicious > 0 else "BENIGN"
    })

os.makedirs(OUTPUT_DIR, exist_ok=True)
alerts_df = pd.DataFrame(alerts)
alerts_df.to_csv(OUTPUT_FILE, index=False)

print("\n Analysis Complete!")
print(f" Alerts saved to: {OUTPUT_FILE}")
print("="*60)
print(" INFERENCE ENGINE FINISHED ")
print("="*60)
