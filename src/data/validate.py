from pathlib import Path
import pandas as pd

REQUIRED = [
    "duration", "src_bytes", "dst_bytes", "packets",
    "failed_logins", "port", "protocol"
]

def validate(path="data/network_logs.csv"):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    df = pd.read_csv(p)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    if df.empty or df.isna().any().any():
        raise ValueError("Data is empty or contains missing values")

    print(f"Validation successful: {len(df)} rows")
    return True

if __name__ == "__main__":
    validate()
