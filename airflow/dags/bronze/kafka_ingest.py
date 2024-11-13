"""
Automate the ingestion process by orchestrating the Kafka producers and consumers. 
This might include starting and stopping data streams as needed, managing topic creation (e.g., “Ride Events” and “Ride Summary”), and monitoring message flow.

"""
from airflow.providers.apache.kafka.operators.produce import KafkaProducerOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow import DAG 
from kafka import KafkaProducer
import json
from datetime import timedelta
from scripts.kafka.ride_summary_producer import send_events

# Kafka producer setup
KAFKA_BROKER = 'kafka:9092'  # Update with your Kafka broker
KAFKA_TOPIC = 'event_types'  # Your target Kafka topic

def produce_message():
    # Create a Kafka producer instance
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
    message = {"": "value", "timestamp": "2024-11-13 15:00"}
    # Send a message to Kafka
    producer.send(KAFKA_TOPIC, value=message)
    producer.flush()
    producer.close()

# Define the default_args for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'kafka_producer_dag',
    default_args=default_args,
    description='Simple Kafka producer DAG',
    schedule_interval=None,  # Can be set to a cron expression, or `None` for manual trigger
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Create a task to produce a message to Kafka
    produce_kafka_message = PythonOperator(
        task_id='produce_kafka_message',
        python_callable=produce_message,
    )

    produce_kafka_message