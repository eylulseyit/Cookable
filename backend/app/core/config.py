import os
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load the .env file from the 'backend' directory
# This makes the path independent of where the script is run from.
env_path = Path('.') / 'backend' / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./recipe.db"  # Changed from PostgreSQL to SQLite
    )
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Recipe Recommendation API"
    
    # Google AI API Key
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

settings = Settings() 