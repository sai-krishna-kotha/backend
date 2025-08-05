from pydantic_settings import BaseSettings, SettingsConfigDict

# This class loads our settings from the .env file.
class Settings(BaseSettings):
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()