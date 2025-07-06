from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from backend.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Evento(Base):
    __tablename__ = 'eventos'
    
    id_evento = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(500), nullable=False)
    fecha_evento = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)

    def __repr__(self):
        return f"<Evento(id={self.id_evento}, descripcion='{self.descripcion[:30]}...')>"
