from sqlalchemy import create_engine, Column, Integer, String,FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis


DATABASE_URL = "postgresql+psycopg2://postgres:appu9677@localhost:5432/wiser"

# Create a database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB URI
db = client["chat_database"]  # Create or access a database
collection = db["conversations"]  

# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)  # Added email field
    credits = Column(FLOAT, default=5)
    tokens = Column(Integer, default=0)
    plan = Column(String, default="free")

# Create the tables
Base.metadata.create_all(bind=engine)
