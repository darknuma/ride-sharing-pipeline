FROM apache/airflow:2.8.0-python3.10

# Switch to root user


# Copy requirements file
COPY ./airflow/requirements.txt /home/requirements.txt

# Install requirements
RUN pip install -r /home/requirements.txt

USER root 

# Copy the custom entrypoint script
COPY ./custom_entrypoint.sh /home/airflow/custom_entrypoint.sh

# Make the custom entrypoint script executable
RUN chmod +x /home/airflow/custom_entrypoint.sh

# Switch back to airflow user
USER airflow

