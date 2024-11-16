from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'kafka_to_delta_dag',
    default_args=default_args,
    description='Ingest Kafka data into Delta Lake using Spark',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:
    
    kafka_to_delta_task = SparkSubmitOperator(
        task_id='kafka_to_delta_task',
        application='/opt/spark/work-dir/kafka_to_delta.py',
        conn_id='spark_default',
        conf={
            "spark.jars.packages": (
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,"
                "io.delta:delta-core_2.12:2.1.0,"
                "org.apache.spark:spark-avro_2.12:3.5.3"
            ),
            "spark.driver.extraJavaOptions": "-Divy.cache.dir=/tmp -Divy.home=/tmp",
            "spark.executor.extraJavaOptions": "-Divy.cache.dir=/tmp -Divy.home=/tmp"
        },
        packages=(
            'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,'
            'io.delta:delta-core_2.12:2.1.0,'
            'org.apache.spark:spark-avro_2.12:3.5.3'
        ),
        name='KafkaToDeltaStream',
        execution_timeout=timedelta(minutes=20),
        driver_memory='2g',
        executor_memory='2g',
        num_executors=2,
        verbose=True
    )
    
    kafka_to_delta_task