import os
from typing import Optional

class Settings:
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tu-clave-secreta-muy-segura")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File paths
    USUARIOS_FILE: str = r"C:\Users\Denisse Albarrán Lpz\OneDrive\Escritorio\Ingeniería de Software\Pruebas\MS-Ingreso\usuarios.txt"
    
    # CORS settings
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000", "*"]

settings = Settings()