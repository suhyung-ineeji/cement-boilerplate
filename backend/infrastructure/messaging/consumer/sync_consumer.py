import pika

from infrastructure.messaging.enum import RabbitMQQueue
from infrastructure.messaging.consumer.interface import IConsumer
from infrastructure.messaging.settings import rabbitmq_settings


class SyncConsumer(IConsumer):
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

    def consume(self, queue_name: RabbitMQQueue)->bytes:
        channel = self.ensure_connection()
        channel.queue_declare(queue=queue_name.value, passive=True, durable=True)
        _, _, byte_message = channel.basic_get(queue=queue_name.value, auto_ack=True)
        if byte_message:
            return byte_message
        return b""
