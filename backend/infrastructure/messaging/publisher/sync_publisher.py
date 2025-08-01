import pika

from infrastructure.messaging.enum import RabbitMQExchange, RabbitMQExchangeType
from infrastructure.messaging.message import Message
from infrastructure.messaging.settings import rabbitmq_settings
from infrastructure.messaging.publisher.interface import IPublisher


class SyncPublisher(IPublisher):
    def __init__(self):
        self.host = rabbitmq_settings.RABBITMQ_HOST
        self.port = rabbitmq_settings.RABBITMQ_PORT
        self.user = rabbitmq_settings.RABBITMQ_USER
        self.password = rabbitmq_settings.RABBITMQ_PASSWORD
        self.vhost = rabbitmq_settings.RABBITMQ_VHOST

        self.__connection = None
        self.__channel = None

    def ensure_connection(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.vhost,
            credentials=credentials,
            blocked_connection_timeout=10,
            retry_delay=2,
            connection_attempts=5,
            heartbeat=30,
        )
        if self.__connection is None:
            self.__connection = pika.BlockingConnection(parameters)
        if self.__channel is None:
            self.__channel = self.__connection.channel()
        
        return self.__channel

    def publish(
        self,
        message: Message,
        exchange: RabbitMQExchange,
        exchange_type: RabbitMQExchangeType = RabbitMQExchangeType.FANOUT,
    ):
        self.ensure_connection().basic_publish(
            exchange=exchange.value,
            routing_key=exchange_type.value,
            body=message.model_dump_json().encode()
        )
