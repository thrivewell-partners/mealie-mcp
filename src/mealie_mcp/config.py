from pydantic_settings import BaseSettings


class MealieSettings(BaseSettings):
    mealie_url: str = "http://localhost:9925"
    mealie_api_key: str = ""
    mealie_request_timeout: int = 30

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = MealieSettings()
