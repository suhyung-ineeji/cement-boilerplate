from abc import ABCMeta, abstractmethod

class IConsumer(metaclass=ABCMeta):
    @abstractmethod
    def consume(self)->bytes:
        pass