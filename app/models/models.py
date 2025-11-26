from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class TipoUsuario(Base):
    __tablename__ = "tipo_usuario"
    
    id_tipo_usuario = Column(Integer, primary_key=True, index=True)
    tipo_usuario = Column(String, nullable=False)
    
    usuarios = relationship("Usuario", back_populates="tipo_usuario")

class Usuario(Base):
    __tablename__ = "usuario"
    
    id_usuario = Column(Integer, primary_key=True, index=True)
    correo_usuario = Column(String, unique=True, nullable=False)
    id_tipo_usuario = Column(Integer, ForeignKey("tipo_usuario.id_tipo_usuario"))
    contrasena = Column(String, nullable=False)
    
    tipo_usuario = relationship("TipoUsuario", back_populates="usuarios")