import bcrypt
from sqlalchemy.orm import Session
from datetime import datetime

from backend.models.user_model import Usuario
from backend.models.event_model import Evento
from backend.database.connection import DatabaseManager


class UserService:
    """
    Servicio para manejar todas las operaciones relacionadas con usuarios.
    
    Incluye:
    - RF-01: Registro de usuario único
    - RF-02: Inicio de sesión
    - RF-04: Bloqueo por intentos fallidos
    - RF-08: Cambio de contraseña  
    - RF-10: Eliminación de cuenta
    - RF-11: Registro de eventos
    - RF-12: Verificación de usuario único
    """
    
    def __init__(self):
        """Inicializa el servicio de usuario"""
        self.db_manager = DatabaseManager("fortifile.db")
        self.max_failed_attempts = 3  # RF-04: Máximo intentos fallidos
        self.failed_attempts = 0      # Contador de intentos fallidos
        self.account_locked = False   # Estado de cuenta bloqueada
        print("✅ UserService inicializado")
        
    def user_exists(self) -> bool:
        """
        RF-12: Verifica si ya existe un usuario registrado
        FortiFile solo permite UN usuario por seguridad
        
        Returns:
            bool: True si existe un usuario, False si no
        """
        session = self.db_manager.get_session()
        try:
            user_count = session.query(Usuario).count()
            return user_count > 0
        except Exception as e:
            print(f"❌ Error verificando usuario: {e}")
            return False
        finally:
            session.close()
    
    def register_user(self, username: str, password: str) -> dict:
        """
        RF-01: Registro inicial del usuario (solo UNO permitido)
        
        Args:
            username (str): Nombre de usuario
            password (str): Contraseña en texto plano
            
        Returns:
            dict: {"success": bool, "message": str, "user_id": int}
        """
        # Verificar si ya existe un usuario
        if self.user_exists():
            return {
                "success": False, 
                "message": "Ya existe un usuario registrado. FortiFile solo permite un usuario por seguridad.",
                "user_id": None
            }
            
        session = self.db_manager.get_session()
        try:
            # Validar contraseña
            validation = self._validate_password(password)
            if not validation["valid"]:
                return {
                    "success": False,
                    "message": f"Contraseña no válida: {validation['message']}",
                    "user_id": None
                }
            
            # RNF-02: Hash seguro de contraseña con bcrypt
            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password_bytes, salt)
            
            # Crear nuevo usuario
            new_user = Usuario(
                username=username,
                password_hash=password_hash.decode('utf-8')
            )
            
            session.add(new_user)
            session.commit()
            
            # RF-11: Registrar evento
            self._log_event(session, new_user.id_usuario, "Usuario registrado exitosamente")
            
            return {
                "success": True,
                "message": "Usuario registrado correctamente",
                "user_id": new_user.id_usuario
            }
            
        except Exception as e:
            session.rollback()
            return {
                "success": False,
                "message": f"Error al registrar usuario: {e}",
                "user_id": None
            }
        finally:
            session.close()
    
    def authenticate_user(self, username: str, password: str) -> dict:
        """
        RF-02 y RF-04: Inicio de sesión con validación y control de intentos fallidos
        
        Args:
            username (str): Nombre de usuario
            password (str): Contraseña en texto plano
            
        Returns:
            dict: {"success": bool, "message": str, "user_id": int, "username": str, "locked": bool}
        """
        # RF-04: Verificar si la cuenta está bloqueada
        if self.account_locked:
            return {
                "success": False,
                "message": f"Cuenta bloqueada por {self.max_failed_attempts} intentos fallidos. Reinicie la aplicación.",
                "user_id": None,
                "username": None,
                "locked": True
            }
        
        session = self.db_manager.get_session()
        try:
            # Buscar usuario por nombre
            user = session.query(Usuario).filter(Usuario.username == username).first()
            
            if not user:
                self._handle_failed_attempt(session, None, "Intento de login con usuario inexistente")
                return {
                    "success": False,
                    "message": "Usuario no encontrado",
                    "user_id": None,
                    "username": None,
                    "locked": self.account_locked
                }
            
            # Verificar contraseña
            password_bytes = password.encode('utf-8')
            stored_hash = user.password_hash.encode('utf-8')
            
            if bcrypt.checkpw(password_bytes, stored_hash):
                # Contraseña correcta - resetear contador
                self.failed_attempts = 0
                self._log_event(session, user.id_usuario, "Inicio de sesión exitoso")
                return {
                    "success": True,
                    "message": "Inicio de sesión exitoso",
                    "user_id": user.id_usuario,
                    "username": user.username,
                    "locked": False
                }
            else:
                # Contraseña incorrecta
                self._handle_failed_attempt(session, user.id_usuario, "Intento de inicio de sesión fallido")
                return {
                    "success": False,
                    "message": f"Contraseña incorrecta. Intentos restantes: {self.max_failed_attempts - self.failed_attempts}",
                    "user_id": None,
                    "username": None,
                    "locked": self.account_locked
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error en autenticación: {e}",
                "user_id": None,
                "username": None,
                "locked": False
            }
        finally:
            session.close()
    
    def _handle_failed_attempt(self, session: Session, user_id: int, description: str):
        """
        RF-04: Maneja intentos fallidos de inicio de sesión
        
        Args:
            session (Session): Sesión activa
            user_id (int): ID del usuario (puede ser None)
            description (str): Descripción del evento
        """
        self.failed_attempts += 1
        
        if user_id:
            self._log_event(session, user_id, f"{description} (Intento {self.failed_attempts}/{self.max_failed_attempts})")
        
        if self.failed_attempts >= self.max_failed_attempts:
            self.account_locked = True
            if user_id:
                self._log_event(session, user_id, "Cuenta bloqueada por intentos fallidos")
            print(f"⚠️  CUENTA BLOQUEADA - {self.max_failed_attempts} intentos fallidos")
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> dict:
        """
        RF-08: Cambio de contraseña con validación
        
        Args:
            user_id (int): ID del usuario
            old_password (str): Contraseña actual
            new_password (str): Nueva contraseña
            
        Returns:
            dict: {"success": bool, "message": str}
        """
        if self.account_locked:
            return {
                "success": False,
                "message": "No se puede cambiar contraseña con cuenta bloqueada"
            }
        
        session = self.db_manager.get_session()
        try:
            user = session.query(Usuario).filter(Usuario.id_usuario == user_id).first()
            
            if not user:
                return {
                    "success": False,
                    "message": "Usuario no encontrado"
                }
            
            # Verificar contraseña actual
            old_password_bytes = old_password.encode('utf-8')
            stored_hash = user.password_hash.encode('utf-8')
            
            if not bcrypt.checkpw(old_password_bytes, stored_hash):
                self._log_event(session, user_id, "Intento de cambio de contraseña fallido - contraseña actual incorrecta")
                return {
                    "success": False,
                    "message": "La contraseña actual es incorrecta"
                }
            
            # Validar nueva contraseña
            validation = self._validate_password(new_password)
            if not validation["valid"]:
                return {
                    "success": False,
                    "message": f"Nueva contraseña no válida: {validation['message']}"
                }
            
            # Cambiar contraseña
            new_password_bytes = new_password.encode('utf-8')
            salt = bcrypt.gensalt()
            new_password_hash = bcrypt.hashpw(new_password_bytes, salt)
            
            user.password_hash = new_password_hash.decode('utf-8')
            session.commit()
            
            self._log_event(session, user_id, "Contraseña cambiada exitosamente")
            
            return {
                "success": True,
                "message": "Contraseña cambiada correctamente"
            }
            
        except Exception as e:
            session.rollback()
            return {
                "success": False,
                "message": f"Error al cambiar contraseña: {e}"
            }
        finally:
            session.close()
    
    def delete_account(self, user_id: int, password: str) -> dict:
        """
        RF-10: Eliminación de cuenta con confirmación de contraseña
        
        Args:
            user_id (int): ID del usuario
            password (str): Contraseña para confirmar
            
        Returns:
            dict: {"success": bool, "message": str}
        """
        session = self.db_manager.get_session()
        try:
            user = session.query(Usuario).filter(Usuario.id_usuario == user_id).first()
            
            if not user:
                return {
                    "success": False,
                    "message": "Usuario no encontrado"
                }
            
            # Verificar contraseña
            password_bytes = password.encode('utf-8')
            stored_hash = user.password_hash.encode('utf-8')
            
            if not bcrypt.checkpw(password_bytes, stored_hash):
                self._log_event(session, user_id, "Intento de eliminación de cuenta fallido - contraseña incorrecta")
                return {
                    "success": False,
                    "message": "Contraseña incorrecta"
                }
            
            username = user.username
            
            # Eliminar usuario (archivos y eventos se eliminan por cascade)
            session.delete(user)
            session.commit()
            
            print(f"✅ Cuenta '{username}' eliminada correctamente")
            
            return {
                "success": True,
                "message": f"Cuenta '{username}' eliminada correctamente"
            }
            
        except Exception as e:
            session.rollback()
            return {
                "success": False,
                "message": f"Error al eliminar cuenta: {e}"
            }
        finally:
            session.close()
    
    def _validate_password(self, password: str) -> dict:
        """
        RNF-02: Validación de contraseña segura
        
        Args:
            password (str): Contraseña a validar
            
        Returns:
            dict: {"valid": bool, "message": str}
        """
        if len(password) < 8:
            return {"valid": False, "message": "Debe tener al menos 8 caracteres"}
        
        if not any(c.isupper() for c in password):
            return {"valid": False, "message": "Debe contener al menos una mayúscula"}
        
        if not any(c.islower() for c in password):
            return {"valid": False, "message": "Debe contener al menos una minúscula"}
        
        if not any(c.isdigit() for c in password):
            return {"valid": False, "message": "Debe contener al menos un número"}
        
        return {"valid": True, "message": "Contraseña válida"}
    
    def _log_event(self, session: Session, user_id: int, description: str):
        """
        RF-11: Registra un evento del sistema
        
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
            
    def get_user_info(self, user_id: int) -> dict:
        """
        Obtiene información básica del usuario
        
        Args:
            user_id (int): ID del usuario
            
        Returns:
            dict: Información del usuario
        """
        session = self.db_manager.get_session()
        try:
            user = session.query(Usuario).filter(Usuario.id_usuario == user_id).first()
            
            if user:
                return {
                    "success": True,
                    "user_id": user.id_usuario,
                    "username": user.username,
                    "fecha_creacion": user.fecha_creacion
                }
            else:
                return {"success": False, "message": "Usuario no encontrado"}
                
        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}
        finally:
            session.close()
    
    def get_user_events(self, user_id: int, limit: int = 10) -> dict:
        """
        RF-11: Obtiene eventos del usuario
        
        Args:
            user_id (int): ID del usuario
            limit (int): Número máximo de eventos a retornar
            
        Returns:
            dict: {"success": bool, "events": list}
        """
        session = self.db_manager.get_session()
        try:
            events = session.query(Evento)\
                .filter(Evento.usuario_id == user_id)\
                .order_by(Evento.fecha_evento.desc())\
                .limit(limit).all()
            
            event_list = []
            for event in events:
                event_list.append({
                    "id": event.id_evento,
                    "descripcion": event.descripcion,
                    "fecha": event.fecha_evento
                })
            
            return {
                "success": True,
                "events": event_list,
                "count": len(event_list)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error obteniendo eventos: {e}",
                "events": []
            }
        finally:
            session.close()
    
    def reset_failed_attempts(self):
        """
        RF-04: Resetea contador de intentos fallidos
        """
        self.failed_attempts = 0
        self.account_locked = False
        print("✅ Contador de intentos fallidos reseteado")
    
    def get_security_status(self) -> dict:
        """
        Obtiene estado de seguridad actual
        
        Returns:
            dict: Estado de seguridad
        """
        return {
            "account_locked": self.account_locked,
            "failed_attempts": self.failed_attempts,
            "max_attempts": self.max_failed_attempts,
            "remaining_attempts": max(0, self.max_failed_attempts - self.failed_attempts)
        }
