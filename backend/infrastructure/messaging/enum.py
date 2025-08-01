from enum import Enum


class RabbitMQExchange(Enum):
    FACTORY_DATA = "factory.data"
    PREDICT_DATA = "predict.data"
    PREDICT_REQUEST = "predict.request"

class RabbitMQExchangeType(Enum):
    FANOUT = "fanout"
    DIRECT = "direct"
    TOPIC = "topic"
    HEADERS = "headers"

class RabbitMQQueue(Enum):
    CACHE_SETTER = "cache.setter"
    DB_SAVER = "db.saver"
    PREDICT_REQUEST = "predict.request"