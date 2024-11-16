#!/bin/bash

# Wait for the database to be ready
sleep 10

# Initialize the Airflow database
airflow db init

# Start the Airflow webserver
exec airflow webserver