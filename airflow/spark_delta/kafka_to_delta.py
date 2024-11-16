from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import col

def create_spark_session():
    return (SparkSession.builder
            .appName("KafkaToDeltaStream")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .getOrCreate())

# Define the Avro schema as a string
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
            .option("subscribe", "ride-events")  # Your topic name
            .option("startingOffsets", "earliest")
            .load())

def process_kafka_data(df):
    # Use from_avro to deserialize Avro data
    return (df
            .select(from_avro(col("value"), avro_schema).alias("data"))
            .select("data.*"))

def write_to_delta(df, checkpoint_path, delta_path):
    return (df.writeStream
            .format("delta")
            .outputMode("append")
            .option("checkpointLocation", checkpoint_path)
            .option("mergeSchema", "true")
            .start(delta_path))

def main():
    spark = create_spark_session()
    
    # Read from Kafka
    kafka_df = read_from_kafka(spark)
    
    # Process the data
    processed_df = process_kafka_data(kafka_df)
    
    # Write to Delta Lake
    checkpoint_path = "/tmp/checkpoint/kafka_to_delta"
    delta_path = "/tmp/delta/kafka_data"
    
    # For debugging
    print("Schema of processed DataFrame:")
    processed_df.printSchema()
    
    query = write_to_delta(processed_df, checkpoint_path, delta_path)
    
    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        query.stop()
        spark.stop()

if __name__ == "__main__":
    main()