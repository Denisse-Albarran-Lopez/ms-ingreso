from sqlalchemy.orm import Session
from app.repository.usuario_repository import UsuarioRepository
from fastapi import HTTPException

class AuthService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
    
    def iniciar_sesion(self, db: Session, correo: str, contrasena: str):
        usuario = self.usuario_repo.obtener_usuario_por_correo(db, correo)
        if not usuario:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        if not self.usuario_repo.verificar_contrasena(contrasena, usuario.contrasena):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        return {"mensaje": "Inicio de sesión exitoso", "usuario_id": usuario.id_usuario}
    
    def registrar_usuario_unam(self, db: Session, correo: str, contrasena: str):
        if self.usuario_repo.obtener_usuario_por_correo(db, correo):
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        
        tipo_unam = self.usuario_repo.obtener_tipo_usuario_unam(db)
        if not tipo_unam:
            raise HTTPException(status_code=500, detail="Tipo de usuario UNAM no encontrado")
        
        usuario = self.usuario_repo.crear_usuario(db, correo, contrasena, tipo_unam.id_tipo_usuario)
        return {"mensaje": "Usuario UNAM registrado exitosamente", "usuario_id": usuario.id_usuario}
    
    def registrar_usuario_externo(self, db: Session, correo: str, contrasena: str):
        if self.usuario_repo.obtener_usuario_por_correo(db, correo):
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        
        tipo_externo = self.usuario_repo.obtener_tipo_usuario_externo(db)
        if not tipo_externo:
            raise HTTPException(status_code=500, detail="Tipo de usuario Externo no encontrado")
        
        usuario = self.usuario_repo.crear_usuario(db, correo, contrasena, tipo_externo.id_tipo_usuario)
        return {"mensaje": "Usuario externo registrado exitosamente", "usuario_id": usuario.id_usuario}