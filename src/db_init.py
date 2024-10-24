from sqlalchemy import create_engine, Column, Integer, String,FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from configs.db_config import db_config

DATABASE_URL = db_config.rds_postgres_url

# Create a database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()




client = MongoClient(db_config.mongo_url)  # Replace with your MongoDB URI
db = client[db_config.mongo_db_name]  # Create or access a database


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
