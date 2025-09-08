from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Starter Kit"
    API_V1_PREFIX: str = "/api/v1"
    ENV: str = "development"  # default to dev
    DATABASE_URL: str  # must be provided in env
    FE_BASE_URL: str  # Frontend base URL

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()
