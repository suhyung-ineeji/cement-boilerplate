import aio_pika
from typing import Callable
import inspect
from infrastructure.messaging.enum import RabbitMQQueue
from infrastructure.messaging.consumer.interface import IConsumer
from infrastructure.messaging.settings import rabbitmq_settings

class AsyncConsumer(IConsumer):
    def __init__(self):
        self.host = rabbitmq_settings.RABBITMQ_HOST
        self.port = rabbitmq_settings.RABBITMQ_PORT
        self.user = rabbitmq_settings.RABBITMQ_USER
        self.password = rabbitmq_settings.RABBITMQ_PASSWORD
        self.vhost = rabbitmq_settings.RABBITMQ_VHOST
        
        self.__connection = None
        self.__channel = None

    async def ensure_connection(self):
        if self.__connection is None:
            self.__connection = await aio_pika.connect_robust(
                host=self.host,
                port=self.port,
                login=self.user,
                password=self.password,
                virtualhost=self.vhost,
            )
        if self.__channel is None:
            self.__channel = await self.__connection.channel()

        return self.__channel

    async def consume(self, queue_name: RabbitMQQueue, callback: Callable):
        channel = await self.ensure_connection()
        queue = await channel.get_queue(name=queue_name.value)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    if inspect.iscoroutinefunction(callback):
                        await callback(message.body)
                    else:
                        callback(message.body)