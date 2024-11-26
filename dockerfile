FROM apache/airflow:2.8.0-python3.10

# Copy the requirements file for Python dependencies
COPY ./airflow/requirements.txt /home/requirements.txt

# Install Python dependencies from the requirements file
RUN pip install -r /home/requirements.txt

# Switch to root user to install system dependencies
USER root 

# Update the package list and install necessary dependencies
# Install Java and necessary dependencies
RUN apt-get update \
&& apt-get install -y --no-install-recommends \
    msopenjdk-11 \
    curl \
    wget \
    procps \
    python3-pip \
&& apt-get autoremove -yqq --purge \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable for msopenjdk-11
ENV JAVA_HOME="/usr/lib/jvm/msopenjdk-11-amd64"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Set up Spark directories
ENV SPARK_HOME=/opt/spark
ENV PYTHONPATH="/home/airflow/.local/lib/python3.10/site-packages/pyspark"
ENV PATH="${SPARK_HOME}/bin:${PATH}"

# Create necessary directories for Spark and other configurations
RUN mkdir -p "${SPARK_HOME}/jars" \
    && mkdir -p "${SPARK_HOME}/work-dir" \
    && mkdir -p "${SPARK_HOME}/conf" \
    && mkdir -p /tmp/ivy \
    && mkdir -p /tmp/spark-temp

# Set working directory to /opt/spark for Spark installation
WORKDIR /opt/spark

# Download Spark tarball from the official source
RUN wget -q https://downloads.apache.org/spark/spark-3.5.3/spark-3.5.3-bin-hadoop3.tgz

# Extract the Spark tarball and remove the tarball file
RUN tar -xzf spark-3.5.3-bin-hadoop3.tgz --strip-components=1 \
    && rm -f spark-3.5.3-bin-hadoop3.tgz

# Download necessary Spark JARs directly into the $SPARK_HOME/jars directory
RUN wget -q https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.3/spark-sql-kafka-0-10_2.12-3.5.3.jar -P ${SPARK_HOME}/jars \
    && wget -q https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.1.0/delta-core_2.12-2.1.0.jar -P ${SPARK_HOME}/jars \
    && wget -q https://repo1.maven.org/maven2/org/apache/spark/spark-avro_2.12/3.5.3/spark-avro_2.12-3.5.3.jar -P ${SPARK_HOME}/jars \
    && wget -q https://repo1.maven.org/maven2/org/apache/spark/spark-launcher_2.12/3.5.3/spark-launcher_2.12-3.5.3.jar -P ${SPARK_HOME}/jars

# Set proper permissions for the Spark directory and files
RUN chown -R airflow:root "${SPARK_HOME}" \
    && chmod -R 775 "${SPARK_HOME}" \
    && chown -R airflow:root /tmp/ivy \
    && chmod -R 775 /tmp/ivy \
    && chown -R airflow:root /tmp/spark-temp \
    && chmod -R 775 /tmp/spark-temp 

# Copy the custom entrypoint script into the container
COPY ./custom_entrypoint.sh /home/airflow/custom_entrypoint.sh

# Make the custom entrypoint script executable
RUN chmod +x /home/airflow/custom_entrypoint.sh

# Switch back to the airflow user for running Airflow processes
USER airflow
