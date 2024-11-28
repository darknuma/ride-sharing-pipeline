from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pendulum

default_args = {
    'owner': 'numa',
    'retries': 10,
    'retry_delay': timedelta(hours=1),

}

with DAG(
    'kafka_to_delta_dag',
    default_args=default_args,
    description='Ingest Kafka data into Delta Lake',
    schedule=None,
    start_date=pendulum.now('UTC'),
    catchup=False,
) as dag:
    
    kafka_to_delta_task = BashOperator(
        task_id='kafka_to_delta_task',
        bash_command = "python /opt/airflow/kafka_to_delta.py",
env={'PATH': '/bin:/usr/bin:/usr/local/bin'}


    )
    
    kafka_to_delta_task

