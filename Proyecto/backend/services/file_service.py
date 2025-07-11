import os
import shutil
from datetime import datetime
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

from backend.models.file_model import Archivo
from backend.models.event_model import Evento
from backend.database.connection import DatabaseManager


class FileService:
    """
    Servicio para manejar todas las operaciones con archivos.
    
    Incluye:
    - RF-03: Carga de archivos
    - RF-04: Cifrado automático
    - RF-05: Visualización de archivos
    - RF-06: Descarga y descifrado
    - RF-07: Eliminación segura
    """
    
    def __init__(self, files_directory="secure_files"):
        """
        Inicializa el servicio de archivos
        
        Args:
            files_directory (str): Directorio donde se almacenan los archivos cifrados
        """
        self.db_manager = DatabaseManager("fortifile.db")
        self.files_directory = files_directory
        self.key_file = "fortifile.key"
        
        # Crear directorio de archivos si no existe
        if not os.path.exists(self.files_directory):
            os.makedirs(self.files_directory)
            print(f"✅ Directorio creado: {self.files_directory}")
        
        # Generar o cargar clave de cifrado
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
        
        print("✅ FileService inicializado")
        
    def _get_or_create_key(self) -> bytes:
        """
        Obtiene la clave de cifrado existente o crea una nueva
        
        Returns:
            bytes: Clave de cifrado
        """
        if os.path.exists(self.key_file):
            # Cargar clave existente
            with open(self.key_file, 'rb') as key_file:
                key = key_file.read()
                print("✅ Clave de cifrado cargada")
                return key
        else:
            # Generar nueva clave
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)
                print("✅ Nueva clave de cifrado generada")
                return key
    
    def upload_file(self, user_id: int, source_file_path: str, original_filename: str = None) -> dict:
        """
        RF-03 y RF-04: Carga y cifra un archivo automáticamente
        
        Args:
            user_id (int): ID del usuario propietario
            source_file_path (str): Ruta del archivo a subir
            original_filename (str): Nombre original (opcional)
            
        Returns:
            dict: {"success": bool, "message": str, "file_id": int}
        """
        if not os.path.exists(source_file_path):
            return {
                "success": False,
                "message": "El archivo fuente no existe",
                "file_id": None
            }
        
        # Determinar nombre original
        if not original_filename:
            original_filename = os.path.basename(source_file_path)
        
        session = self.db_manager.get_session()
        try:
            # Generar nombre único para archivo cifrado
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            encrypted_filename = f"user_{user_id}_{timestamp}_{original_filename}.enc"
            encrypted_path = os.path.join(self.files_directory, encrypted_filename)
            
            # Leer y cifrar archivo
            with open(source_file_path, 'rb') as original_file:
                file_data = original_file.read()
                encrypted_data = self.cipher.encrypt(file_data)
            
            # Guardar archivo cifrado
            with open(encrypted_path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)
            
            # Registrar en base de datos
            new_file = Archivo(
                nombre_archivo=original_filename,
                ruta_archivo=encrypted_path,
                usuario_id=user_id
            )
            
            session.add(new_file)
            session.commit()
            
            # Registrar evento
            self._log_event(session, user_id, f"Archivo subido y cifrado: {original_filename}")
            
            return {
                "success": True,
                "message": f"Archivo '{original_filename}' subido y cifrado correctamente",
                "file_id": new_file.id_archivo
            }
            
        except Exception as e:
            session.rollback()
            # Limpiar archivo si se creó
            if os.path.exists(encrypted_path):
                os.remove(encrypted_path)
            return {
                "success": False,
                "message": f"Error al subir archivo: {e}",
                "file_id": None
            }
        finally:
            session.close()
    
    def get_user_files(self, user_id: int) -> dict:
        """
        RF-05: Obtiene la lista de archivos del usuario
        
        Args:
            user_id (int): ID del usuario
            
        Returns:
            dict: {"success": bool, "files": list, "count": int}
        """
        session = self.db_manager.get_session()
        try:
            files = session.query(Archivo).filter(Archivo.usuario_id == user_id).all()
            
            file_list = []
            for file in files:
                file_info = {
                    "id": file.id_archivo,
                    "nombre": file.nombre_archivo,
                    "fecha_subida": file.fecha_subida,
                    "size_mb": self._get_file_size(file.ruta_archivo)
                }
                file_list.append(file_info)
            
            return {
                "success": True,
                "files": file_list,
                "count": len(file_list)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error obteniendo archivos: {e}",
                "files": [],
                "count": 0
            }
        finally:
            session.close()
    
    def download_file(self, user_id: int, file_id: int, output_path: str) -> dict:
        """
        RF-06: Descarga y descifra un archivo
        
        Args:
            user_id (int): ID del usuario
            file_id (int): ID del archivo
            output_path (str): Ruta donde guardar el archivo descifrado
            
        Returns:
            dict: {"success": bool, "message": str, "output_path": str}
        """
        session = self.db_manager.get_session()
        try:
            # Verificar que el archivo pertenece al usuario
            file = session.query(Archivo).filter(
                Archivo.id_archivo == file_id,
                Archivo.usuario_id == user_id
            ).first()
            
            if not file:
                return {
                    "success": False,
                    "message": "Archivo no encontrado o no pertenece al usuario",
                    "output_path": None
                }
            
            if not os.path.exists(file.ruta_archivo):
                return {
                    "success": False,
                    "message": "El archivo cifrado no existe en el sistema",
                    "output_path": None
                }
            
            # Leer y descifrar archivo
            with open(file.ruta_archivo, 'rb') as encrypted_file:
                encrypted_data = encrypted_file.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Guardar archivo descifrado
            with open(output_path, 'wb') as output_file:
                output_file.write(decrypted_data)
            
            # Registrar evento
            self._log_event(session, user_id, f"Archivo descargado: {file.nombre_archivo}")
            
            return {
                "success": True,
                "message": f"Archivo '{file.nombre_archivo}' descargado correctamente",
                "output_path": output_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error al descargar archivo: {e}",
                "output_path": None
            }
        finally:
            session.close()
    
    def delete_file(self, user_id: int, file_id: int) -> dict:
        """
        RF-07: Elimina un archivo de forma segura
        
        Args:
            user_id (int): ID del usuario
            file_id (int): ID del archivo
            
        Returns:
            dict: {"success": bool, "message": str}
        """
        session = self.db_manager.get_session()
        try:
            # Verificar que el archivo pertenece al usuario
            file = session.query(Archivo).filter(
                Archivo.id_archivo == file_id,
                Archivo.usuario_id == user_id
            ).first()
            
            if not file:
                return {
                    "success": False,
                    "message": "Archivo no encontrado o no pertenece al usuario"
                }
            
            filename = file.nombre_archivo
            file_path = file.ruta_archivo
            
            # Eliminar archivo físico
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Eliminar registro de base de datos
            session.delete(file)
            session.commit()
            
            # Registrar evento
            self._log_event(session, user_id, f"Archivo eliminado: {filename}")
            
            return {
                "success": True,
                "message": f"Archivo '{filename}' eliminado correctamente"
            }
            
        except Exception as e:
            session.rollback()
            return {
                "success": False,
                "message": f"Error al eliminar archivo: {e}"
            }
        finally:
            session.close()
    
    def _get_file_size(self, file_path: str) -> float:
        """
        Obtiene el tamaño de un archivo en MB
        
        Args:
            file_path (str): Ruta del archivo
            
        Returns:
            float: Tamaño en MB
        """
        try:
            if os.path.exists(file_path):
                size_bytes = os.path.getsize(file_path)
                return round(size_bytes / 1024 / 1024, 2)
            return 0.0
        except:
            return 0.0
    
    def _log_event(self, session: Session, user_id: int, description: str):
        """
        Registra un evento del sistema
        
        Args:
            session (Session): Sesión activa de base de datos
            user_id (int): ID del usuario
            description (str): Descripción del evento
        """
        try:
            event = Evento(
                descripcion=description,
                usuario_id=user_id,
                fecha_evento=datetime.utcnow()
            )
            session.add(event)
            session.commit()
        except Exception as e:
            print(f"❌ Error registrando evento: {e}")
    
    def get_storage_info(self) -> dict:
        """
        Obtiene información del almacenamiento
        
        Returns:
            dict: Información del almacenamiento
        """
        try:
            total_files = 0
            total_size = 0
            
            if os.path.exists(self.files_directory):
                for filename in os.listdir(self.files_directory):
                    file_path = os.path.join(self.files_directory, filename)
                    if os.path.isfile(file_path):
                        total_files += 1
                        total_size += os.path.getsize(file_path)
            
            return {
                "success": True,
                "total_files": total_files,
                "total_size_mb": round(total_size / 1024 / 1024, 2),
                "storage_directory": self.files_directory
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error obteniendo info de almacenamiento: {e}"
            }
