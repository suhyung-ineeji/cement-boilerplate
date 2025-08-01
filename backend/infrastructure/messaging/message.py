from pydantic import BaseModel

from core.type.message import MessageType

class Message(BaseModel):
    message_type: MessageType
    data: dict

    def to_bytes(self) -> bytes:
        return self.model_dump_json().encode("utf-8")

    @staticmethod
    def from_bytes(data: bytes) -> "Message":
        return Message.model_validate_json(data.decode("utf-8"))
