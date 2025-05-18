from pydantic_settings import BaseSettings  # Updated import
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra env variables

settings = Settings()
