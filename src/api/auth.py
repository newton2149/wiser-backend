from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Header
from utils.jwt_utils import create_jwt_token, verify_jwt_token
from model.UserCreate import UserCreate
from utils.db_utils import create_user_db, user_exists
from starlette.status import HTTP_403_FORBIDDEN


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

async def get_current_user(authorization: str = Header(...)):
    try:
        # Expect the token to be in the format: Bearer <JWT_TOKEN>
        token_type, token = authorization.split(" ")
        
        if token_type != "Bearer":
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid token type")
        
        # Verify the token
        payload = verify_jwt_token(token)
        
        # Extract user info from token (you can add more claims like user_id, roles, etc.)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid token")
        
        return username
    except Exception as e:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(e))

@auth_router.post("/create_user")
async def create_user(user: UserCreate):
    user_id = create_user_db(user)
    return {"user_id": user_id}


@auth_router.post("/token")
async def login(username: str):
    if username is None:
        raise HTTPException(status_code=400, detail="Invalid username")
    
    if user_exists(username) == False:
        raise HTTPException(status_code=400, detail="User does not exist")
        
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_jwt_token(data={"sub": username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}