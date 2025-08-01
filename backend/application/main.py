import sys
sys.path.append("..")

import json
from fastapi import FastAPI
import uvicorn

from core.type.message import MessageType
from infrastructure.messaging.publisher.async_publisher import AsyncPublisher
from infrastructure.messaging.enum import RabbitMQExchange, RabbitMQExchangeType
from infrastructure.messaging.message import Message

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/predict")
async def predict():
    publisher = AsyncPublisher()
    msg = Message(message_type=MessageType.PREDICT_REQUEST, data={"message": "Hello World"})
    await publisher.publish(
        message=msg,
        exchange_name=RabbitMQExchange.PREDICT_REQUEST,
        exchange_type=RabbitMQExchangeType.FANOUT
    )
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
