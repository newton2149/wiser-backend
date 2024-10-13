from pydantic import BaseModel


class RequestData(BaseModel):
    username: str
    prompt: str
