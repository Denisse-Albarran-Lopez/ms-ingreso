from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.service.auth_service import AuthService
from app.database import get_db

router = APIRouter()
auth_service = AuthService()

class LoginRequest(BaseModel):
    correo: str
    contrasena: str

class RegisterRequest(BaseModel):
    correo: str
    contrasena: str

@router.post("/login")
def iniciar_sesion(request: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.iniciar_sesion(db, request.correo, request.contrasena)

@router.post("/register/unam")
def registrar_usuario_unam(request: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.registrar_usuario_unam(db, request.correo, request.contrasena)

@router.post("/register/externo")
def registrar_usuario_externo(request: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.registrar_usuario_externo(db, request.correo, request.contrasena)