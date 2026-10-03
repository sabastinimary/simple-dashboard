from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="network_anomaly_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    generate = BashOperator(
        task_id="generate_data",
        bash_command="cd $AIRFLOW_HOME/../network-anomaly-detection && python -m src.data.generate"
    )

    validate = BashOperator(
        task_id="validate_data",
        bash_command="cd $AIRFLOW_HOME/../network-anomaly-detection && python -m src.data.validate"
    )

    train = BashOperator(
        task_id="train_and_track",
        bash_command="cd $AIRFLOW_HOME/../network-anomaly-detection && python -m src.pipeline"
    )

    generate >> validate >> train
