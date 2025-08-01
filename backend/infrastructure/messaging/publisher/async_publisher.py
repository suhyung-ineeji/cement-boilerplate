import aio_pika

from infrastructure.messaging.enum import RabbitMQExchange, RabbitMQExchangeType
from infrastructure.messaging.publisher.interface import IPublisher
from infrastructure.messaging.settings import rabbitmq_settings
from infrastructure.messaging.message import Message
class AsyncPublisher(IPublisher):
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

    async def publish(
        self,
        message: Message,
        exchange_name: RabbitMQExchange,
        exchange_type: RabbitMQExchangeType,
    ):
        channel = await self.ensure_connection()
        exchange = await channel.declare_exchange(name=exchange_name.value, type=exchange_type.value, durable=True)
        await exchange.publish(aio_pika.Message(body=message.model_dump_json().encode()), routing_key=exchange_type.value)
