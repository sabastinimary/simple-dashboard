import pandas as pd
from src.features.engineering import transform
from src.model import level

def test_features():
    df = pd.DataFrame([{
        "duration": 1, "src_bytes": 100,
        "dst_bytes": 50, "packets": 10,
        "failed_logins": 0, "port": 80,
        "protocol": "TCP"
    }])
    assert transform(df).shape == (1, 9)

def test_levels():
    assert level(0.1) == "Low"
    assert level(0.5) == "Medium"
    assert level(0.9) == "High"
