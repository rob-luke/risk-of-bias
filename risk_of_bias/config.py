from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # model selection
    fast_ai_model: str = "gpt-4.1-nano"
    good_ai_model: str = "gpt-4.1-mini"
    best_ai_model: str = "gpt-4.1"


settings = Settings()
