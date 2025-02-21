from enum import Enum

from pydantic import BaseModel
from typing_extensions import Optional


class MessageType(str, Enum):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"


class MessageAction(str, Enum):
    STOP = "STOP"
    MOVE = "MOVE"
    UPDATE = "UPDATE"


class Message(BaseModel):
    message_type: MessageType
    message_action: MessageAction
    extra: Optional[str] = None
