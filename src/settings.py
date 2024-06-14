from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    pguser: str = "user"
    pgpassword: str = "password"
    pghost: str = "localhost"
    pgport: int = 5432
    pgdb: str = "postgres"
