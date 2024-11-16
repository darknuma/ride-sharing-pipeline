KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "ride-events"
AVRO_SCHEMA_JSON = """
{
    "type": "record",
    "name": "Ride",
    "fields": [
        {"name": "ride_id", "type": "string"},
        {"name": "city", "type": "string"},
        {"name": "ride_type", "type": "string"},
        {"name": "start_time", "type": "long"},
        {"name": "end_time", "type": "long"},
        {"name": "duration_minutes", "type": "int"},
        {"name": "distance_miles", "type": "float"},
        {"name": "fare_usd", "type": "float"},
        {"name": "driver_id", "type": "string"},
        {"name": "rider_id", "type": "string"}
    ]
}
"""
