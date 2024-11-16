# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime, timedelta
# import subprocess

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# def submit_spark_job():
#     spark_submit_command = [
#         'spark-submit',
#         '--master', 'spark://spark:7077',  # Change to your Spark Master URL
#         # '--conf', 'spark.executor.memory=2g',
#         './spark_delta/kafka_to_delta.py'  # Path to your Spark job script
#     ]
#     subprocess.run(spark_submit_command, check=True)

# with DAG(
#     'custom_spark_submit_dag',
#     default_args=default_args,
#     description='Submit Spark job using custom PythonOperator',
#     schedule_interval=None,
#     start_date=datetime(2023, 1, 1),
#     catchup=False,
# ) as dag:

#     submit_spark_job_task = PythonOperator(
#         task_id='submit_spark_job',
#         python_callable=submit_spark_job,
#         show_return_value_in_logs=True,
#     )

#     submit_spark_job_task
