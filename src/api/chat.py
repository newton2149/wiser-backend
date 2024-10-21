import json
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from utils.db_utils import deduct_credits, generate_title_store, get_user_credits, retrieve_conversation_history,store_conversation,create_new_session,retrieve_last_message,retrieve_conversation,add_token_usage, store_conversation_v2
from model.RequestData import RequestData,InferRequestData
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


@chat_router.post("/inference")
async def analyse(data: InferRequestData,username: str = Depends(get_current_user)):
    
   
    prompt = data.message
    user_credits = get_user_credits(username)
        
    if user_credits <= 0:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    result,cb = inference(prompt)
    generate_title_store(data.session_id,data.user_id,data.message)
    

    deduct_credits(username, cost=cb.total_cost)
    add_token_usage(username, tokens=cb.total_tokens)

    

    return Response(content=json.dumps({"message": result}), headers={"X-Session-ID": data.session_id}, media_type="application/json")



@chat_router.post("/inference-reply")
async def analyse(data: InferRequestData,username: str = Depends(get_current_user)):
    
    prompt = data.message
    user_credits = get_user_credits(username)
        
    if user_credits <= 0:
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    history = retrieve_conversation_history(data.username,data.session_id)
    
    result,cb = reply_analyse(history,prompt)
    

    deduct_credits(data.username, cost=cb.total_cost)
    add_token_usage(data.username, tokens=cb.total_tokens)


    
    return Response(content=json.dumps({"message": result}), headers={"X-Session-ID": data.session_id}, media_type="application/json")

@chat_router.post("/store")
async def store(data: InferRequestData,username: str = Depends(get_current_user)):
        
        store_conversation_v2(data)
        
        return Response(content=json.dumps({"message": "Stored"}), headers={"X-Session-ID": data.session_id}, media_type="application/json")



