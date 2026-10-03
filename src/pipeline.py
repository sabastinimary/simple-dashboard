from pathlib import Path
import yaml
import mlflow
import pandas as pd
from src.data.validate import validate
from src.features.engineering import transform
from src.model import train, score, level

def main():
    cfg = yaml.safe_load(Path("config.yaml").read_text())
    data_path = cfg["data"]["path"]
    model_path = cfg["model"]["path"]

    validate(data_path)
    df = pd.read_csv(data_path)
    X = transform(df)

    mlflow.set_experiment(cfg["mlflow"]["experiment"])

    with mlflow.start_run():
        model = train(
            X,
            model_path,
            cfg["model"]["contamination"]
        )
        risks = score(model, X)

        mlflow.log_param("algorithm", "IsolationForest")
        mlflow.log_param("rows", len(X))
        mlflow.log_param("contamination", cfg["model"]["contamination"])
        mlflow.log_metric("mean_risk", float(risks.mean()))
        mlflow.log_metric("high_risk_count", int((risks >= 0.70).sum()))
        mlflow.log_artifact(model_path)

        result = pd.DataFrame({
            "risk_score": risks,
            "risk_level": [level(r) for r in risks]
        })
        result.to_csv("data/predictions.csv", index=False)

    print("Pipeline completed")
    print(result["risk_level"].value_counts())

if __name__ == "__main__":
    main()
