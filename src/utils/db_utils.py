from db_init import SessionLocal, User,collection,db
from model.UserCreate import UserCreate
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
        # Create a new user
        db_user = User(username=user.username, email=user.email)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user.id
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

def get_user_conversation_collection(user_id):
    collection_name = f"conversation_{user_id}"  # Collection name based on user_id
    return db[collection_name]

def store_conversation(user_id, session_id, message, role="user"):
    # Get the user's specific conversation collection
    collection = get_user_conversation_collection(user_id)
    
    # Define the conversation structure
    conversation = {
        "user_id": user_id,
        "session_id": session_id,
        "message": message,
        "role": role,  # Can be 'user' or 'assistant'
        "timestamp": datetime.datetime.now()
    }
    
    # Insert the message into the user-specific collection
    collection.insert_one(conversation)
    print(f"Stored message for user {user_id} in session {session_id}.")
    
    
def retrieve_last_message(user_id, session_id):
    # Get the user's specific conversation collection
    collection = get_user_conversation_collection(user_id)
    
    # Fetch the most recent message by session_id, sorted by timestamp (descending order)
    last_message = collection.find_one(
        {"session_id": session_id},
        sort=[("timestamp", -1)]  # Sort by timestamp in descending order
    )
    
    # Return the last message if found, else None
    if last_message:
        return (last_message["role"], last_message["message"])
    else:
        return None

def retrieve_conversation(user_id, session_id):
    collection = get_user_conversation_collection(user_id)
    
    messages = list(collection.find({"session_id": session_id}).sort("timestamp", 1))
    
    # conversation_history = [(message["role"], message["message"]) for message in messages]
    
    conversation_history_message = "\n".join([message["message"] for message in messages])

    
        
    return conversation_history_message

