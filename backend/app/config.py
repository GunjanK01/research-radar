from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central app config. Values are read from environment variables (or a .env file
    in local dev). In docker-compose, these get injected via the compose file's
    `environment:` block, so no .env file is needed inside containers.
    """

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/research_radar"
    openalex_mailto: str = "your-email@example.com"  # OpenAlex asks for this as a courtesy header
    embedding_model_name: str = "all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
