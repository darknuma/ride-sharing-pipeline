# from pyspark.sql import SparkSession
# from pyspark.sql.avro.functions import from_avro
# from pyspark.sql.functions import col
# import logging
# # from typing import Optional, DataFrame 


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__) 


# def create_spark_session():
#     return (SparkSession.builder
#             .appName("KafkaToDeltaStream")
#             .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,"
#                                            "org.apache.spark:spark-avro_2.12:3.5.3,"
#                                            "io.delta:delta-spark_2.12:3.2.0,"
#                                            "org.apache.kafka:kafka-clients:3.5.2")
#             .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
#             .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
#             .getOrCreate())



# avro_schema = """
# {
#   "type": "record",
#   "name": "Ride",
#   "fields": [
#     {"name": "ride_id", "type": "string"},
#     {"name": "city", "type": "string"},
#     {"name": "ride_type", "type": "string"},
#     {"name": "start_time", "type": {"type": "long", "logicalType": "timestamp-millis"}},
#     {"name": "end_time", "type": {"type": "long", "logicalType": "timestamp-millis"}},
#     {"name": "duration_minutes", "type": "int"},
#     {"name": "distance_miles", "type": "float"},
#     {"name": "fare_usd", "type": "float"},
#     {"name": "driver_id", "type": "string"},
#     {"name": "rider_id", "type": "string"}
#   ]
# }
# """

# def read_from_kafka(spark):
#     return (spark
#             .readStream
#             .format("kafka")
#             .option("kafka.bootstrap.servers", "kafka-broker-1:9092,kafka-broker-2:9093")
#             .option("subscribe", "ride-events")  
#             .option("startingOffsets", "earliest")
#             .option("includeHeaders", "true")
#             .load())


# def process_kafka_data(kafka_df, avro_schema: str):
#     """Process Kafka data using provided Avro schema."""
#     try:
#         if not avro_schema or not isinstance(avro_schema, str):
#             raise ValueError("Invalid Avro schema provided")
            
#         kafka_df = kafka_df.filter(col("value").isNotNull())
        
#         processed_df = kafka_df.select(
#             from_avro(col("value"), avro_schema).alias("data")
#         ).select("data.*")
        
#         return processed_df
#     except Exception as e:
#         logger.error(f"Failed to process Kafka data: {str(e)}")
#         raise

# def write_to_delta(df, checkpoint_path, delta_path):
#     try:
#         query = (df.writeStream
#                  .format("delta")
#                  .outputMode("append")
#                  .option("checkpointLocation", checkpoint_path)
#                  .option("mergeSchema", "true")
#                  .trigger(processingTime='10 seconds')
#                  .start(delta_path))
#         return query
#     except Exception as e:
#         logger.error(f"Error writing to Delta: {str(e)}")
#         raise

# def main():
#     spark = create_spark_session()

#     # Reduce logging
#     spark.sparkContext.setLogLevel("WARN")
#     spark.conf.set("spark.sql.adaptive.enabled", "false")
    
#     # Read from Kafka
#     kafka_df = read_from_kafka(spark)

#     kafka_df.isStreaming  # Check if the dataframe is streaming
#     kafka_df.printSchema()  # Print schema to check the fields
    
#     # Process the data
#     processed_df = process_kafka_data(kafka_df, avro_schema)
    
    
#     # Write to Delta Lake
#     checkpoint_path = "/tmp/checkpoint_kafka_to_delta"
#     delta_path = "/tmp/kafka_data"
    
#     # For debugging
#     print("Schema of processed DataFrame:")
#     processed_df.printSchema()
    
#     query = write_to_delta(processed_df, checkpoint_path, delta_path)
    
#     try:
#         query.awaitTermination()
#     except Exception as e:
#         logger.error(f"Streaming query failed: {str(e)}")
#         query.stop()
#     finally:
#         spark.stop()

# if __name__ == "__main__":
#     main()


# from pyspark.sql import SparkSession
# from pyspark.sql.avro.functions import from_avro
# from pyspark.sql.functions import col, lit
# import logging

# # Setup Logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Configuration Variables
# KAFKA_BROKERS = "kafka-broker-1:9092,kafka-broker-2:9093"
# KAFKA_TOPIC = "ride-events"
# CHECKPOINT_PATH = "/opt/airflow/checkpoint_kafka_to_delta"
# DELTA_PATH = "/opt/airflow/kafka_data"
# MALFORMED_RECORDS_PATH = "/opt/airflow/malformed_records"
# PROCESSING_TIME = "10 seconds"

