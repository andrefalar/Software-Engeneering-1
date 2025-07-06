from sqlalchemy.ext.declarative import declarative_base

# Base compartida para todos los modelos
# Esto permite que SQLAlchemy vea todas las tablas y sus relaciones
Base = declarative_base()
