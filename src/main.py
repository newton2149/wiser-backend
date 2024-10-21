from fastapi import FastAPI
from api.auth import auth_router
from api.chat import chat_router
from api.user import user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(user_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)