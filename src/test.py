# import datetime
# import uuid
# from utils.db_utils import get_user_conversation_collection
from utils.utils import generate_title
def retrieve_conversation(user_id, session_id):
    collection = get_user_conversation_collection()
    
    messages = list(collection.find({"user_id": user_id, "session_id": session_id,"role":"user"}).sort("timestamp", 1))
    
    
    
    return messages


def retrieve_all_session_id(user_id):
    # Get the user's specific conversation collection
    collection = get_user_conversation_collection()

    session_ids = collection.distinct("session_id", {"user_id": user_id})
    
    return session_ids


def create_new_session(user_id):
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    return session_id


result,cb = generate_title("Analyse Tata steel and give the data about its financial")

print(result) 