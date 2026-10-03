from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path("data/network_logs.csv")

def main():
    rng = np.random.default_rng(42)
    n = 1000
    normal = int(n * 0.9)
    attack = n - normal

    df = pd.DataFrame({
        "duration": rng.exponential(5, n),
        "src_bytes": rng.lognormal(8, 1, n),
        "dst_bytes": rng.lognormal(7, 1, n),
        "packets": rng.poisson(40, n) + 1,
        "failed_logins": rng.poisson(0.4, n),
        "port": rng.choice([22, 53, 80, 443, 8080], n),
        "protocol": rng.choice(["TCP", "UDP"], n)
    })

    idx = rng.choice(n, attack, replace=False)
    df.loc[idx, "src_bytes"] *= rng.uniform(10, 30, attack)
    df.loc[idx, "packets"] *= rng.integers(5, 15, attack)
    df.loc[idx, "failed_logins"] += rng.integers(5, 20, attack)
    df.loc[idx, "port"] = rng.choice([21, 23, 445, 3389], attack)

    OUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Created {OUT} with {len(df)} rows")

if __name__ == "__main__":
    main()
