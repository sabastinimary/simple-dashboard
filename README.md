# AI Network Anomaly Detection

Simple MLOps project using **Python + Isolation Forest + MLflow + Airflow + Git**.

## Flow

Network Logs -> Validation -> Feature Engineering -> Isolation Forest -> Risk Score -> MLflow  
Airflow runs the pipeline automatically. FastAPI exposes predictions.

## 1. Requirements

- Python 3.11+
- Git
- Airflow
- MLflow

## 2. Setup - Windows PowerShell

```powershell
cd network-anomaly-detection
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Generate data and train

```powershell
python -m src.data.generate
python -m src.pipeline
```

This creates:
- `data/network_logs.csv`
- `models/model.joblib`
- MLflow experiment data in `mlruns/`

## 4. Start MLflow

Open another terminal:

```powershell
cd network-anomaly-detection
.\.venv\Scripts\Activate.ps1
mlflow ui --host 127.0.0.1 --port 5000
```

Open http://127.0.0.1:5000

## 5. Start FastAPI

```powershell
uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
```

Open http://127.0.0.1:8000/docs

Example request:

```json
{
  "duration": 20,
  "src_bytes": 90000,
  "dst_bytes": 300,
  "packets": 500,
  "failed_logins": 8,
  "port": 23,
  "protocol": "TCP"
}
```

## 6. Airflow

Airflow is easiest in WSL/Linux.

Install:

```bash
pip install -r requirements.txt
export AIRFLOW_HOME=$PWD/airflow
airflow db migrate
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

Set the DAG folder:

```bash
export AIRFLOW__CORE__DAGS_FOLDER=$PWD/dags
```

Start Airflow in two terminals:

```bash
airflow scheduler
```

```bash
airflow api-server --port 8080
```

Open http://127.0.0.1:8080

Enable `network_anomaly_pipeline`.

## 7. Git

```powershell
git init
git add .
git commit -m "initial network anomaly detection project"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

## 8. Project structure

```text
network-anomaly-detection/
├── dags/
│   └── network_anomaly_pipeline.py
├── data/
├── models/
├── mlruns/
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── generate.py
│   │   └── validate.py
│   ├── features/
│   │   ├── __init__.py
│   │   └── engineering.py
│   ├── __init__.py
│   ├── model.py
│   ├── pipeline.py
│   └── api.py
├── tests/
│   └── test_pipeline.py
├── config.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

## 9. Risk levels

- `0.00-0.39` Low
- `0.40-0.69` Medium
- `0.70-1.00` High

## 10. Main commands

```powershell
python -m src.data.generate
python -m src.data.validate
python -m src.pipeline
mlflow ui --port 5000
uvicorn src.api:app --port 8000
pytest
git status
git add .
git commit -m "update model"
git push
```
