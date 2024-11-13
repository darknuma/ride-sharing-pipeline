from kafka import KafkaConsumer
import fastavro
from io import BytesIO

avro_schema = {
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

def deserialize_avro(data, schema):
    # Use BytesIO to create a file-like object for fastavro to read
    buffer = BytesIO(data)
    reader = fastavro.reader(buffer, schema)
    return next(reader)

def consume_rides(topic_name):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='ride-consumers',
        value_deserializer=lambda x: deserialize_avro(x, avro_schema) 
    )

    for message in consumer:
        ride_data = message.value
        print(f"Consumed ride: {ride_data['ride_id']} - {ride_data['ride_type']} at {ride_data['start_time']}")
        
        

    consumer.close()

if __name__ == "__main__":
    consume_rides('ride-events')
