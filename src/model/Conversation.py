from pydantic import BaseModel
from typing import List
from datetime import datetime

class Message(BaseModel):
    sender: str  # "user" or "ai"
    content: str
    timestamp: datetime

class RequestData(BaseModel):
    prompt: str

class Conversation(BaseModel):
    conversation_id: str
    user_id: str
    messages: List[Message] = []
    created_at: datetime
    updated_at: datetime
