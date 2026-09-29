from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_path: str = "yolo11n.pt"
    model_version: str = "yolo11n"
    confidence_threshold: float = 0.25

    database_url: str = (
        "postgresql+psycopg2://"
        "product_ai_user:product_ai_password"
        "@localhost:5432/product_ai"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()