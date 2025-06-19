from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database Config
    db_username: str
    db_password: str
    db_hostname: str
    db_port: str
    db_name: str

    # JWT Config
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    #SMTP Configuration
    smtp_host: str 
    smtp_port: int 
    smtp_email: EmailStr
    smtp_password: str

    class Config:
        env_file = ".env"


settings = Settings()