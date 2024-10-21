from pydantic_settings import BaseSettings


class DbConfig(BaseSettings):
    mongo_url: str = "mongodb+srv://mongo:Appu9677@wiser-chat.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
    rds_postgres_url: str = "postgresql+psycopg2://postgres:appu9677@wiser-db.cjo2qsmkkvt3.us-east-1.rds.amazonaws.com:5432/postgres"
    mongo_db_name: str = "wiser-chat"


db_config = DbConfig()