# # Avro Schema Definition
# AVRO_SCHEMA = """
# {
#   "type": "record",
#   "name": "Ride",
#   "fields": [
#     {"name": "ride_id", "type": "string"},
#     {"name": "city", "type": "string"},
#     {"name": "ride_type", "type": "string"},
#     {"name": "start_time", "type": {"type": "long", "logicalType": "timestamp-millis"}},
#     {"name": "end_time", "type": {"type": "long", "logicalType": "timestamp-millis"}},
#     {"name": "duration_minutes", "type": "int"},
#     {"name": "distance_miles", "type": "float"},
#     {"name": "fare_usd", "type": "float"},
#     {"name": "driver_id", "type": "string"},
#     {"name": "rider_id", "type": "string"}
#   ]
# }
# """

# def create_spark_session() -> SparkSession:
#     """
#     Create and configure a Spark session with necessary packages.
#     """
#     return (SparkSession.builder
#             .appName("KafkaToDeltaStream")
#             .config("spark.jars.packages", 
#                     "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,"
#                     "org.apache.spark:spark-avro_2.12:3.5.3,"
#                     "io.delta:delta-spark_2.12:3.2.0,"
#                     "org.apache.kafka:kafka-clients:3.5.2")
#             .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
#             .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
#             .getOrCreate())

# def read_from_kafka(spark: SparkSession):
#     """
#     Read data from Kafka as a streaming DataFrame.
#     """
#     logger.info("Reading data from Kafka...")
#     return (spark
#             .readStream
#             .format("kafka")
#             .option("kafka.bootstrap.servers", KAFKA_BROKERS)
#             .option("subscribe", KAFKA_TOPIC)
#             .option("startingOffsets", "earliest")
#             .option("includeHeaders", "true")
#             .option("mode", "PERMISSIVE")  # Switch to PERMISSIVE mode
#             .load())

# def process_kafka_data(kafka_df, avro_schema: str)-> None:
#     """
#     Process Kafka data by applying the Avro schema, separating malformed records.
#     """
#     logger.info("Processing Kafka data...")

#     if not avro_schema:
#         raise ValueError("Avro schema is missing or invalid")

#     # Filter out records with null value
#     kafka_df = kafka_df.filter(col("value").isNotNull())

#     # Extract valid and malformed records
#     processed_df = kafka_df.select(
#         from_avro(col("value"), avro_schema, {"mode": "PERMISSIVE"}).alias("data")
#     ).select("data.*")

#     malformed_df = kafka_df.filter(col("value").isNull()) \
#         .withColumn("error", lit("Malformed record")) \
#         .withColumn("original_value", col("value"))

#     logger.info("Successfully processed Kafka data.")
#     return processed_df, malformed_df

# def write_to_delta(df, checkpoint_path: str, delta_path: str):
#     """
#     Write processed data to Delta Lake in append mode.
#     """
#     logger.info(f"Writing data to Delta Lake at {delta_path}...")
#     return (df.writeStream
#             .format("delta")
#             .outputMode("append")
#             .option("checkpointLocation", checkpoint_path)
#             .option("mergeSchema", "true")
#             .trigger(processingTime=PROCESSING_TIME)
#             .start(delta_path))

# def write_malformed_records(malformed_df, output_path: str):
#     """
#     Write malformed records to a specified path for debugging and analysis.
#     """
#     logger.info(f"Writing malformed records to {output_path}...")
#     return (malformed_df.writeStream
#             .format("json")
#             .outputMode("append")
#             .option("path", output_path)
#             .option("checkpointLocation", f"{output_path}_checkpoint")
#             .start())

# def main():
#     """
#     Main function to orchestrate reading, processing, and writing Kafka data to Delta Lake.
#     """
#     spark = create_spark_session()
#     spark.sparkContext.setLogLevel("WARN")

#     try:

#         kafka_df = read_from_kafka(spark)
#         kafka_df.printSchema()  # Debugging: Print schema

#         processed_df, malformed_df = process_kafka_data(kafka_df, AVRO_SCHEMA)
#         processed_df.printSchema()  # Debugging: Print processed schema

