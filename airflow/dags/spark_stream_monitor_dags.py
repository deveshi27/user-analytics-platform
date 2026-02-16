from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException
from datetime import datetime, timedelta
import os, time

SPARK_OUTPUT_DIR = "/opt/spark/output"
MAX_STALE_MINUTES = 10


def check_spark_output():
    if not os.path.exists(SPARK_OUTPUT_DIR):
        raise AirflowFailException("Spark output directory missing")

    files = [
        os.path.join(SPARK_OUTPUT_DIR, f)
        for f in os.listdir(SPARK_OUTPUT_DIR)
        if f.endswith(".parquet")
    ]

    if not files:
        raise AirflowFailException("No parquet files found")

    latest = max(files, key=os.path.getmtime)
    age_min = (time.time() - os.path.getmtime(latest)) / 60

    if age_min > MAX_STALE_MINUTES:
        raise AirflowFailException("Spark output is stale")

    print("Spark streaming healthy")


default_args = {
    "owner": "data-eng",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="spark_stream_monitor",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/5 * * * *",
    catchup=False,
) as dag:

    PythonOperator(
        task_id="check_spark_output",
        python_callable=check_spark_output
    )
