import os
import shutil
from backend.database.connection import DatabaseManager


class SystemService:
    """
    Servicio para operaciones del sistema FortiFile.

    Incluye:
    - RF-13: Reinicio completo del sistema
    - Gestión de estado del sistema
    - Operaciones de mantenimiento
    """

    def __init__(self):
        """Inicializa el servicio del sistema"""
        self.db_manager = DatabaseManager("fortifile.db")
        print("✅ SystemService inicializado")

    def reset_system(self, confirmation_text: str = None) -> dict:
        """
        RF-13: Reinicia completamente el sistema FortiFile

        Elimina:
        - Todos los usuarios
        - Todos los archivos cifrados
        - Todos los eventos
        - Clave de cifrado
        - Base de datos

        Args:
            confirmation_text (str): Texto de confirmación (debe ser "RESET FORTIFILE")

        Returns:
            dict: {"success": bool, "message": str}
        """
        # Validar confirmación
        if confirmation_text != "RESET FORTIFILE":
            return {
                "success": False,
                "message": "Confirmación incorrecta. Escriba exactamente: RESET FORTIFILE",
            }

        try:
            reset_items = []

            # 1. Eliminar base de datos
            if os.path.exists("fortifile.db"):
                os.remove("fortifile.db")
                reset_items.append("Base de datos principal")

            if os.path.exists("test_fortifile.db"):
                os.remove("test_fortifile.db")
                reset_items.append("Base de datos de prueba")

            # 2. Eliminar clave de cifrado
            if os.path.exists("fortifile.key"):
                os.remove("fortifile.key")
                reset_items.append("Clave de cifrado")

            # 3. Eliminar directorio de archivos seguros
            if os.path.exists("secure_files"):
                shutil.rmtree("secure_files")
                reset_items.append("Archivos cifrados")

            # 4. Limpiar archivos temporales
            temp_files = ["downloaded_document.txt", "test_document.txt"]
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    reset_items.append(f"Archivo temporal: {temp_file}")

            # 5. Recrear estructura básica
            self.db_manager.create_tables()

            if not os.path.exists("secure_files"):
                os.makedirs("secure_files")

            print("🔄 SISTEMA FORTIFILE REINICIADO COMPLETAMENTE")
            print(f"   Elementos eliminados: {len(reset_items)}")
            for item in reset_items:
                print(f"   ✅ {item}")

            return {
                "success": True,
                "message": f"Sistema reiniciado. {len(reset_items)} elementos eliminados y estructura recreada.",
                "reset_items": reset_items,
            }

        except Exception as e:
            return {"success": False, "message": f"Error al reiniciar sistema: {e}"}

    def get_system_status(self) -> dict:
        """
        Obtiene el estado actual del sistema

        Returns:
            dict: Estado del sistema
        """
        try:
            status = {
                "database_exists": os.path.exists("fortifile.db"),
                "encryption_key_exists": os.path.exists("fortifile.key"),
                "secure_files_dir_exists": os.path.exists("secure_files"),
                "database_size_mb": 0,
                "secure_files_count": 0,
                "secure_files_size_mb": 0,
            }

            # Tamaño de base de datos
            if status["database_exists"]:
                db_size = os.path.getsize("fortifile.db")
                status["database_size_mb"] = round(db_size / 1024 / 1024, 3)

            # Información de archivos seguros
            if status["secure_files_dir_exists"]:
                files = os.listdir("secure_files")
                status["secure_files_count"] = len(
                    [
                        f
                        for f in files
                        if os.path.isfile(os.path.join("secure_files", f))
                    ]
                )

                total_size = 0
                for file in files:
                    file_path = os.path.join("secure_files", file)
                    if os.path.isfile(file_path):
                        total_size += os.path.getsize(file_path)
                status["secure_files_size_mb"] = round(total_size / 1024 / 1024, 3)

            # Estado general
            status["system_initialized"] = all(
                [
                    status["database_exists"],
                    status["encryption_key_exists"],
                    status["secure_files_dir_exists"],
                ]
            )

            return {"success": True, "status": status}

        except Exception as e:
            return {
                "success": False,
                "message": f"Error obteniendo estado del sistema: {e}",
            }

    def backup_system(self, backup_path: str) -> dict:
        """
        Crea respaldo del sistema (sin incluir archivos por seguridad)

        Args:
            backup_path (str): Ruta donde crear el respaldo

        Returns:
            dict: {"success": bool, "message": str}
        """
        try:
            if not os.path.exists(backup_path):
                os.makedirs(backup_path)

            backup_items = []

            # Respaldar base de datos
            if os.path.exists("fortifile.db"):
                shutil.copy2(
                    "fortifile.db", os.path.join(backup_path, "fortifile_backup.db")
                )
                backup_items.append("Base de datos")

            # NOTA: NO respaldamos la clave de cifrado por seguridad
            # NOTA: NO respaldamos archivos cifrados por seguridad

            return {
                "success": True,
                "message": f"Respaldo creado en {backup_path}. Elementos: {', '.join(backup_items)}",
                "backup_items": backup_items,
            }

        except Exception as e:
            return {"success": False, "message": f"Error creando respaldo: {e}"}

    def verify_system_integrity(self) -> dict:
        """
        Verifica la integridad del sistema

        Returns:
            dict: Resultado de verificación
        """
        try:
            issues = []

            # Verificar archivos esenciales
            if not os.path.exists("fortifile.db"):
                issues.append("Base de datos principal no existe")

            if not os.path.exists("fortifile.key"):
                issues.append("Clave de cifrado no existe")

            if not os.path.exists("secure_files"):
                issues.append("Directorio de archivos seguros no existe")

            # Verificar consistencia base de datos vs archivos
            try:
                session = self.db_manager.get_session()
                from backend.models.file_model import Archivo

                db_files = session.query(Archivo).all()
                for db_file in db_files:
                    if not os.path.exists(db_file.ruta_archivo):
                        issues.append(
                            f"Archivo referenciado en BD no existe: {db_file.nombre_archivo}"
                        )

                session.close()
            except Exception as e:
                issues.append(f"Error verificando consistencia BD: {e}")

            integrity_ok = len(issues) == 0

            return {
                "success": True,
                "integrity_ok": integrity_ok,
                "issues": issues,
                "issues_count": len(issues),
            }

        except Exception as e:
            return {"success": False, "message": f"Error verificando integridad: {e}"}
