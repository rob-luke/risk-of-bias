from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # model selection
    fast_ai_model: str = "gpt-4.1-nano"
    good_ai_model: str = "gpt-4.1-mini"
    best_ai_model: str = "gpt-4.1"

    # OpenAI API settings
    temperature: float = 0.2


settings = Settings()
