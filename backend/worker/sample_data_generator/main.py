import sys
sys.path.append("..")

from datetime import datetime
import random
import time

from core.type.message import MessageType
from infrastructure.messaging.message import Message
from infrastructure.messaging.publisher.sync_publisher import SyncPublisher
from infrastructure.messaging.enum import RabbitMQExchange


factory_id = 1
data_id = 1
def get_random_factory_data() -> dict:
    global factory_id, data_id

    data = {
            "factory_id": factory_id,
            "data_id": data_id,
            "val1": random.uniform(0, 100),
            "val2": random.uniform(0, 100),
            "val3": random.uniform(0, 100),
            "val4": random.uniform(0, 100),
            "val5": random.uniform(0, 100),
            "collected_at": datetime.now().isoformat()
        }
    data_id += 1
    factory_id += 1

    return data

def get_random_predict_data() -> dict:
    return {
        "predict1": random.uniform(0, 100),
        "predict2": random.uniform(0, 100),
        "predict3": random.uniform(0, 100),
        "predict4": random.uniform(0, 100),
        "predict5": random.uniform(0, 100),
        "predicted_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    publisher = SyncPublisher()

    while True:
        
        factory_data = get_random_factory_data()
        factory_data_msg = Message(message_type=MessageType.FACTORY_DATA, data=factory_data)
        publisher.publish(factory_data_msg, exchange=RabbitMQExchange.FACTORY_DATA)

        time.sleep(1)
