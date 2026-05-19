from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "RILL API"
    database_url: str = "sqlite:///./rill.db"
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()

