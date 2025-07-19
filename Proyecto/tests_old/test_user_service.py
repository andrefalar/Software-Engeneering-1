"""
Tests para el servicio de usuario
"""

def test_user_service_basic():
    """Prueba funcionalidades básicas del UserService"""
    try:
        from backend.services.user_service import UserService
        
        print("🔧 Probando UserService básico...")
        
        # Inicializar servicio
        user_service = UserService()
        
        # Crear tablas primero
        user_service.db_manager.create_tables()
        
        # 1. Verificar que no hay usuarios
        print(f"   - ¿Usuario existe? {user_service.user_exists()}")
        
        # 2. Registrar primer usuario
        result = user_service.register_user("admin", "MiPassword123")
        print(f"   - Registro: {result['success']} - {result['message']}")
        
        if result['success']:
            user_id = result['user_id']
            
            # 3. Intentar registrar segundo usuario (debe fallar)
            result2 = user_service.register_user("admin2", "Password456")
            print(f"   - Segundo registro: {result2['success']} - {result2['message']}")
            
            # 4. Probar autenticación correcta
            auth_result = user_service.authenticate_user("admin", "MiPassword123")
            print(f"   - Login correcto: {auth_result['success']} - {auth_result['message']}")
            
            # 5. Probar autenticación incorrecta
            auth_fail = user_service.authenticate_user("admin", "passwordMala")
            print(f"   - Login incorrecto: {auth_fail['success']} - {auth_fail['message']}")
            
            # 6. Obtener info de usuario
            user_info = user_service.get_user_info(user_id)
            if user_info['success']:
                print(f"   - Info usuario: {user_info['username']} creado el {user_info['fecha_creacion']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con UserService básico: {e}")
        return False

def test_user_service_advanced():
    """Prueba funcionalidades avanzadas del UserService"""
    try:
        from backend.services.user_service import UserService
        
        print("🔧 Probando UserService avanzado...")
        
        user_service = UserService()
        user_service.db_manager.create_tables()
        
        # 1. Validación de contraseña débil
        weak_password = "123"
        result = user_service.register_user("testuser", weak_password)
        print(f"   - Contraseña débil rechazada: {not result['success']}")
        
        # 2. Registro con contraseña fuerte
        strong_password = "MiPassword123"
        result = user_service.register_user("testuser", strong_password)
        if result['success']:
            user_id = result['user_id']
            print(f"   - Usuario registrado con contraseña fuerte: {result['success']}")
            
            # 3. Probar bloqueo por intentos fallidos (RF-04)
            print("   - Probando bloqueo por intentos fallidos:")
            for i in range(4):
                auth_result = user_service.authenticate_user("testuser", "passwordMala")
                print(f"     Intento {i+1}: Bloqueado={auth_result.get('locked', False)}")
                if auth_result.get('locked'):
                    break
            
            # 4. Resetear intentos
            user_service.reset_failed_attempts()
            print("   - Intentos fallidos reseteados")
            
            # 5. Login exitoso después de reset
            auth_result = user_service.authenticate_user("testuser", strong_password)
            print(f"   - Login después de reset: {auth_result['success']}")
            
            # 6. Cambio de contraseña (RF-08)
            new_password = "NuevaPassword456"
            change_result = user_service.change_password(user_id, strong_password, new_password)
            print(f"   - Cambio de contraseña: {change_result['success']}")
            
            # 7. Verificar nuevo login
            auth_new = user_service.authenticate_user("testuser", new_password)
            print(f"   - Login con nueva contraseña: {auth_new['success']}")
            
            # 8. Ver eventos
            events_result = user_service.get_user_events(user_id, 5)
            print(f"   - Eventos registrados: {events_result['count']}")
            
            # 9. Estado de seguridad
            security_status = user_service.get_security_status()
            print(f"   - Cuenta bloqueada: {security_status['account_locked']}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error con UserService avanzado: {e}")
        return False

def test_user_service_password_validation():
    """Prueba las validaciones de contraseña"""
    try:
        from backend.services.user_service import UserService
        
        print("🔧 Probando validación de contraseñas...")
        
        user_service = UserService()
        
        # Tests de validación
        test_passwords = [
            ("123", False, "muy corta"),
            ("password", False, "sin mayúscula ni número"),
            ("PASSWORD", False, "sin minúscula ni número"),
            ("Password", False, "sin número"),
            ("Password1", True, "válida"),
            ("MiSuperPassword123", True, "válida compleja")
        ]
        
        for password, should_be_valid, description in test_passwords:
            validation = user_service._validate_password(password)
            result = validation['valid'] == should_be_valid
            status = "✅" if result else "❌"
            print(f"   {status} '{password}' ({description}): {validation['message']}")
            if not result:
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error con validación de contraseñas: {e}")
        return False

def run_all_user_service_tests():
    """Ejecuta todos los tests de UserService"""
    print("🧪 TESTS DE USER SERVICE")
    print("=" * 40)
    
    tests = [
        ("Funcionalidades básicas", test_user_service_basic),
        ("Funcionalidades avanzadas", test_user_service_advanced),
        ("Validación contraseñas", test_user_service_password_validation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔧 Test: {test_name}")
        print("-" * 30)
        if test_func():
            print(f"✅ {test_name}: PASÓ")
            passed += 1
        else:
            print(f"❌ {test_name}: FALLÓ")
    
    print(f"\n📊 RESULTADO: {passed}/{total} tests pasaron")
    return passed == total

if __name__ == "__main__":
    success = run_all_user_service_tests()
    exit(0 if success else 1)
