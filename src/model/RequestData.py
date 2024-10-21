from pydantic import BaseModel


class RequestData(BaseModel):
    username: str
    prompt: str
    
    
class InferRequestData(BaseModel):
    
    user_id: str
    session_id: str
    message: str
    role: str
    timestamp: str