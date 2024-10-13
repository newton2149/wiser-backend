from pydantic import BaseModel


class RequestReplyData(BaseModel):
    username: str
    session_id: str
    prompt: str
