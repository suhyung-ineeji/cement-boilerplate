import sys
sys.path.append("..")

import asyncio

from core.type.message import MessageType
from infrastructure.messaging.consumer.async_consumer import AsyncConsumer
from infrastructure.messaging.enum import RabbitMQQueue
from infrastructure.cache.redis import RedisCache
from infrastructure.cache.cache_info import FactoryDataCache, PredictDataCache, CacheType
from infrastructure.messaging.message import Message

consumer = AsyncConsumer()
cache = RedisCache()

def job(byte_msg: bytes):
    if not byte_msg:
        return
    cache_msg = Message.from_bytes(byte_msg)

    match cache_msg.message_type:
        ###########################
        # 여기에 캐시 타입을 추가해주세요 #
        ###########################
        case MessageType.FACTORY_DATA:
            factory_data_cache = FactoryDataCache(**cache_msg.data)
            __set_cache_by_type(factory_data_cache.key, factory_data_cache.get_data_dict(), factory_data_cache.cache_type)
        case MessageType.PREDICT_DATA:
            predict_data_cache = PredictDataCache(**cache_msg.data)
            __set_cache_by_type(predict_data_cache.key, predict_data_cache.get_data_dict(), predict_data_cache.cache_type)
        case _:
            raise ValueError(f"Invalid cache type: {cache_msg.message_type}")

def __set_cache_by_type(key, value, cache_type):
    match cache_type:
        case CacheType.STRING:
            cache.set_cache_entry(key, value)
        case CacheType.LIST:
            cache.append_to_list_cache(key, value)


async def task():
    await consumer.consume(queue_name=RabbitMQQueue.CACHE_SETTER, callback=job)

if __name__ == "__main__":
    asyncio.run(task())
