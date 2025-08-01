import sys
sys.path.append("..")

import asyncio

from core.domain.factory_data import FactoryData
from infrastructure.cache.cache_info import FactoryDataCache, PredictDataCache
from infrastructure.messaging.consumer.async_consumer import AsyncConsumer
from infrastructure.messaging.publisher.async_publisher import AsyncPublisher
from infrastructure.messaging.enum import RabbitMQExchange, RabbitMQExchangeType, RabbitMQQueue
from infrastructure.messaging.message import Message
from infrastructure.cache.redis import RedisCache
from core.type.message import MessageType
from ai_inference.predict import predict


consumer = AsyncConsumer()
publisher = AsyncPublisher()
cache = RedisCache()

async def get_data(byte_msg: bytes):
    # 메세지 수신
    msg = Message.from_bytes(byte_msg)
    print(msg.data)

    # 예측 수행
    cache_data = cache.get_list_cache(FactoryDataCache.key, 100)
    data_list = [FactoryData(**data) for data in cache_data]
    predict_data = predict(data_list)
    predict_data_msg = Message(message_type=MessageType.PREDICT_DATA, data=predict_data.model_dump())

    # 결과 발행
    await publisher.publish(
        message=predict_data_msg,
        exchange_name=RabbitMQExchange.PREDICT_DATA,
        exchange_type=RabbitMQExchangeType.FANOUT
    )

async def task():
    await consumer.consume(RabbitMQQueue.PREDICT_REQUEST, get_data)

if __name__ == "__main__":
    asyncio.run(task())
