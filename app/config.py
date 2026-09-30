from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduGenie"
    app_version: str = "1.0.0"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    demo_mode: bool = True
    cors_origins: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()