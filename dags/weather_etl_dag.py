from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

from weather_etl.extract import extract_weather
from weather_etl.transform import transform_weather
from weather_etl.load import load_weather

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="weather_etl_dag",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["weather", "openweathermap", "etl"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_weather",
        python_callable=extract_weather,
    )

    transform_task = PythonOperator(
        task_id="transform_weather",
        python_callable=transform_weather,
    )

    load_task = PythonOperator(
        task_id="load_weather",
        python_callable=load_weather,
    )

    extract_task >> transform_task >> load_task
