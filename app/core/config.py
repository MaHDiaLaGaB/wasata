import os
from dotenv import load_dotenv
from pydantic import BaseSettings, condecimal

load_dotenv()


class Config(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    class Config:
        env_file = ".env"


config = Config()
