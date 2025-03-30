from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URI: str
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES: int = 3600
    YANDEX_AUTH_URL: str
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_TOKEN_URL: str
    YANDEX_USER_INFO_URL: str
    LOKI_URL: str 
    UPLOAD_DIR: str = 'uploads'

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )

settings = Settings()
print(f"UPLOAD_DIR set to: {settings.UPLOAD_DIR}")

