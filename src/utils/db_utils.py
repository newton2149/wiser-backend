from db_init import SessionLocal, User,db
from model.RequestData import InferRequestData
from model.UserCreate import UserCreate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from utils.utils import generate_title
import datetime
import uuid


# Function to get user credits by user_id
def get_user_credits(username: str) -> int:
    # Create a new session
    session = SessionLocal()
    try:
        # Fetch the user from the database
        user = session.query(User).filter(User.username == username).first()
        
        if not user:
            raise Exception(f"User with id {username} not found.")
        
        # Return the user's available credits
        return user.credits
    finally:
        session.close()
        
def get_user_plan(username: str) -> int:
    # Create a new session
    session = SessionLocal()
    try:
        # Fetch the user from the database
        user = session.query(User).filter(User.username == username).first()
        
        if not user:
            raise Exception(f"User with id {username} not found.")
        
        # Return the user's available credits
        return user.plan
    finally:
        session.close()


def deduct_credits(username: str, cost: int):
    # Create a new session
    session = SessionLocal()
    try:
        # Fetch the user from the database
        user = session.query(User).filter(User.username == username).first()
        
        if not user:
            raise Exception(f"User with id {username} not found.")
        
        # Ensure the user has enough credits
        if user.credits < cost:
            raise Exception("Not enough credits to perform this action.")
        
        # Deduct the cost from the user's credits
        user.credits -= cost
        session.commit()
    finally:
        session.close()
        
def add_token_usage(username: str, tokens: int):
    # Create a new session
    session = SessionLocal()
    try:
        # Fetch the user from the database
        user = session.query(User).filter(User.username == username).first()
        
        if not user:
            raise Exception(f"User with id {username} not found.")
        
        # Add the tokens to the user's token count
        user.tokens += tokens
        session.commit()
    finally:
        session.close()

def create_user_db(user: UserCreate):
    # Create a new session
    session = SessionLocal()
    try:
        existing_user = session.query(User).filter_by(email=user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists.")

        db_user = User(username=user.username, email=user.email)

        session.add(db_user)
        session.commit()  
        session.refresh(db_user) 

        return db_user.id 

    except IntegrityError as e:
        session.rollback()  
        raise HTTPException(status_code=400, detail="User with this email or username already exists.")
    
    except SQLAlchemyError as e:
        session.rollback()  
        raise HTTPException(status_code=500, detail="Database error occurred. Please try again later.")
    
    finally:
        session.close() 
        
        
def user_exists(username: str) -> bool:
    # Create a new session
    session = SessionLocal()
    try:
        # Fetch the user from the database
        user = session.query(User).filter(User.username == username).first()
        
        if not user:
            return False
        return True
    finally:
        session.close()
        
        


def create_new_session(user_id):
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    return session_id


import datetime

def get_user_conversation_collection():
    # collection_name = f"conversation_{user_id}"  # Collection name based on user_id
    return db["session"]

def get_session_title():
    # collection_name = f"conversation_{user_id}"  # Collection name based on user_id
    return db["title"]

def store_conversation(user_id, session_id, message, role="user",respone=False):
    # Get the conversation collection
    collection = get_user_conversation_collection()
    
    if respone:
        if if_session_exists(user_id, session_id) == False:
            raise HTTPException("Session does not exist.")    
    
    
    # Define the conversation structure
    conversation = {
        "user_id": user_id,
        "session_id": session_id,
        "message": message,
        "role": role,  # Can be 'user' or 'assistant'
        "timestamp": datetime.datetime.now()
    }
    
    # Insert the message into the collection
    collection.insert_one(conversation)
    print(f"Stored message for user {user_id} in session {session_id}.")
    

def store_conversation_v2(data: InferRequestData):
    # Get the conversation collection
    collection = get_user_conversation_collection()
    

    
    
    # Define the conversation structure
    conversation = {
        "user_id": data.user_id,
        "session_id": data.session_id,
        "message": data.message,
        "role": data.role,  # Can be 'user' or 'assistant'
        "timestamp": data.timestamp
    }
    
    # Insert the message into the collection
    collection.insert_one(conversation)
    print(f"Stored message for user {data.user_id} in session {data.session_id}.")


def retrieve_last_message(user_id, session_id):
    collection = get_user_conversation_collection()
    
    last_message = collection.find_one(
        {"user_id": user_id, "session_id": session_id},
        sort=[("timestamp", -1)] 
    )
    
    if last_message:
        return (last_message["role"], last_message["message"])
    else:
        return None

def retrieve_conversation_history(user_id, session_id):
    collection = get_user_conversation_collection()
    
    if if_session_exists(user_id, session_id) == False:
        raise HTTPException("Session does not exist.")
    
    messages = list(collection.find({"user_id": user_id, "session_id": session_id}).sort("timestamp", 1))
    
    conversation_history_message = "\n".join([message["message"] for message in messages])
    
    return conversation_history_message

def retrieve_conversation(user_id, session_id):
    collection = get_user_conversation_collection()
    
    if if_session_exists(user_id, session_id) == False:
        raise HTTPException("Session does not exist.")
    
    messages = list(collection.find({"user_id": user_id, "session_id": session_id}).sort("timestamp", 1))
    
   
    
    return messages



def if_session_exists(user_id, session_id):
    collection = get_user_conversation_collection()
    
    session = collection.find_one({"user_id": user_id, "session_id": session_id})
    
    return session is not None





def generate_title_store(session_id,username,msg):
    
    collection = get_session_title()
    t = generate_title(msg)
    title = {
        "session_id": session_id,
        "user_id": username,
        "title": t,
        "timestamp": datetime.datetime.now()
    }
    
    collection.insert_one(title)
    
    print(f"Stored title for user {msg} in session {msg}.")
    
    return msg


def get_All_title(user_id):
    
    collection = get_session_title()
    
    titles = collection.find({"user_id": user_id})
    
    return titles
    

def retrieve_all_session_id(user_id):
    # Get the user's specific conversation collection
    collection = get_user_conversation_collection()

    session_ids = collection.distinct("session_id", {"user_id": user_id})
    print(session_ids)
    
    return session_ids

def retrieve_all_session_title(user_id):

    collection = get_session_title()
    session_ids = collection.distinct("session_id", {"user_id": user_id})
    print(session_ids)
    
    return session_ids