from datetime import datetime
import json
import random
import time 
from kafka import KafkaProducer

# producer = KafkaProducer(value_serializer=lambda msg: json.dumps(msg).encode('utf-8'), 
#    bootstrap_servers=[' 127.0.0.1:29092'])

producer = KafkaProducer(
    value_serializer=lambda msg: json.dumps(msg).encode('utf-8'),
    bootstrap_servers=['kafka:9092']
)

TOPIC_NAME = "event_types"
RIDE_EVENTS = ['ride_requested', 'ride accepted', 'ride started', 'ride ended', 'ride cancelled']

def _producer_events():
    """
    Write the Producer of this event
    """
    return {
         'event_id': random.randint(1, 2999),
         'event_datetime': datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
         'event_type': random.choice(RIDE_EVENTS)

    }
   
def send_events():

    """
    send events
    """
    count = 0
    while count < 100:
        
        data = _producer_events()
        producer.send(TOPIC_NAME, data)
        count += 1
        time.sleep(3)
        producer.flush()


# if __name__ == '__main__':
#     send_events()



