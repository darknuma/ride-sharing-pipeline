from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import col
import logging
# from typing import Optional, DataFrame 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 


def create_spark_session():
    return (SparkSession.builder
            .appName("KafkaToDeltaStream")
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,"
                                           "org.apache.spark:spark-avro_2.12:3.5.3,"
                                           "io.delta:delta-core_2.12:2.1.0,"
                                           "org.apache.kafka:kafka-clients:3.5.2:3.5.3")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .getOrCreate())



avro_schema = """
{
  "type": "record",
  "name": "Ride",
  "fields": [
    {"name": "ride_id", "type": "string"},
    {"name": "city", "type": "string"},
    {"name": "ride_type", "type": "string"},
    {"name": "start_time", "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "end_time", "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "duration_minutes", "type": "int"},
    {"name": "distance_miles", "type": "float"},
    {"name": "fare_usd", "type": "float"},
    {"name": "driver_id", "type": "string"},
    {"name": "rider_id", "type": "string"}
  ]
}
"""

def read_from_kafka(spark):
    return (spark
            .readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", "kafka-broker-1:9092,kafka-broker-2:9093")
            .option("subscribe", "ride-events")  
            .option("startingOffsets", "earliest")
            .option("includeHeaders", "true")
            .load())


def process_kafka_data(kafka_df, avro_schema: str):
    """Process Kafka data using provided Avro schema."""
    try:
        if not avro_schema or not isinstance(avro_schema, str):
            raise ValueError("Invalid Avro schema provided")
            
        kafka_df = kafka_df.filter(col("value").isNotNull())
        
        processed_df = kafka_df.select(
            from_avro(col("value"), avro_schema).alias("data")
        ).select("data.*")
        
        return processed_df
    except Exception as e:
        logger.error(f"Failed to process Kafka data: {str(e)}")
        raise



def write_to_delta(df, checkpoint_path, delta_path):
    return (df.writeStream
            .format("delta")
            .outputMode("append")
            .option("checkpointLocation", checkpoint_path)
            .option("mergeSchema", "true")
            .start(delta_path))

def main():
    spark = create_spark_session()

    # Reduce logging
    spark.sparkContext.setLogLevel("WARN")
    
    # Read from Kafka
    kafka_df = read_from_kafka(spark)

    kafka_df.isStreaming  # Check if the dataframe is streaming
    kafka_df.printSchema()  # Print schema to check the fields
    
    # Process the data
    processed_df = process_kafka_data(kafka_df, avro_schema)
    
    
    # Write to Delta Lake
    checkpoint_path = "/tmp/checkpoint/kafka_to_delta"
    delta_path = "/tmp/delta/kafka_data"
    
    # For debugging
    print("Schema of processed DataFrame:")
    processed_df.printSchema()
    
    query = write_to_delta(processed_df, checkpoint_path, delta_path)
    
    try:
        query.awaitTermination()
    except Exception as e:
        logger.error(f"Streaming query failed: {str(e)}")
        query.stop()
    finally:
        spark.stop()

if __name__ == "__main__":
    main()