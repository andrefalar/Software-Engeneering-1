"""
Tests para el servicio de archivos - Versión adaptada a pytest
"""

from backend.services.user_service import UserService
from backend.services.file_service import FileService
import os
import pytest
import tempfile
import shutil
from unittest import mock
import sys

# Agregar el directorio del proyecto al path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)


class TestFileService:
    """Test suite para el servicio de archivos"""

    @pytest.fixture(scope="function")
    def temp_dir(self):
        """Fixture para crear directorio temporal para archivos de prueba"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup: eliminar directorio y contenidos
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    @pytest.fixture
    def services(self):
        """Fixture para inicializar servicios"""
        user_service = UserService()
        file_service = FileService()

        # Crear tablas
        user_service.db_manager.create_tables()

        return {"user_service": user_service, "file_service": file_service}

    @pytest.fixture
    def test_user(self, services):
        """Fixture para crear un usuario de prueba"""
        user_service = services["user_service"]

        # Intentar registrar usuario
        user_result = user_service.register_user("fileuser", "FilePassword123")

        if not user_result["success"]:
            # Si usuario ya existe, autenticar
            auth_result = user_service.authenticate_user("fileuser", "FilePassword123")
            user_id = auth_result["user_id"] if auth_result["success"] else 1
        else:
            user_id = user_result["user_id"]

        return user_id

    @pytest.fixture
    def test_file(self, temp_dir):
        """Fixture para crear archivo de prueba"""
        test_file_path = os.path.join(temp_dir, "test_file_service.txt")
        test_content = "Contenido de prueba para FileService\n¡Datos confidenciales!"

        with open(test_file_path, "w") as f:
            f.write(test_content)

        return {"path": test_file_path, "content": test_content}

    def test_file_service_upload_and_download(
        self, services, test_user, test_file, temp_dir
    ):
        """Test 1: Prueba subida y descarga de archivos (RF-03, RF-04, RF-06)"""
        print("🔧 Probando subida y descarga de archivos...")

        file_service = services["file_service"]
        user_id = test_user

        # 1. Subir archivo (RF-03 y RF-04)
        upload_result = file_service.upload_file(
            user_id, test_file["path"], "documento_prueba.txt"
        )

        assert (
            upload_result["success"]
        ), "La subida del archivo debería ser exitosa"
        assert "file_id" in upload_result, "El resultado debería incluir file_id"

        file_id = upload_result["file_id"]
        print(f"   ✅ Archivo subido con ID: {file_id}")

        # 2. Descargar archivo (RF-06)
        download_path = os.path.join(temp_dir, "downloaded_test_file.txt")
        download_result = file_service.download_file(user_id, file_id, download_path)

        assert download_result["success"], "La descarga debería ser exitosa"
        assert os.path.exists(download_path), "El archivo descargado debería existir"
        print("   ✅ Archivo descargado exitosamente")

        # 3. Verificar contenido
        with open(download_path, "r") as f:
            downloaded_content = f.read()

        assert (
            downloaded_content == test_file["content"]
        ), "El contenido descargado debería coincidir con el original"
        print("   ✅ Contenido verificado correctamente")

        # 4. Limpiar - eliminar archivo
        delete_result = file_service.delete_file(user_id, file_id)
        assert delete_result["success"], "La eliminación debería ser exitosa"
        print("   ✅ Archivo eliminado exitosamente")

    def test_file_service_list_files(self, services, test_user, test_file):
        """Test 2: Prueba listado de archivos (RF-05)"""
        print("🔧 Probando listado de archivos...")

        file_service = services["file_service"]
        user_id = test_user

        # Subir archivo
        upload_result = file_service.upload_file(
            user_id, test_file["path"], "documento_listado.txt"
        )
        assert upload_result["success"]
        file_id = upload_result["file_id"]

        # Listar archivos del usuario
        files_result = file_service.get_user_files(user_id)

        assert files_result["success"], "El listado debería ser exitoso"
        assert files_result["count"] >= 1, "Debería haber al menos 1 archivo"
        assert (
            "files" in files_result
        ), "El resultado debería incluir la lista de archivos"

        print(f"   ✅ Archivos listados: {files_result['count']} archivo(s)")

        # Limpiar
        file_service.delete_file(user_id, file_id)

    def test_file_service_storage_info(self, services):
        """Test 3: Prueba información de almacenamiento"""
        print("🔧 Probando información de almacenamiento...")

        file_service = services["file_service"]

        storage_info = file_service.get_storage_info()

        assert (
            storage_info["success"]
        ), "La consulta de almacenamiento debería ser exitosa"
        assert (
            "total_files" in storage_info
        ), "Debería incluir información de total de archivos"
        assert isinstance(
            storage_info["total_files"], int
        ), "total_files debería ser un entero"

        print(f"   ✅ Almacenamiento: {storage_info['total_files']} archivos")

    def test_file_service_security_access_control(self, services, test_file, temp_dir):
        """Test 4: Prueba control de acceso y seguridad"""
        print("🔧 Probando seguridad y control de acceso...")

        user_service = services["user_service"]
        file_service = services["file_service"]

        # Crear usuario para la prueba
        user1_result = user_service.register_user("securityuser1", "Password123")
        user1_id = user1_result["user_id"] if user1_result["success"] else 1

        # Subir archivo como usuario 1
        upload_result = file_service.upload_file(
            user1_id, test_file["path"], "archivo_privado.txt"
        )
        assert upload_result["success"]
        file_id = upload_result["file_id"]

        # Verificar que usuario 1 puede ver sus archivos
        files_user1 = file_service.get_user_files(user1_id)
        assert files_user1["success"]
        assert files_user1["count"] >= 1, "Usuario 1 debería ver sus archivos"
        print("   ✅ Usuario puede ver sus propios archivos")

        # Simular usuario diferente intentando acceder
        fake_user_id = 999

        # Intentar descargar archivo de otro usuario (debe fallar)
        hack_path = os.path.join(temp_dir, "hack_attempt.txt")
        download_result = file_service.download_file(fake_user_id, file_id, hack_path)
        assert (
            download_result["success"] == False
        ), "Acceso de otro usuario debería ser denegado"
        print("   ✅ Acceso denegado correctamente a usuario no autorizado")

        # Intentar eliminar archivo de otro usuario (debe fallar)
        delete_result = file_service.delete_file(fake_user_id, file_id)
        assert (
            delete_result["success"] == False
        ), "Eliminación por otro usuario debería ser denegada"
        print("   ✅ Eliminación denegada correctamente a usuario no autorizado")

        # Usuario correcto puede eliminar
        delete_result = file_service.delete_file(user1_id, file_id)
        assert (
            delete_result["success"]
        ), "Usuario propietario debería poder eliminar"
        print("   ✅ Usuario propietario puede eliminar correctamente")

    def test_file_service_encryption_verification(
        self, services, test_user, test_file, temp_dir
    ):
        """Test 5: Prueba que los archivos se cifran correctamente"""
        print("🔧 Probando cifrado de archivos...")

        file_service = services["file_service"]
        user_id = test_user

        # Subir archivo
        upload_result = file_service.upload_file(
            user_id, test_file["path"], "archivo_cifrado.txt"
        )
        assert upload_result["success"]
        file_id = upload_result["file_id"]

        # Verificar que existe el archivo cifrado en secure_files
        secure_files_dir = os.path.join(project_root, "secure_files")

        if os.path.exists(secure_files_dir):
            # Buscar archivos .enc del usuario
            encrypted_files = [
                f
                for f in os.listdir(secure_files_dir)
                if f.startswith(f"user_{user_id}_") and f.endswith(".enc")
            ]

            assert (
                len(encrypted_files) >= 1
            ), "Debería haber al menos un archivo cifrado"

            # Verificar que el archivo cifrado no contiene el texto original
            encrypted_file_path = os.path.join(secure_files_dir, encrypted_files[0])

            with open(encrypted_file_path, "rb") as f:
                encrypted_content = f.read()

            # El contenido cifrado no debería contener el texto original
            original_text = test_file["content"].encode()
            assert (
                original_text not in encrypted_content
            ), "El archivo cifrado no debería contener texto plano"

            print("   ✅ Archivo correctamente cifrado en disco")

        # Limpiar
        file_service.delete_file(user_id, file_id)

    def test_file_service_invalid_operations(self, services, test_user):
        """Test 6: Prueba manejo de operaciones inválidas"""
        print("🔧 Probando manejo de operaciones inválidas...")

        file_service = services["file_service"]
        user_id = test_user

        # Intentar descargar archivo inexistente
        fake_file_id = 99999
        download_result = file_service.download_file(
            user_id, fake_file_id, "nonexistent.txt"
        )
        assert (
            download_result["success"] == False
        ), "Descarga de archivo inexistente debería fallar"

        # Intentar eliminar archivo inexistente
        delete_result = file_service.delete_file(user_id, fake_file_id)
        assert (
            delete_result["success"] == False
        ), "Eliminación de archivo inexistente debería fallar"

        # Intentar subir archivo inexistente
        upload_result = file_service.upload_file(
            user_id, "nonexistent_file.txt", "test.txt"
        )
        assert (
            upload_result["success"] == False
        ), "Subida de archivo inexistente debería fallar"

        print("   ✅ Operaciones inválidas manejadas correctamente")


# Mantener compatibilidad con ejecución directa
if __name__ == "__main__":
    pytest.main([__file__])
