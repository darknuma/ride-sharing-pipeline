import json
import time
from datetime import datetime, timedelta
from kafka import KafkaProducer
import random
from dataclasses import dataclass, asdict

CITIES = [
    "New York City", "Buffalo", "Rochester", "Yonkers",
    "Syracuse", "Albany (the state capital)", "New Rochelle", 
    "Mount Vernon", "Schenectady", "Utica"
]
RIDE_TYPES = ["UberX", "UberXL", "UberBLACK", "UberSUV", "UberPOOL"]

@dataclass
class Ride:
    ride_id: str
    city: str
    ride_type: str
    start_time: int  
    end_time: int   
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

def serialize_json(ride):
    """Serialize the ride object to JSON."""
    return json.dumps(asdict(ride)).encode('utf-8')

def produce_rides(producer, topic_name, generator, rides_per_minute=60):
    """Produce ride events and send them to the Kafka topic."""
    while True:
        ride = generator.generate_ride()
        json_data = serialize_json(ride)
        producer.send(topic_name, json_data)
        print(f"Produced ride: {ride.ride_id} at {ride.start_time}")
        time.sleep(60 / rides_per_minute)

def main():
    """Main function to start the Kafka producer."""
    producer = KafkaProducer(bootstrap_servers=['kafka-broker-1:9092', 'kafka-broker-2:9093'])
    topic_name = 'ride-events'

    generator = RideGenerator()
    produce_rides(producer, topic_name, generator, rides_per_minute=60)

    producer.close()

# if __name__ == "__main__":
#     main()
