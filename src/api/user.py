from fastapi import APIRouter, Depends, HTTPException, Response

from api.auth import get_current_user
from utils.db_utils import get_All_title, get_user_credits, get_user_plan, retrieve_all_session_id, retrieve_all_session_title, retrieve_conversation

user_router = APIRouter()

@user_router.get("/credits")
async def get_credits(username: str = Depends(get_current_user)):
    user_credits = get_user_credits(username)
    return {"credits": user_credits}


@user_router.get("/plan")
async def get_plan(username: str = Depends(get_current_user)):
    user_plan = get_user_plan(username)
    return {"plan": user_plan}


@user_router.get("/fetch/{session_id}")
async def fetch_conversation(session_id: str, username: str = Depends(get_current_user)):
    conversation = retrieve_conversation(username, session_id)
    return conversation

@user_router.get("/fetch-session-title/{username}")
async def fetch_session_title(username: str = Depends(get_current_user)):
    session_ids = get_All_title(username)
    return session_ids