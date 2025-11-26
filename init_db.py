from sqlalchemy.orm import Session
from app.database import SessionLocal, create_tables
from app.models.models import TipoUsuario

def init_database():
    create_tables()
    
    db = SessionLocal()
    try:
        # Verificar si ya existen los tipos de usuario
        if not db.query(TipoUsuario).filter(TipoUsuario.tipo_usuario == "UNAM").first():
            tipo_unam = TipoUsuario(tipo_usuario="UNAM")
            db.add(tipo_unam)
        
        if not db.query(TipoUsuario).filter(TipoUsuario.tipo_usuario == "Externo").first():
            tipo_externo = TipoUsuario(tipo_usuario="Externo")
            db.add(tipo_externo)
        
        db.commit()
        print("Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()