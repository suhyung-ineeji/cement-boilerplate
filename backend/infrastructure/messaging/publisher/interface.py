from abc import ABCMeta, abstractmethod
from infrastructure.messaging.enum import RabbitMQExchange, RabbitMQExchangeType
from infrastructure.messaging.message import Message

class IPublisher(metaclass=ABCMeta):
    @abstractmethod
    def publish(
        self,
        message: Message,
        exchange: RabbitMQExchange,
        exchange_type: RabbitMQExchangeType,
    ):
        pass
