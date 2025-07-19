"""
Tests para la conexión y gestión de base de datos - Versión adaptada a pytest
"""

from backend.models.user_model import Usuario
from backend.database.connection import DatabaseManager
import os
import pytest
import tempfile
from unittest import mock
import sys

# Agregar el directorio del proyecto al path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)


class TestDatabase:
    """Test suite para la gestión de base de datos"""

    @pytest.fixture
    def temp_db_path(self):
        """Fixture para crear una base de datos temporal para tests"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            db_path = tmp.name
        yield db_path
        # Cleanup: eliminar el archivo después del test
        if os.path.exists(db_path):
            os.unlink(db_path)

    @pytest.fixture
    def db_manager(self, temp_db_path):
        """Fixture para crear un DatabaseManager con DB temporal"""
        return DatabaseManager(temp_db_path)

    def test_database_connection(self, db_manager, temp_db_path):
        """Test 1: Prueba que la conexión a la base de datos funciona"""
        print("🔧 Probando conexión a base de datos...")

        # Obtener información de la base de datos
        db_info = db_manager.get_database_info()

        # Verificaciones con assert (no return)
        assert db_info["path"] == temp_db_path
        assert isinstance(db_info["exists"], bool)
        print(f"   - Archivo: {db_info['path']}")
        print(f"   - Existe: {db_info['exists']}")

        # Crear las tablas
        tables_created = db_manager.create_tables()
        assert tables_created, "Las tablas deberían crearse exitosamente"
        print("✅ Tablas creadas exitosamente")

        # Probar obtener una sesión
        session = db_manager.get_session()
        assert session is not None, "Debería poder obtener una sesión de BD"
        session.close()
        print("✅ Sesión de base de datos obtenida correctamente")

        # Verificar información actualizada
        db_info_updated = db_manager.get_database_info()
        assert isinstance(db_info_updated["size_mb"], (int, float))
        print(f"   - Tamaño: {db_info_updated['size_mb']} MB")

    def test_database_operations(self, db_manager):
        """Test 2: Prueba operaciones básicas de base de datos"""
        print("🔧 Probando operaciones de base de datos...")

        # Crear las tablas primero
        assert db_manager.create_tables()

        session = db_manager.get_session()
        assert session is not None

        try:
            # Crear un usuario de prueba
            test_user = Usuario(username="test_db_user", password_hash="test_hash_123")

            # Agregar a la sesión y confirmar
            session.add(test_user)
            session.commit()
            print("✅ Usuario de prueba creado")

            # Verificar que se guardó correctamente
            saved_user = (
                session.query(Usuario).filter_by(username="test_db_user").first()
            )
            assert saved_user is not None, "El usuario debería existir en la BD"
            assert saved_user.username == "test_db_user"
            assert saved_user.password_hash == "test_hash_123"
            print("✅ Usuario recuperado correctamente")

            # Probar actualización
            saved_user.password_hash = "new_hash_456"
            session.commit()

            # Verificar actualización
            updated_user = (
                session.query(Usuario).filter_by(username="test_db_user").first()
            )
            assert updated_user.password_hash == "new_hash_456"
            print("✅ Usuario actualizado correctamente")

            # Probar eliminación
            session.delete(updated_user)
            session.commit()

            # Verificar eliminación
            deleted_user = (
                session.query(Usuario).filter_by(username="test_db_user").first()
            )
            assert deleted_user is None, "El usuario debería haber sido eliminado"
            print("✅ Usuario eliminado correctamente")

        finally:
            session.close()

    def test_database_error_handling(self, temp_db_path):
        """Test 3: Prueba manejo de errores de base de datos"""
        print("🔧 Probando manejo de errores...")

        # Test con archivo de BD inválido
        invalid_db_path = "/invalid/path/database.db"

        # El DatabaseManager se crea pero create_tables() debería fallar
        db_manager = DatabaseManager(invalid_db_path)

        # create_tables() debería retornar False para rutas inválidas
        result = db_manager.create_tables()
        assert (
            result == False
        ), "create_tables() debería retornar False para rutas inválidas"

        print("✅ Manejo de errores funcionando correctamente")

    def test_database_info_structure(self, db_manager):
        """Test 4: Verifica la estructura de información de BD"""
        db_info = db_manager.get_database_info()

        # Verificar que tiene las claves esperadas
        required_keys = ["path", "exists", "size_mb"]
        for key in required_keys:
            assert key in db_info, f"db_info debería tener la clave '{key}'"

        # Verificar tipos de datos
        assert isinstance(db_info["path"], str)
        assert isinstance(db_info["exists"], bool)
        assert isinstance(db_info["size_mb"], (int, float))

        print("✅ Estructura de información de BD válida")


# Mantener compatibilidad con ejecución directa
if __name__ == "__main__":
    pytest.main([__file__])
