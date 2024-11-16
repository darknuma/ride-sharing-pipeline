from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, dayofweek, month, year, avg, count
from spark_setup import create_spark_session

def transform_ride_data():
    # Create Spark session using the helper function
    spark = create_spark_session()
    
    # Read from Delta table
    rides_df = spark.read.format("delta").load("/tmp/delta/kafka_data")
    
    # Extract time-based features
    rides_with_time = rides_df.withColumn("hour", hour("start_time")) \
                             .withColumn("day_of_week", dayofweek("start_time")) \
                             .withColumn("month", month("start_time")) \
                             .withColumn("year", year("start_time"))
    
    # Calculate ride metrics by city
    city_metrics = rides_with_time.groupBy("city") \
        .agg(
            avg("fare_usd").alias("avg_fare"),
            avg("distance_miles").alias("avg_distance"),
            avg("duration_minutes").alias("avg_duration"),
            count("*").alias("total_rides")
        )
    
    # Calculate hourly ride patterns
    hourly_patterns = rides_with_time.groupBy("city", "hour") \
        .agg(count("*").alias("rides_per_hour")) \
        .orderBy("city", "hour")
    
    # Calculate driver statistics
    driver_metrics = rides_df.groupBy("driver_id") \
        .agg(
            count("*").alias("total_rides"),
            avg("fare_usd").alias("avg_fare"),
            avg("distance_miles").alias("avg_distance")
        )
    
    # Write transformed data to new Delta tables
    city_metrics.write.format("delta").mode("overwrite").save("/tmp/delta/city_metrics")
    hourly_patterns.write.format("delta").mode("overwrite").save("/tmp/delta/hourly_patterns")
    driver_metrics.write.format("delta").mode("overwrite").save("/tmp/delta/driver_metrics")
    
    # Also save the enriched rides data with time features
    rides_with_time.write.format("delta").mode("overwrite").save("/tmp/delta/enriched_rides")

if __name__ == "__main__":
    transform_ride_data()
