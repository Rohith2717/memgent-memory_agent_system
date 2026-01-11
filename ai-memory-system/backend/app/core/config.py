from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI Memory System"
    ENV: str = "dev"

    VECTOR_DB_PATH: str = "data/memory_index"
    EMBEDDING_MODEL: str = "default-embedding"
    LLM_PROVIDER: str = "local"

    class Config:
        env_file = ".env"

settings = Settings()
