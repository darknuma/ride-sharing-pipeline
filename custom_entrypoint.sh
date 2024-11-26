#!/bin/bash

# Create necessary Spark directories if they don't exist
mkdir -p /tmp/ivy
mkdir -p /tmp/spark-temp
mkdir -p /home/airflow/.local/lib/python3.10/site-packages/pyspark/jars
mkdir -p /home/airflow/.local/conf

# Set proper permissions
chmod -R 775 /tmp/ivy
chmod -R 775 /tmp/spark-temp
chmod -R 775 /home/airflow/.local

# Wait for the database to be ready
sleep 10

# Initialize the Airflow database if needed
airflow db init

# Execute the original Airflow entrypoint with the provided command
if [ "$1" = "webserver" ]; then
    exec airflow webserver
else
    exec /entrypoint "${@}"
fi