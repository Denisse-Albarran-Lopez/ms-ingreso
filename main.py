from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from google.auth.transport import requests
from google.oauth2 import id_token
import json
import os
from datetime import datetime
from typing import Optional

app = FastAPI(title="MS-Ingreso", description="Microservicio de autenticación")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ruta del archivo de usuarios
USUARIOS_FILE = r"C:\Users\Denisse Albarrán Lpz\OneDrive\Escritorio\Ingeniería de Software\Pruebas\MS-Ingreso\usuarios.txt"

# Modelos Pydantic
class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str

class RegisterRequest(BaseModel):
    correo: EmailStr
    contrasena: str

class GoogleAuthRequest(BaseModel):
    token: str

# Funciones auxiliares
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def load_users():
    if not os.path.exists(USUARIOS_FILE):
        return []
    try:
        with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return [json.loads(line) for line in content.split('\n') if line.strip()]
    except:
        return []

def save_user(user_data):
    with open(USUARIOS_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(user_data, ensure_ascii=False) + '\n')

def find_user_by_email(email: str):
    users = load_users()
    return next((user for user in users if user['correo'] == email), None)

def is_unam_email(email: str) -> bool:
    return email.endswith('@comunidad.unam.mx') or email.endswith('@unam.mx')

# Endpoints
@app.post("/auth/login")
async def login(request: LoginRequest):
    user = find_user_by_email(request.correo)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    if not verify_password(request.contrasena, user['contrasena_hash']):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    return {
        "mensaje": "Inicio de sesión exitoso",
        "usuario_id": user['id'],
        "tipo_usuario": user['tipo_usuario']
    }

@app.post("/auth/register/unam")
async def register_unam(request: RegisterRequest):
    if not is_unam_email(request.correo):
        raise HTTPException(status_code=400, detail="Debe usar un correo institucional UNAM")
    
    if find_user_by_email(request.correo):
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    user_data = {
        "id": len(load_users()) + 1,
        "correo": request.correo,
        "contrasena_hash": hash_password(request.contrasena),
        "tipo_usuario": "unam",
        "fecha_registro": datetime.now().isoformat(),
        "verificado": False
    }
    
    save_user(user_data)
    
    return {
        "mensaje": "Usuario UNAM registrado exitosamente",
        "usuario_id": user_data['id']
    }

@app.post("/auth/register/externo")
async def register_externo(request: RegisterRequest):
    if is_unam_email(request.correo):
        raise HTTPException(status_code=400, detail="Los correos UNAM deben registrarse como comunidad UNAM")
    
    if find_user_by_email(request.correo):
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    user_data = {
        "id": len(load_users()) + 1,
        "correo": request.correo,
        "contrasena_hash": hash_password(request.contrasena),
        "tipo_usuario": "externo",
        "fecha_registro": datetime.now().isoformat(),
        "verificado": False
    }
    
    save_user(user_data)
    
    return {
        "mensaje": "Usuario externo registrado exitosamente",
        "usuario_id": user_data['id']
    }

@app.post("/auth/google/unam")
async def google_auth_unam(request: GoogleAuthRequest):
    try:
        # Verificar token de Google (requiere configurar CLIENT_ID)
        # idinfo = id_token.verify_oauth2_token(request.token, requests.Request(), CLIENT_ID)
        
        # Por ahora simulamos la verificación
        # En producción, decodificar el token y obtener el email
        email = "usuario@comunidad.unam.mx"  # Esto vendría del token
        
        if not is_unam_email(email):
            raise HTTPException(status_code=400, detail="Debe usar un correo institucional UNAM")
        
        user = find_user_by_email(email)
        if not user:
            # Crear usuario automáticamente con Google OAuth
            user_data = {
                "id": len(load_users()) + 1,
                "correo": email,
                "contrasena_hash": "",  # No necesita contraseña con OAuth
                "tipo_usuario": "unam",
                "fecha_registro": datetime.now().isoformat(),
                "verificado": True,
                "oauth_provider": "google"
            }
            save_user(user_data)
            return {
                "mensaje": "Usuario UNAM creado y autenticado con Google",
                "usuario_id": user_data['id']
            }
        
        return {
            "mensaje": "Autenticación con Google exitosa",
            "usuario_id": user['id']
        }
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token de Google inválido")

@app.post("/auth/google/externo")
async def google_auth_externo(request: GoogleAuthRequest):
    try:
        # Verificar token de Google (requiere configurar CLIENT_ID)
        # idinfo = id_token.verify_oauth2_token(request.token, requests.Request(), CLIENT_ID)
        
        # Por ahora simulamos la verificación
        email = "usuario@gmail.com"  # Esto vendría del token
        
        if is_unam_email(email):
            raise HTTPException(status_code=400, detail="Los correos UNAM deben usar el endpoint específico")
        
        user = find_user_by_email(email)
        if not user:
            # Crear usuario automáticamente con Google OAuth
            user_data = {
                "id": len(load_users()) + 1,
                "correo": email,
                "contrasena_hash": "",  # No necesita contraseña con OAuth
                "tipo_usuario": "externo",
                "fecha_registro": datetime.now().isoformat(),
                "verificado": True,
                "oauth_provider": "google"
            }
            save_user(user_data)
            return {
                "mensaje": "Usuario externo creado y autenticado con Google",
                "usuario_id": user_data['id']
            }
        
        return {
            "mensaje": "Autenticación con Google exitosa",
            "usuario_id": user['id']
        }
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token de Google inválido")

@app.get("/")
async def root():
    return {"mensaje": "MS-Ingreso - Microservicio de autenticación"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)