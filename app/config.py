from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Variables chargées depuis le fichier .env
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    
    # On garde le niveau de log, c'est utile
    LOG_LEVEL: str = "INFO"

    # Construction automatique de l'URL de connexion
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        extra = "ignore" 

settings = Settings()