#         query_valid = write_to_delta(processed_df, CHECKPOINT_PATH, DELTA_PATH)

#         query_malformed = write_malformed_records(malformed_df, MALFORMED_RECORDS_PATH)

#         query_valid.awaitTermination()
#         query_malformed.awaitTermination()
#     except Exception as e:
#         logger.error(f"Error occurred: {str(e)}")
#         raise
#     finally:
#         spark.stop()
#         logger.info("Spark session stopped.")

# if __name__ == "__main__":
#     main()


from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, from_json
from pyspark.sql.types import TimestampType
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, LongType
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BROKERS = "kafka-broker-1:9092,kafka-broker-2:9093"
KAFKA_TOPIC = "ride-events"
CHECKPOINT_PATH = "/opt/airflow/checkpoint_kafka_to_delta"
DELTA_PATH = "/opt/airflow/kafka_data"
MALFORMED_RECORDS_PATH = "/opt/airflow/malformed_records"
PROCESSING_TIME = "10 seconds"

JSON_SCHEMA = StructType([
    StructField("ride_id", StringType(), True),
    StructField("city", StringType(), True),
    StructField("ride_type", StringType(), True),
    StructField("start_time", TimestampType(), True),
    StructField("end_time", TimestampType(), True),
    StructField("duration_minutes", IntegerType(), True),
    StructField("distance_miles", FloatType(), True),
    StructField("fare_usd", FloatType(), True),
    StructField("driver_id", StringType(), True),
    StructField("rider_id", StringType(), True),
])

def create_spark_session() -> SparkSession:
    """
    Create and configure a Spark session with necessary packages.
    """
    return (SparkSession.builder
            .appName("KafkaToDeltaStream")
            .config("spark.jars.packages", 
                    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,"
                    "io.delta:delta-spark_2.12:3.2.0,"
                    "org.apache.kafka:kafka-clients:3.5.2")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .getOrCreate())

def read_from_kafka(spark: SparkSession):
    """
    Read data from Kafka as a streaming DataFrame.
    """
    logger.info("Reading data from Kafka...")
    return (spark
            .readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", KAFKA_BROKERS)
            .option("subscribe", KAFKA_TOPIC)
            .option("startingOffsets", "earliest")
            .option("includeHeaders", "true")
            .load())

def process_kafka_data(kafka_df, json_schema: StructType):
    logger.info("Processing Kafka data...")

    processed_df = kafka_df.select(
        from_json(col("value").cast("string"), json_schema).alias("parsed_data")
    ).select("parsed_data.*")

    malformed_df = kafka_df.filter(
        from_json(col("value").cast("string"), json_schema).isNull()
    ).withColumn("error", lit("Malformed record"))

    logger.info("Successfully processed Kafka data.")
    return processed_df, malformed_df

def write_to_delta(df, checkpoint_path: str, delta_path: str):
    """
    Write processed data to Delta Lake in append mode.
    """
    logger.info(f"Writing data to Delta Lake at {delta_path}...")
    return (df.writeStream
            .format("delta")
            .outputMode("append")
            .option("checkpointLocation", checkpoint_path)
            .option("mergeSchema", "true")
            .trigger(processingTime=PROCESSING_TIME)
            .start(delta_path))

def write_malformed_records(malformed_df, output_path: str):
    """
    Write malformed records to a specified path for debugging and analysis.
    """
    logger.info(f"Writing malformed records to {output_path}...")
    return (malformed_df.writeStream
            .format("json")
            .outputMode("append")
            .option("path", output_path)
            .option("checkpointLocation", f"{output_path}_checkpoint")
            .start())

def main():
    """
    Main function to orchestrate reading, processing, and writing Kafka data to Delta Lake.
    """
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    try:
        kafka_df = read_from_kafka(spark)
        kafka_df.printSchema()  

        processed_df, malformed_df = process_kafka_data(kafka_df, JSON_SCHEMA)
        processed_df.printSchema()  

        query_valid = write_to_delta(processed_df, CHECKPOINT_PATH, DELTA_PATH)

        query_malformed = write_malformed_records(malformed_df, MALFORMED_RECORDS_PATH)

        query_valid.awaitTermination()
        query_malformed.awaitTermination()
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise
    finally:
        spark.stop()
        logger.info("Spark session stopped.")

if __name__ == "__main__":
    main()
