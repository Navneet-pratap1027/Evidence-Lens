from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    env: str = "development"
    api_port: int = 8000
    upload_dir: str = "uploads"
    max_file_size_mb: int = 200
    database_url: str = "sqlite:///./evidencelens.db"
    llm_api_key: str = ""
    class Config:
        env_file = ".env"
settings = Settings()