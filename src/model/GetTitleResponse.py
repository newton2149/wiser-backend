from pydantic import BaseModel


class GetResponseTitle(BaseModel):
    session_id: str
    user_id: str
    title: str
    timestamp: str