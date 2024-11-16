FROM apache/airflow:2.8.0-python3.10

# Switch to root user


# Copy requirements file
COPY ./airflow/requirements.txt /home/requirements.txt

# Install requirements
RUN pip install -r /home/requirements.txt

USER root 

RUN apt-get update \
&& apt-get install -y --no-install-recommends \
    default-jre \
    default-jdk \
    curl \
    wget \
&& apt-get autoremove -yqq --purge \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-default-jdk

RUN mkdir -p /opt/spark/jars \
&& chown -R airflow:root /opt/spark

WORKDIR /opt/spark/jars

RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.3/spark-sql-kafka-0-10_2.12-3.5.3.jar \
&& wget https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.1.0/delta-core_2.12-2.1.0.jar \
&& wget https://repo1.maven.org/maven2/org/apache/spark/spark-avro_2.12/3.5.3/spark-avro_2.12-3.5.3.jar \
&& chown -R airflow:root /opt/spark/jars

# Copy the custom entrypoint script
COPY ./custom_entrypoint.sh /home/airflow/custom_entrypoint.sh

RUN chmod +x /home/airflow/custom_entrypoint.sh

# Switch back to airflow user
USER airflow

