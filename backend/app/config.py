from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "BioSample AI Gateway"
    debug: bool = True

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5433/biosample"
    redis_url: str = "redis://localhost:6380/0"

    biosamples_base_url: str = "https://www.ebi.ac.uk/biosamples"
    biosamples_timeout: float = 10.0
    
    # توکن EBI (اختیاری - اگر خالی باشد از Mock استفاده می‌شود)
    webin_token: str = ""

    llm_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

settings = Settings()