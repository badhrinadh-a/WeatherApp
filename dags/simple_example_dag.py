from airflow import DAG
from airflow.sdk import task
import pendulum

with DAG(
    dag_id="simple_example_dag",
    description="A simple Airflow 3.1.5 DAG example",
    start_date=pendulum.now("UTC").subtract(days=1),
    schedule="@daily",
    catchup=False,
    tags=["example"],
):

    @task
    def hello():
        print("Hello from Airflow 3.1.5!")

    @task
    def goodbye():
        print("Goodbye from Airflow!")

    hello() >> goodbye() 

