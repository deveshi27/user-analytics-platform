from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException
from datetime import datetime, timedelta
import boto3
import time

BUCKET = "user-analytics-datalake-dev"
PREFIX = "silver/user_metrics/"   # or bronze/events_raw/
MAX_STALE_MINUTES = 10


def check_spark_s3_output():
    s3 = boto3.client("s3")

    response = s3.list_objects_v2(
        Bucket=BUCKET,
        Prefix=PREFIX
    )

    if "Contents" not in response:
        raise AirflowFailException("No Spark output found in S3")

    latest_obj = max(
        response["Contents"],
        key=lambda x: x["LastModified"]
    )

    age_minutes = (
        time.time() - latest_obj["LastModified"].timestamp()
    ) / 60

    if age_minutes > MAX_STALE_MINUTES:
        raise AirflowFailException(
            f"Spark output stale: {age_minutes:.1f} minutes old"
        )

    print("✅ Spark streaming healthy (S3 updated)")


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
        task_id="check_spark_s3_output",
        python_callable=check_spark_s3_output
    )
