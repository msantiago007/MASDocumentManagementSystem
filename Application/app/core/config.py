from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    # Base Configuration
    PROJECT_NAME: str = "Document Management System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # SQL Server Configuration
    DB_HOST: str = "EC2AMAZ-8NPGMI\\SQLEXPRESS"
    DB_NAME: str = "DocumentManagement"
    DB_PORT: str = "1433"
    
    # Storage
    STORAGE_DIR: Path = Path(__file__).parent.parent.parent / "storage"
    ML_MODELS_DIR: Path = STORAGE_DIR / "ml_models"
    VECTOR_STORE_DIR: Path = STORAGE_DIR / "vectors"
    
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mssql+pyodbc://{self.DB_HOST}/{self.DB_NAME}"
            "?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&trusted_connection=yes"
        )

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()