from pydantic_settings import BaseSettings
import os 

class Settings(BaseSettings):
    email: str = os.getenv("EMAIL")
    hostName: str = os.getenv("HOST_NAME")

    class Config:
        env_file = ".env"

settings = Settings()