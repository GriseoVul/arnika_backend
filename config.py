from pydantic_settings import BaseSettings
import os 

class Settings(BaseSettings):
    email: str = os.getenv("EMAIL", "")
    host_name: str = os.getenv("HOST_NAME", "")
    g_dock: str = os.getenv("G_DOCK")
    
    class Config:
        env_file = ".env"

settings = Settings()
