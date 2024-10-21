from pydantic_settings import BaseSettings


# class DbConfig(BaseSettings):
#     mongo_url: str = <MONGO_URL>
#     rds_postgres_url: str = <postgresdb_url>
#     mongo_db_name: str = "wiser-chat"


db_config = DbConfig()