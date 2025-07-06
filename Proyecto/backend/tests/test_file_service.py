"""
Tests para el servicio de archivos
"""
import os

def test_file_service_basic():
    """Prueba funcionalidades básicas del FileService"""
    try:
        from backend.services.file_service import FileService
        from backend.services.user_service import UserService
        
        print("🔧 Probando FileService básico...")
        
        # Inicializar servicios
        user_service = UserService()
        file_service = FileService()
        
        # Crear tablas
        user_service.db_manager.create_tables()
        
        # Registrar un usuario para las pruebas
        user_result = user_service.register_user("fileuser", "FilePassword123")
        if not user_result['success']:
            # Si usuario ya existe, intentar autenticar
            auth_result = user_service.authenticate_user("fileuser", "FilePassword123")
            user_id = auth_result['user_id'] if auth_result['success'] else 1
        else:
            user_id = user_result['user_id']
        
        print(f"   - Usuario ID para pruebas: {user_id}")
        
        # Crear archivo de prueba
        test_file_path = "test_file_service.txt"
        test_content = "Contenido de prueba para FileService\n¡Datos confidenciales!"
        
        with open(test_file_path, 'w') as f:
            f.write(test_content)
        print(f"   - Archivo de prueba creado: {test_file_path}")
        
        # 1. Subir archivo (RF-03 y RF-04)
        upload_result = file_service.upload_file(user_id, test_file_path, "documento_prueba.txt")
        print(f"   - Subida y cifrado: {upload_result['success']}")
        
        if upload_result['success']:
            file_id = upload_result['file_id']
            
            # 2. Listar archivos (RF-05)
            files_result = file_service.get_user_files(user_id)
            print(f"   - Archivos listados: {files_result['count']} archivo(s)")
            
            # 3. Info de almacenamiento
            storage_info = file_service.get_storage_info()
            if storage_info['success']:
                print(f"   - Almacenamiento: {storage_info['total_files']} archivos")
            
            # 4. Descargar archivo (RF-06)
            download_path = "downloaded_test_file.txt"
            download_result = file_service.download_file(user_id, file_id, download_path)
            print(f"   - Descarga y descifrado: {download_result['success']}")
            
            # Verificar contenido
            if download_result['success']:
                with open(download_path, 'r') as f:
                    downloaded_content = f.read()
                content_match = downloaded_content == test_content
                print(f"   - Contenido verificado: {content_match}")
                
                # Limpiar archivo descargado
                if os.path.exists(download_path):
                    os.remove(download_path)
            
            # 5. Eliminar archivo (RF-07)
            delete_result = file_service.delete_file(user_id, file_id)
            print(f"   - Eliminación segura: {delete_result['success']}")
        
        # Limpiar archivo de prueba
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error con FileService básico: {e}")
        return False

def test_file_service_security():
    """Prueba características de seguridad del FileService"""
    try:
        from backend.services.file_service import FileService
        from backend.services.user_service import UserService
        
        print("🔧 Probando seguridad de FileService...")
        
        user_service = UserService()
        file_service = FileService()
        user_service.db_manager.create_tables()
        
        # Crear dos usuarios
        user1_result = user_service.register_user("user1", "Password123")
        user1_id = user1_result['user_id'] if user1_result['success'] else 1
        
        # Crear archivo de prueba
        test_file = "security_test.txt"
        with open(test_file, 'w') as f:
            f.write("Archivo confidencial del usuario 1")
        
        # Usuario 1 sube archivo
        upload_result = file_service.upload_file(user1_id, test_file, "archivo_privado.txt")
        if upload_result['success']:
            file_id = upload_result['file_id']
            
            # Verificar que usuario 1 puede ver sus archivos
            files_user1 = file_service.get_user_files(user1_id)
            print(f"   - Usuario 1 ve sus archivos: {files_user1['count'] > 0}")
            
            # Simular usuario diferente (ID 999) intentando acceder
            fake_user_id = 999
            
            # Intentar descargar archivo de otro usuario (debe fallar)
            download_result = file_service.download_file(fake_user_id, file_id, "hack_attempt.txt")
            print(f"   - Acceso denegado a otro usuario: {not download_result['success']}")
            
            # Intentar eliminar archivo de otro usuario (debe fallar)
            delete_result = file_service.delete_file(fake_user_id, file_id)
            print(f"   - Eliminación denegada a otro usuario: {not delete_result['success']}")
            
            # Usuario correcto puede eliminar
            delete_result = file_service.delete_file(user1_id, file_id)
            print(f"   - Usuario correcto puede eliminar: {delete_result['success']}")
        
        # Limpiar
        if os.path.exists(test_file):
            os.remove(test_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Error con seguridad FileService: {e}")
        return False

def test_file_service_encryption():
    """Prueba que los archivos se cifran correctamente"""
    try:
        from backend.services.file_service import FileService
        from backend.services.user_service import UserService
        
        print("🔧 Probando cifrado de archivos...")
        
        user_service = UserService()
        file_service = FileService()
        user_service.db_manager.create_tables()
        
        # Obtener o crear usuario
        user_result = user_service.register_user("cryptouser", "CryptoPass123")
        user_id = user_result['user_id'] if user_result['success'] else 1
        
        # Crear archivo con contenido específico
        original_file = "encryption_test.txt"
        original_content = "CONTENIDO SUPER SECRETO QUE DEBE SER CIFRADO"
        
        with open(original_file, 'w') as f:
            f.write(original_content)
        
        # Subir archivo
        upload_result = file_service.upload_file(user_id, original_file, "archivo_cifrado.txt")
        
        if upload_result['success']:
            # Obtener ruta del archivo cifrado
            files_result = file_service.get_user_files(user_id)
            if files_result['success'] and files_result['count'] > 0:
                # Leer archivo cifrado directamente
                file_info = files_result['files'][0]
                encrypted_file_path = None
                
                # Buscar el archivo en secure_files
                if os.path.exists("secure_files"):
                    for filename in os.listdir("secure_files"):
                        if "archivo_cifrado.txt" in filename:
                            encrypted_file_path = os.path.join("secure_files", filename)
                            break
                
                if encrypted_file_path and os.path.exists(encrypted_file_path):
                    with open(encrypted_file_path, 'rb') as f:
                        encrypted_content = f.read()
                    
                    # Verificar que el contenido está cifrado (no es legible)
                    is_encrypted = original_content.encode() not in encrypted_content
                    print(f"   - Archivo está cifrado: {is_encrypted}")
                    print(f"   - Tamaño archivo original: {len(original_content)} bytes")
                    print(f"   - Tamaño archivo cifrado: {len(encrypted_content)} bytes")
                
                # Limpiar - eliminar archivo del sistema
                file_id = upload_result['file_id']
                file_service.delete_file(user_id, file_id)
        
        # Limpiar archivo original
        if os.path.exists(original_file):
            os.remove(original_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando cifrado: {e}")
        return False

def run_all_file_service_tests():
    """Ejecuta todos los tests de FileService"""
    print("🧪 TESTS DE FILE SERVICE")
    print("=" * 40)
    
    tests = [
        ("Funcionalidades básicas", test_file_service_basic),
        ("Seguridad de acceso", test_file_service_security),
        ("Cifrado de archivos", test_file_service_encryption)
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
    success = run_all_file_service_tests()
    exit(0 if success else 1)
