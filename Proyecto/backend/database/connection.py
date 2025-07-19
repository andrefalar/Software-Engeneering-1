from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


class DatabaseManager:
    """
    Gestor de conexión a la base de datos SQLite.
    Se encarga de:
    - Crear la conexión a la base de datos
    - Proporcionar sesiones para trabajar con los datos
    - Crear y eliminar tablas
    """

    def __init__(self, db_path="fortifile.db"):
        """
        Inicializa el gestor de base de datos

        Args:
            db_path (str): Ruta del archivo de base de datos SQLite
        """
        self.db_path = db_path

        # Crear el engine (motor de base de datos)
        # sqlite:/// indica que usamos SQLite con archivo local
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)

        # Crear la fábrica de sesiones
        # autocommit=False: Los cambios deben confirmarse manualmente
        # autoflush=False: Los cambios no se envían automáticamente
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        print(f"✅ DatabaseManager inicializado con archivo: {db_path}")

    def create_tables(self):
        """
        Crea todas las tablas definidas en los modelos
        """
        try:
            # Importar todos los modelos para que SQLAlchemy los conozca
            from backend.models.user_model import Usuario
            from backend.models.file_model import Archivo
            from backend.models.event_model import Evento
            from backend.models.base import Base

            # Crear todas las tablas usando la Base compartida
            Base.metadata.create_all(bind=self.engine)

            print("✅ Todas las tablas creadas correctamente")
            return True

        except Exception as e:
            print(f"❌ Error creando tablas: {e}")
            return False

    def get_session(self):
        """
        Obtiene una nueva sesión para trabajar con la base de datos

        Returns:
            Session: Sesión de SQLAlchemy para realizar operaciones
        """
        return self.SessionLocal()

    def drop_tables(self):
        """
        Elimina todas las tablas (útil para reiniciar el sistema)
        """
        try:
            from backend.models.user_model import Usuario
            from backend.models.file_model import Archivo
            from backend.models.event_model import Evento
            from backend.models.base import Base

            Base.metadata.drop_all(bind=self.engine)

            print("✅ Todas las tablas eliminadas correctamente")
            return True

        except Exception as e:
            print(f"❌ Error eliminando tablas: {e}")
            return False

    def database_exists(self):
        """
        Verifica si el archivo de base de datos existe

        Returns:
            bool: True si existe, False si no
        """
        return os.path.exists(self.db_path)

    def get_database_info(self):
        """
        Obtiene información sobre la base de datos

        Returns:
            dict: Información de la base de datos
        """
        return {
            "path": self.db_path,
            "exists": self.database_exists(),
            "size_mb": (
                round(os.path.getsize(self.db_path) / 1024 / 1024, 2)
                if self.database_exists()
                else 0
            ),
        }
