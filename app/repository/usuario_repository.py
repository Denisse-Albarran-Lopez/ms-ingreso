from sqlalchemy.orm import Session
from app.models.models import Usuario, TipoUsuario
import bcrypt

class UsuarioRepository:
    
    def crear_usuario(self, db: Session, correo: str, contrasena: str, id_tipo_usuario: int):
        hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        db_usuario = Usuario(
            correo_usuario=correo,
            contrasena=hashed_password.decode('utf-8'),
            id_tipo_usuario=id_tipo_usuario
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    def obtener_usuario_por_correo(self, db: Session, correo: str):
        return db.query(Usuario).filter(Usuario.correo_usuario == correo).first()
    
    def verificar_contrasena(self, contrasena: str, hashed_password: str):
        return bcrypt.checkpw(contrasena.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def obtener_tipo_usuario_unam(self, db: Session):
        return db.query(TipoUsuario).filter(TipoUsuario.tipo_usuario == "UNAM").first()
    
    def obtener_tipo_usuario_externo(self, db: Session):
        return db.query(TipoUsuario).filter(TipoUsuario.tipo_usuario == "Externo").first()