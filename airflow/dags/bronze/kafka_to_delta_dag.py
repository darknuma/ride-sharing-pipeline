# from airflow import DAG
# from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
# from airflow.utils.dates import days_ago
# from datetime import timedelta
# import os 
# import pendulum 
# from datetime import datetime, timedelta

# os.environ["SPARK_HOME"] = "/home/airflow/.local/lib/python3.10/site-packages/pyspark"
# os.environ["PATH"] += f":{os.environ['SPARK_HOME']}/bin" 
# os.environ["PYTHONPATH"] = "/home/airflow/.local/lib/python3.10/site-packages/pyspark"


# default_args = {
#     'owner': 'airflow',
#     'retries': 3,
#     'retry_delay': timedelta(minutes=5),
# }

# with DAG(
#     'kafka_to_delta_dag',
#     default_args=default_args,
#     description='Ingest Kafka data into Delta Lake using Spark',
#     schedule=None,
#     start_date=pendulum.now('UTC'),
#     catchup=False,
# ) as dag:
    
#     kafka_to_delta_task = SparkSubmitOperator(
#         task_id='kafka_to_delta_task',
#         application='/opt/airflow/kafka_to_delta.py',
#         conn_id='spark_default',
#         conf={
#             "spark.jars.packages": (
#                 "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,"
#                 "io.delta:delta-core_2.12:2.1.0,"
#                 "org.apache.spark:spark-avro_2.12:3.5.3",
#                 "org.apache.kafka:kafka-clients:3.5.2"
#             ),
#             "spark.jars": "/home/airflow/.local/lib/python3.10/site-packages/pyspark/jars/*",
#             "spark.driver.extraClassPath": "/home/airflow/.local/lib/python3.10/site-packages/pyspark/jars/*",
#             "spark.executor.extraClassPath": "/home/airflow/.local/lib/python3.10/site-packages/pyspark/jars/*",
#             "spark.driver.extraJavaOptions": "-Divy.cache.dir=/tmp -Divy.home=/tmp",
#             "spark.executor.extraJavaOptions": "-Divy.cache.dir=/tmp -Divy.home=/tmp",
#             "spark.jars.ivy": "/tmp/ivy",
#             "spark.local.dir": "/tmp/spark-temp"
#         },
#         name='KafkaToDeltaStream',
#         execution_timeout=timedelta(minutes=20),
#         driver_memory='2g',
#         executor_memory='2g',
#         num_executors=2,
#         verbose=True,
#         env_vars={
#             'SPARK_HOME': '/home/airflow/.local/lib/python3.10/site-packages/pyspark',
#             'PYTHONPATH': '/home/airflow/.local/lib/python3.10/site-packages/pyspark',
            
#         }

#     )
    
#     kafka_to_delta_task
