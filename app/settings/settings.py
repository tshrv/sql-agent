from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM Configuration
    llm_model: str = "gpt-4"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2048
    llm_api_key: str = "your_openai_api_key_here"
    llm_api_base_url: str = "http://172.29.192.1:11434/v1"
    llm_api_timeout: int = 60

    # Database configuration
    postgres_db: str = "sql_agent_db"
    postgres_user: str = "sql_agent_user"
    postgres_password: str = "sql_agent_password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    pgadmin_email: str = "pgadmin@example.com"
    pgadmin_password: str = "pgadmin_password"
    pgadmin_port: int = 8080

    class Config:
        env_file = ".env"


settings = Settings()
