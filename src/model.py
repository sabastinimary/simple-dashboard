from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

def train(X, path="models/model.joblib", contamination=0.10):
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=200
    )
    model.fit(X)
    Path(path).parent.mkdir(exist_ok=True)
    joblib.dump(model, path)
    return model

def load(path="models/model.joblib"):
    return joblib.load(path)

def score(model, X):
    raw = -model.decision_function(X)
    lo, hi = raw.min(), raw.max()
    risk = (raw - lo) / (hi - lo + 1e-9)
    return np.clip(risk, 0, 1)

def level(risk):
    if risk < 0.40:
        return "Low"
    if risk < 0.70:
        return "Medium"
    return "High"
