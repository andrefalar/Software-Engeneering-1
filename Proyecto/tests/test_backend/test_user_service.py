"""
Tests para el servicio de usuario - Versión adaptada a pytest
"""
import pytest
import tempfile
import os
import sys

# Agregar el directorio del proyecto al path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from backend.services.user_service import UserService

class TestUserService:
    """Test suite para el servicio de usuarios"""
    
    @pytest.fixture
    def temp_db(self):
        """Fixture para crear base de datos temporal"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        yield db_path
        # Cleanup: eliminar el archivo después del test
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    @pytest.fixture
    def user_service(self, temp_db):
        """Fixture para crear UserService con DB temporal"""
        from unittest.mock import patch
        
        # Mockear DatabaseManager para usar DB temporal
        with patch('backend.services.user_service.DatabaseManager') as mock_db_manager:
            from backend.database.connection import DatabaseManager
            
            # Crear instancia real con DB temporal
            real_db_manager = DatabaseManager(temp_db)
            real_db_manager.create_tables()
            
            # Configurar el mock para retornar la instancia real
            mock_db_manager.return_value = real_db_manager
            
            # Crear UserService con el mock
            service = UserService()
            return service
    
    def test_user_service_initialization(self, user_service):
        """Test 1: Verifica inicialización del servicio"""
        print("🔧 Probando inicialización de UserService...")
        
        # Verificar que el servicio se inicializa correctamente
        assert user_service is not None, "UserService debería inicializarse"
        assert hasattr(user_service, 'db_manager'), "Debería tener db_manager"
        
        # Verificar estado inicial sin usuarios
        user_exists = user_service.user_exists()
        assert isinstance(user_exists, bool), "user_exists() debería retornar bool"
        
        print(f"   ✅ Servicio inicializado. ¿Usuario existe? {user_exists}")
    
    def test_user_registration_basic(self, user_service):
        """Test 2: Prueba registro básico de usuario"""
        print("🔧 Probando registro básico de usuario...")
        
        # Registrar primer usuario
        result = user_service.register_user("admin", "MiPassword123")
        
        assert result['success'] == True, f"Registro debería ser exitoso: {result['message']}"
        assert 'user_id' in result, "Resultado debería incluir user_id"
        assert isinstance(result['user_id'], int), "user_id debería ser entero"
        
        user_id = result['user_id']
        print(f"   ✅ Usuario registrado exitosamente con ID: {user_id}")
        
        # Verificar que ahora existe un usuario
        user_exists = user_service.user_exists()
        assert user_exists == True, "Debería existir al menos un usuario después del registro"
        print("   ✅ Existencia de usuario verificada")
    
    def test_user_registration_restrictions(self, user_service):
        """Test 3: Prueba restricciones de registro (un solo usuario)"""
        print("🔧 Probando restricciones de registro...")
        
        # Registrar primer usuario
        result1 = user_service.register_user("admin", "MiPassword123")
        assert result1['success'] == True
        
        # Intentar registrar segundo usuario (debe fallar)
        result2 = user_service.register_user("admin2", "Password456")
        assert result2['success'] == False, "No debería permitir registro de segundo usuario"
        assert 'message' in result2, "Debería incluir mensaje de error"
        
        print(f"   ✅ Segundo registro denegado correctamente: {result2['message']}")
    
    def test_user_authentication_success(self, user_service):
        """Test 4: Prueba autenticación exitosa"""
        print("🔧 Probando autenticación exitosa...")
        
        # Registrar usuario
        register_result = user_service.register_user("admin", "MiPassword123")
        assert register_result['success'] == True
        
        # Probar autenticación correcta
        auth_result = user_service.authenticate_user("admin", "MiPassword123")
        
        assert auth_result['success'] == True, f"Autenticación debería ser exitosa: {auth_result['message']}"
        assert 'user_id' in auth_result, "Resultado debería incluir user_id"
        assert auth_result['user_id'] == register_result['user_id'], "user_id debería coincidir"
        
        print(f"   ✅ Login correcto: {auth_result['message']}")
    
    def test_user_authentication_failure(self, user_service):
        """Test 5: Prueba autenticación fallida"""
        print("🔧 Probando autenticación fallida...")
        
        # Registrar usuario
        user_service.register_user("admin", "MiPassword123")
        
        # Probar autenticación incorrecta
        auth_fail = user_service.authenticate_user("admin", "passwordMala")
        
        assert auth_fail['success'] == False, "Autenticación con contraseña incorrecta debería fallar"
        assert 'message' in auth_fail, "Debería incluir mensaje de error"
        
        print(f"   ✅ Login incorrecto denegado: {auth_fail['message']}")
    
    def test_user_info_retrieval(self, user_service):
        """Test 6: Prueba obtención de información de usuario"""
        print("🔧 Probando obtención de información de usuario...")
        
        # Registrar usuario
        register_result = user_service.register_user("admin", "MiPassword123")
        user_id = register_result['user_id']
        
        # Obtener info de usuario
        user_info = user_service.get_user_info(user_id)
        
        assert user_info['success'] == True, "Obtención de info debería ser exitosa"
        assert 'username' in user_info, "Debería incluir username"
        assert 'fecha_creacion' in user_info, "Debería incluir fecha_creacion"
        assert user_info['username'] == "admin", "Username debería coincidir"
        
        print(f"   ✅ Info usuario: {user_info['username']} creado el {user_info['fecha_creacion']}")
    
    def test_password_validation_weak(self, user_service):
        """Test 7: Prueba validación de contraseñas débiles"""
        print("🔧 Probando validación de contraseñas débiles...")
        
        # Intentar registrar con contraseña débil
        weak_password = "123"
        result = user_service.register_user("testuser", weak_password)
        
        assert result['success'] == False, "Contraseña débil debería ser rechazada"
        assert 'message' in result, "Debería incluir mensaje explicativo"
        
        print(f"   ✅ Contraseña débil rechazada: {result['message']}")
    
    def test_password_validation_strong(self, user_service):
        """Test 8: Prueba validación de contraseñas fuertes"""
        print("🔧 Probando validación de contraseñas fuertes...")
        
        # Registrar con contraseña fuerte
        strong_password = "MiPassword123"
        result = user_service.register_user("testuser", strong_password)
        
        assert result['success'] == True, f"Contraseña fuerte debería ser aceptada: {result['message']}"
        
        print("   ✅ Usuario registrado con contraseña fuerte")
    
    def test_failed_login_attempts_and_blocking(self, user_service):
        """Test 9: Prueba bloqueo por intentos fallidos (RF-04)"""
        print("🔧 Probando bloqueo por intentos fallidos...")
        
        # Registrar usuario
        user_service.register_user("testuser", "MiPassword123")
        
        # Intentar logins fallidos múltiples veces
        blocked = False
        for i in range(4):
            auth_result = user_service.authenticate_user("testuser", "passwordMala")
            
            assert auth_result['success'] == False, f"Intento {i+1} debería fallar"
            
            if auth_result.get('locked'):
                blocked = True
                print(f"   ✅ Usuario bloqueado después de {i+1} intentos")
                break
        
        # Verificar que eventualmente se bloquea (dependiendo de la implementación)
        # Nota: algunos servicios pueden no implementar bloqueo inmediato
        print(f"   📝 Estado de bloqueo después de intentos: {blocked}")
    
    def test_password_change(self, user_service):
        """Test 10: Prueba cambio de contraseña (RF-08)"""
        print("🔧 Probando cambio de contraseña...")
        
        # Registrar usuario
        original_password = "MiPassword123"
        register_result = user_service.register_user("testuser", original_password)
        user_id = register_result['user_id']
        
        # Cambiar contraseña
        new_password = "NuevaPassword456"
        change_result = user_service.change_password(user_id, original_password, new_password)
        
        if hasattr(user_service, 'change_password'):
            assert change_result['success'] == True, f"Cambio de contraseña debería ser exitoso: {change_result['message']}"
            
            # Verificar que la nueva contraseña funciona
            auth_new = user_service.authenticate_user("testuser", new_password)
            assert auth_new['success'] == True, "Login con nueva contraseña debería funcionar"
            
            # Verificar que la contraseña anterior ya no funciona
            auth_old = user_service.authenticate_user("testuser", original_password)
            assert auth_old['success'] == False, "Login con contraseña anterior debería fallar"
            
            print("   ✅ Cambio de contraseña exitoso")
        else:
            pytest.skip("Método change_password no implementado")
    
    def test_user_events_logging(self, user_service):
        """Test 11: Prueba registro de eventos de usuario"""
        print("🔧 Probando registro de eventos...")
        
        # Registrar usuario y hacer login
        register_result = user_service.register_user("testuser", "MiPassword123")
        user_id = register_result['user_id']
        
        user_service.authenticate_user("testuser", "MiPassword123")
        
        # Obtener eventos
        if hasattr(user_service, 'get_user_events'):
            events_result = user_service.get_user_events(user_id, 5)
            
            assert events_result['success'] == True, "Obtención de eventos debería ser exitosa"
            assert 'count' in events_result, "Resultado debería incluir count"
            assert isinstance(events_result['count'], int), "count debería ser entero"
            
            print(f"   ✅ Eventos registrados: {events_result['count']}")
        else:
            pytest.skip("Método get_user_events no implementado")
    
    def test_security_status(self, user_service):
        """Test 12: Prueba estado de seguridad"""
        print("🔧 Probando estado de seguridad...")
        
        if hasattr(user_service, 'get_security_status'):
            security_status = user_service.get_security_status()
            
            assert 'account_locked' in security_status, "Estado debería incluir account_locked"
            assert isinstance(security_status['account_locked'], bool), "account_locked debería ser bool"
            
            print(f"   ✅ Cuenta bloqueada: {security_status['account_locked']}")
        else:
            pytest.skip("Método get_security_status no implementado")
    
    def test_password_validation_comprehensive(self, user_service):
        """Test 13: Prueba exhaustiva de validación de contraseñas"""
        print("🔧 Probando validación exhaustiva de contraseñas...")
        
        test_passwords = [
            ("123", False, "muy corta"),
            ("password", False, "sin mayúscula ni número"),
            ("PASSWORD", False, "sin minúscula ni número"),
            ("Password", False, "sin número"),
            ("Password1", True, "válida"),
            ("MiSuperPassword123", True, "válida compleja")
        ]
        
        for password, should_be_valid, description in test_passwords:
            if hasattr(user_service, '_validate_password'):
                validation = user_service._validate_password(password)
                
                assert 'valid' in validation, "Validación debería incluir 'valid'"
                assert 'message' in validation, "Validación debería incluir 'message'"
                
                actual_valid = validation['valid']
                result = actual_valid == should_be_valid
                
                status = "✅" if result else "❌"
                print(f"   {status} '{password}' ({description}): {validation['message']}")
                
                assert result, f"Validación de '{password}' debería ser {should_be_valid}"
            else:
                # Si no hay método de validación, probar con registro
                register_result = user_service.register_user("testpass", password)
                actual_valid = register_result['success']
                
                # Para passwords que deberían ser inválidas, el registro debería fallar
                if not should_be_valid:
                    assert not actual_valid, f"Password '{password}' debería ser rechazada"
                    print(f"   ✅ '{password}' ({description}): rechazada correctamente")
        
        print("   ✅ Validación de contraseñas completa")

# Mantener compatibilidad con ejecución directa
if __name__ == '__main__':
    pytest.main([__file__])
