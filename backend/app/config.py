from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = ""
    jwt_secret: str = "fallback_secret_change_in_production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    gemini_api_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
