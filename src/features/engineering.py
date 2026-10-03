import pandas as pd

NUMERIC = [
    "duration", "src_bytes", "dst_bytes",
    "packets", "failed_logins", "port"
]

def transform(df):
    x = df.copy()
    x["bytes_ratio"] = (x["src_bytes"] + 1) / (x["dst_bytes"] + 1)
    x["bytes_per_packet"] = (
        x["src_bytes"] + x["dst_bytes"]
    ) / (x["packets"] + 1)
    x["protocol_tcp"] = (x["protocol"] == "TCP").astype(int)

    features = NUMERIC + [
        "bytes_ratio", "bytes_per_packet", "protocol_tcp"
    ]
    return x[features]
