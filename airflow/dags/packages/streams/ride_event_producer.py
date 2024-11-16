import json
import time
from datetime import datetime, timedelta
from kafka import KafkaProducer
import random
from dataclasses import dataclass, asdict
import fastavro 
from io import BytesIO

CITIES = ["New York City", "Buffalo", "Rochester", "Yonkers",
           "Syracuse", "Albany (the state capital)", "New Rochelle", "Mount Vernon", 
           "Schenectady", "Utica"]
RIDE_TYPES = ["UberX", "UberXL", "UberBLACK", "UberSUV", "UberPOOL"]

@dataclass
class Ride:
    ride_id: str
    city: str
    ride_type: str
    start_time: int  # Use int for timestamp
    end_time: int    # Use int for timestamp
    duration_minutes: int
    distance_miles: float
    fare_usd: float
    driver_id: str
    rider_id: str

class RideGenerator:
    def __init__(self):
        self.current_time = datetime.now()

    def generate_ride(self):
        ride_id = f"RIDE-{self.current_time.strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
        city = random.choice(CITIES)
        ride_type = random.choice(RIDE_TYPES)
        start_time = self.current_time
        duration = random.randint(5, 60)
        end_time = start_time + timedelta(minutes=duration)
        distance = round(random.uniform(1, 20), 2)
        fare = round(5 + (2 * distance) + (0.5 * duration), 2)
        
        return Ride(
            ride_id=ride_id,
            city=city,
            ride_type=ride_type,
            start_time=int(start_time.timestamp() * 1000),  # Convert to milliseconds
            end_time=int(end_time.timestamp() * 1000),      # Convert to milliseconds
            duration_minutes=duration,
            distance_miles=distance,
            fare_usd=fare,
            driver_id=f"DRIVER-{random.randint(1000, 9999)}",
            rider_id=f"RIDER-{random.randint(1000, 9999)}"
        )

# Define the Avro schema as a Python dictionary
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

def serialize_avro(ride, schema):
    buffer = BytesIO()
    fastavro.writer(buffer, schema, [asdict(ride)])
    return buffer.getvalue()

def produce_rides(producer, topic_name, generator, schema, rides_per_minute=60):
    while True:
        ride = generator.generate_ride()
        avro_data = serialize_avro(ride, schema)
        producer.send(topic_name, avro_data)
        print(f"Produced ride: {ride.ride_id} at {ride.start_time}")
        time.sleep(60 / rides_per_minute)

def main():
    producer = KafkaProducer(bootstrap_servers=['kafka-broker-1:9092', 'kafka-broker-2:9093'])
    topic_name = 'ride-events'

    generator = RideGenerator()
    produce_rides(producer, topic_name, generator, avro_schema, rides_per_minute=60)

    producer.close()

# if __name__ == "__main__":
#     main()
