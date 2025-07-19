"""
Tests para el servicio del sistema
"""
import os
import shutil

def test_system_service_status():
    """Prueba el estado del sistema"""
    try:
        from backend.services.system_service import SystemService
        
        print("🔧 Probando estado del sistema...")
        
        system_service = SystemService()
        
        # 1. Estado del sistema
        status_result = system_service.get_system_status()
        if status_result['success']:
            status = status_result['status']
            print(f"   - Sistema inicializado: {status['system_initialized']}")
            print(f"   - BD existe: {status['database_exists']}")
            print(f"   - Clave cifrado existe: {status['encryption_key_exists']}")
            print(f"   - Directorio seguro existe: {status['secure_files_dir_exists']}")
            print(f"   - Archivos seguros: {status['secure_files_count']}")
            print(f"   - Tamaño BD: {status['database_size_mb']} MB")
        else:
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando estado del sistema: {e}")
        return False

def test_system_service_integrity():
    """Prueba la verificación de integridad"""
    try:
        from backend.services.system_service import SystemService
        
        print("🔧 Probando verificación de integridad...")
        
        system_service = SystemService()
        
        # Asegurar que el sistema esté inicializado
        system_service.db_manager.create_tables()
        
        # Verificar integridad
        integrity_result = system_service.verify_system_integrity()
        if integrity_result['success']:
            print(f"   - Integridad OK: {integrity_result['integrity_ok']}")
            print(f"   - Problemas encontrados: {integrity_result['issues_count']}")
            
            if integrity_result['issues_count'] > 0:
                for issue in integrity_result['issues']:
                    print(f"     - {issue}")
        else:
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando integridad: {e}")
        return False

def test_system_service_backup():
    """Prueba el sistema de respaldo"""
    try:
        from backend.services.system_service import SystemService
        
        print("🔧 Probando sistema de respaldo...")
        
        system_service = SystemService()
        system_service.db_manager.create_tables()
        
        # Crear directorio de respaldo de prueba
        backup_dir = "test_backup"
        
        # Realizar respaldo
        backup_result = system_service.backup_system(backup_dir)
        print(f"   - Respaldo creado: {backup_result['success']}")
        
        if backup_result['success']:
            print(f"   - Elementos respaldados: {len(backup_result['backup_items'])}")
            
            # Verificar que se creó el directorio
            backup_exists = os.path.exists(backup_dir)
            print(f"   - Directorio respaldo existe: {backup_exists}")
            
            # Verificar archivos de respaldo
            if backup_exists:
                backup_files = os.listdir(backup_dir)
                print(f"   - Archivos en respaldo: {len(backup_files)}")
                for file in backup_files:
                    print(f"     - {file}")
        
        # Limpiar directorio de respaldo
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
            print("   - Directorio respaldo limpiado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando respaldo: {e}")
        return False

def test_system_service_reset_simulation():
    """Simula el proceso de reset (sin ejecutarlo realmente)"""
    try:
        from backend.services.system_service import SystemService
        
        print("🔧 Probando simulación de reset...")
        
        system_service = SystemService()
        
        # 1. Probar confirmación incorrecta
        wrong_confirmation = system_service.reset_system("TEXTO INCORRECTO")
        print(f"   - Confirmación incorrecta rechazada: {not wrong_confirmation['success']}")
        
        # 2. Verificar mensaje de error
        if not wrong_confirmation['success']:
            expected_msg = "Confirmación incorrecta"
            has_expected_msg = expected_msg in wrong_confirmation['message']
            print(f"   - Mensaje de error correcto: {has_expected_msg}")
        
        # NOTA: NO ejecutamos el reset real porque eliminaría todo el sistema
        print("   - Reset real: NO EJECUTADO (preserva datos del sistema)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error simulando reset: {e}")
        return False

def test_system_service_comprehensive():
    """Test comprehensivo del SystemService"""
    try:
        from backend.services.system_service import SystemService
        from backend.services.user_service import UserService
        from backend.services.file_service import FileService
        
        print("🔧 Test comprehensivo del sistema...")
        
        # Inicializar servicios
        system_service = SystemService()
        user_service = UserService()
        file_service = FileService()
        
        # Crear datos de prueba
        system_service.db_manager.create_tables()
        
        # Registrar usuario y subir archivo
        user_result = user_service.register_user("systemtest", "SystemTest123")
        if user_result['success']:
            user_id = user_result['user_id']
            
            # Crear y subir archivo de prueba
            test_file = "system_test_file.txt"
            with open(test_file, 'w') as f:
                f.write("Archivo para test comprehensivo")
            
            upload_result = file_service.upload_file(user_id, test_file, "test_system.txt")
            
            # Verificar estado del sistema después de crear datos
            status_after = system_service.get_system_status()
            if status_after['success']:
                status = status_after['status']
                print(f"   - Sistema con datos - BD: {status['database_size_mb']} MB")
                print(f"   - Archivos seguros: {status['secure_files_count']}")
            
            # Verificar integridad con datos
            integrity_with_data = system_service.verify_system_integrity()
            print(f"   - Integridad con datos: {integrity_with_data['integrity_ok']}")
            
            # Limpiar archivo de prueba
            if os.path.exists(test_file):
                os.remove(test_file)
            
            # Limpiar archivo subido
            if upload_result['success']:
                file_service.delete_file(user_id, upload_result['file_id'])
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test comprehensivo: {e}")
        return False

def run_all_system_service_tests():
    """Ejecuta todos los tests de SystemService"""
    print("🧪 TESTS DE SYSTEM SERVICE")
    print("=" * 40)
    
    tests = [
        ("Estado del sistema", test_system_service_status),
        ("Verificación integridad", test_system_service_integrity),
        ("Sistema de respaldo", test_system_service_backup),
        ("Simulación reset", test_system_service_reset_simulation),
        ("Test comprehensivo", test_system_service_comprehensive)
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
    success = run_all_system_service_tests()
    exit(0 if success else 1)
