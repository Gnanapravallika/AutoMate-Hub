from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AutoMate Hub"
    API_V1_STR: str = "/api/v1"
    
    # Email Settings (to be populated from env)
    MAIL_USERNAME: str = "your_email@example.com"
    MAIL_PASSWORD: str = "your_password"
    MAIL_FROM: str = "your_email@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    
    # File Settings
    UPLOAD_DIR: str = "temp/uploads"
    INVOICE_DIR: str = "temp/invoices"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
