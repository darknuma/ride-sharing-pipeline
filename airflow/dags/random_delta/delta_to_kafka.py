from spark_setup import create_spark_session
from configs.kafka_config import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS

def delta_to_kafka():
    spark = create_spark_session()
    
    delta_df = spark.read.format("delta").load("/home/to/delta/lake/ride-data")

    delta_df.selectExpr("CAST(value AS STRING)").write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("topic", KAFKA_TOPIC) \
        .save()