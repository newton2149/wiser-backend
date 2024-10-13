from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from utils.db_utils import deduct_credits, get_user_credits,store_conversation,create_new_session,retrieve_last_message,retrieve_conversation,add_token_usage
from model.RequestData import RequestData
from model.RequestReplyData import RequestReplyData
from utils.utils import inference,reply_analyse
from .auth import get_current_user

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

def generate_stream(result: str):
    # This generator will stream the result in chunks
    for chunk in result:
        yield chunk

@chat_router.post("/analyse")
async def analyse(data: RequestData,username: str = Depends(get_current_user)):
    
    session_id  = create_new_session(username)
    prompt = data.prompt
    user_credits = get_user_credits(data.username)
        
    if user_credits <= 0:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    result,cb = inference(prompt)
    

    deduct_credits(data.username, cost=cb.total_cost)
    add_token_usage(data.username, tokens=cb.total_tokens)
    
    store_conversation(username,session_id,prompt,role="user")
    store_conversation(username,session_id,result,role="ai")
    
    # Stream the result back to the user
    return StreamingResponse(generate_stream(result), media_type="text/plain")


@chat_router.post("/reply/analyse")
async def analyse(data: RequestReplyData,username: str = Depends(get_current_user)):
    
    prompt = data.prompt
    user_credits = get_user_credits(username)
        
    if user_credits <= 0:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    history = retrieve_conversation(data.username,data.session_id)
    
    result,cb = reply_analyse(history,prompt)
    

    deduct_credits(data.username, cost=cb.total_cost)
    add_token_usage(data.username, tokens=cb.total_tokens)
    
    store_conversation(username,data.session_id,prompt,role="user")
    store_conversation(username,data.session_id,result,role="ai")    
    

    
    return StreamingResponse(generate_stream(result), media_type="text/plain")


