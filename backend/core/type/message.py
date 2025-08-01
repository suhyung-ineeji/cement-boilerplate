from enum import Enum

class MessageType(Enum):
    FACTORY_DATA = "factory_data"
    PREDICT_DATA = "predict_data"
    INFERENCE = "inference"
    PREDICT_REQUEST = "predict_request"

