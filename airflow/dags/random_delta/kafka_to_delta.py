from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from random_delta.configs.kafka_config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, AVRO_SCHEMA_JSON
from random_delta.configs.delta_config import DELTA_TABLE_PATH, CHECKPOINT_PATH
# from configs.kafka_config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, AVRO_SCHEMA_JSON
# from configs.delta_config import DELTA_TABLE_PATH, CHECKPOINT_PATH

def run_kafka_to_delta_streaming():
    spark = SparkSession.builder \
        .appName("KafkaToDelta") \
        .config("spark.jars.packages", "org.apache.spark:spark-avro_2.12:3.3.0,io.delta:delta-core_2.12:2.1.0") \
        .getOrCreate() 


    rides_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "latest") \
        .load() \
        .selectExpr("CAST(value AS BINARY) as value")

    rides_deserialized_df = rides_df.select(
        from_avro(rides_df["value"], AVRO_SCHEMA_JSON).alias("ride_data")
    ).select("ride_data.*")

    rides_to_delta = rides_deserialized_df.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", CHECKPOINT_PATH) \
        .start(DELTA_TABLE_PATH)

    rides_to_delta.awaitTermination()

