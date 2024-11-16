from kafka import KafkaConsumer
import json

TOPIC_NAME = "event_types"

consumer = KafkaConsumer(
    TOPIC_NAME,
    auto_offset_reset='earliest',
    bootstrap_servers = ['kafka:9092'],
    group_id = 'different_event_types',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')
                        ))

def read_events():
    for m in consumer:
        print(m.value)


# if __name__ == "__main__":
#     read_events()