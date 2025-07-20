from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from backend.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Archivo(Base):
    __tablename__ = "archivos"

    id_archivo = Column(Integer, primary_key=True, autoincrement=True)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(String(500), nullable=False)
    fecha_subida = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    def __repr__(self):
        return f"<Archivo(id={self.id_archivo}, nombre='{self.nombre_archivo}')>"
