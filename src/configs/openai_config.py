from pydantic_settings import BaseSettings
from pathlib import Path

class OpenAiConfig(BaseSettings):
    azure_openai_api_key: str = '8483b03cc4084b919ab26c9a83677583'
    azure_openai_api_version: str = '2024-08-01-preview'
    azure_openai_endpoint: str = 'https://navne-m1xc43b3-eastus2.openai.azure.com/'
    azure_openai_deployment: str = 'gpt-4-2'
    azure_openai_embedding_model: str = 'text-embedding-3-large'
    vector_store_path: str = str(Path("src/vector_store").resolve())
    token_size: int = 4096


openai_config = OpenAiConfig()

