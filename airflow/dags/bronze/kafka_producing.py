"""
Automate the ingestion process by orchestrating the Kafka producers and consumers. 
This might include starting and stopping data streams as needed, managing topic creation (e.g., “Ride Events” and “Ride Summary”), and monitoring message flow.

"""
import os
import sys
from airflow.plugins_manager import AirflowPlugin
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow import DAG 
from datetime import timedelta
# from packages.streams.ride_event_producer import main
from packages.streams.ride_event_json import main

sys.path.append('/home/airflow/dags/packages/streams') 


TOPIC_NAME = 'ride-events'

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'kafka_producer_dag',
    default_args=default_args,
    description='Producer for ride events',
    schedule_interval=None,  
    start_date=days_ago(1),
    catchup=True,
) as dag:
    
    produce_kafka_ride_message = PythonOperator(
        task_id="ride_events",
        python_callable=main,
        op_args=None,
        show_return_value_in_logs=True

    )

  
    produce_kafka_ride_message 


