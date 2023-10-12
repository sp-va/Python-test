from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    DATABASE_HOST_TEST: str
    DATABASE_PORT_TEST: str
    DATABASE_NAME_TEST: str
    DATABASE_USER_TEST: str
    DATABASE_PASSWORD_TEST: str

    class Config:
        env_file = '.env'
        
settings = Settings()