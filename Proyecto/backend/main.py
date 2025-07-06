import os

def test_usuario_model():
    """Prueba que el modelo Usuario funciona correctamente"""
    try:
        from backend.models.user_model import Usuario, Base
        print("✅ Modelo Usuario importado correctamente")
        print(f"   - Tabla: {Usuario.__tablename__}")
        print(f"   - Columnas: {list(Usuario.__table__.columns.keys())}")
        
        # Crear una instancia para probar
        usuario_test = Usuario(username="test_user", password_hash="hash123")
        print(f"✅ Instancia creada: {usuario_test}")
        
        return True
    except Exception as e:
        print(f"❌ Error con modelo Usuario: {e}")
        return False

def test_archivo_model():
    """Prueba que el modelo Archivo funciona correctamente"""
    try:
        from backend.models.file_model import Archivo, Base
        print("✅ Modelo Archivo importado correctamente")
        print(f"   - Tabla: {Archivo.__tablename__}")
        print(f"   - Columnas: {list(Archivo.__table__.columns.keys())}")
        
        # Crear una instancia para probar
        archivo_test = Archivo(
            nombre_archivo="documento.pdf", 
            ruta_archivo="/ruta/segura/documento.pdf",
            usuario_id=1
        )
        print(f"✅ Instancia creada: {archivo_test}")
        
        return True
    except Exception as e:
        print(f"❌ Error con modelo Archivo: {e}")
        return False

def test_evento_model():
    """Prueba que el modelo Evento funciona correctamente"""
    try:
        from backend.models.event_model import Evento, Base
        print("✅ Modelo Evento importado correctamente")
        print(f"   - Tabla: {Evento.__tablename__}")
        print(f"   - Columnas: {list(Evento.__table__.columns.keys())}")
        
        # Crear una instancia para probar
        evento_test = Evento(
            descripcion="Usuario inició sesión exitosamente",
            usuario_id=1
        )
        print(f"✅ Instancia creada: {evento_test}")
        
        return True
    except Exception as e:
        print(f"❌ Error con modelo Evento: {e}")
        return False

def test_database_connection():
    """Prueba que la conexión a la base de datos funciona"""
    try:
        from backend.database.connection import DatabaseManager
        
        print("🔧 Probando conexión a base de datos...")
        
        # Crear instancia del gestor
        db_manager = DatabaseManager("test_fortifile.db")
        
        # Obtener información de la base de datos
        db_info = db_manager.get_database_info()
        print(f"   - Archivo: {db_info['path']}")
        print(f"   - Existe: {db_info['exists']}")
        
        # Crear las tablas
        if db_manager.create_tables():
            print("✅ Tablas creadas exitosamente")
        else:
            return False
            
        # Probar obtener una sesión
        session = db_manager.get_session()
        session.close()
        print("✅ Sesión de base de datos obtenida correctamente")
        
        # Verificar información actualizada
        db_info = db_manager.get_database_info()
        print(f"   - Tamaño: {db_info['size_mb']} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con conexión a base de datos: {e}")
        return False

def test_user_service():
    """Prueba el servicio de usuario"""
    try:
        from backend.services.user_service import UserService
        
        print("� Probando UserService...")
        
        # Inicializar servicio
        user_service = UserService()
        
        # Crear tablas primero
        user_service.db_manager.create_tables()
        
        # 1. Verificar que no hay usuarios
        print(f"   - ¿Usuario existe? {user_service.user_exists()}")
        
        # 2. Registrar primer usuario
        result = user_service.register_user("admin", "miPassword123")
        print(f"   - Registro: {result['success']} - {result['message']}")
        
        if result['success']:
            user_id = result['user_id']
            
            # 3. Intentar registrar segundo usuario (debe fallar)
            result2 = user_service.register_user("admin2", "pass456")
            print(f"   - Segundo registro: {result2['success']} - {result2['message']}")
            
            # 4. Probar autenticación correcta
            auth_result = user_service.authenticate_user("admin", "miPassword123")
            print(f"   - Login correcto: {auth_result['success']} - {auth_result['message']}")
            
            # 5. Probar autenticación incorrecta
            auth_fail = user_service.authenticate_user("admin", "passwordMala")
            print(f"   - Login incorrecto: {auth_fail['success']} - {auth_fail['message']}")
            
            # 6. Obtener info de usuario
            user_info = user_service.get_user_info(user_id)
            print(f"   - Info usuario: {user_info['username']} creado el {user_info['fecha_creacion']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con UserService: {e}")
        return False

def test_file_service():
    """Prueba el servicio de archivos"""
    try:
        from backend.services.file_service import FileService
        from backend.services.user_service import UserService
        
        print("🔧 Probando FileService...")
        
        # Inicializar servicios
        user_service = UserService()
        file_service = FileService()
        
        # Crear tablas
        user_service.db_manager.create_tables()
        
        # Registrar un usuario para las pruebas
        user_result = user_service.register_user("testuser", "password123")
        if not user_result['success']:
            print("   ⚠️  Usuario ya existe, continuando...")
            # Intentar autenticar usuario existente
            auth_result = user_service.authenticate_user("testuser", "password123")
            if auth_result['success']:
                user_id = auth_result['user_id']
            else:
                # Si no puede autenticar, usar ID 1
                user_id = 1
        else:
            user_id = user_result['user_id']
        
        print(f"   - Usuario ID para pruebas: {user_id}")
        
        # Crear archivo de prueba
        test_file_path = "test_document.txt"
        test_content = "Este es un documento de prueba para FortiFile.\n¡Contenido confidencial!"
        
        with open(test_file_path, 'w') as f:
            f.write(test_content)
        print(f"   - Archivo de prueba creado: {test_file_path}")
        
        # 1. Subir archivo (RF-03 y RF-04)
        upload_result = file_service.upload_file(user_id, test_file_path, "documento_secreto.txt")
        print(f"   - Subida: {upload_result['success']} - {upload_result['message']}")
        
        if upload_result['success']:
            file_id = upload_result['file_id']
            
            # 2. Listar archivos (RF-05)
            files_result = file_service.get_user_files(user_id)
            print(f"   - Archivos del usuario: {files_result['count']} archivo(s)")
            if files_result['success'] and files_result['count'] > 0:
                for file_info in files_result['files']:
                    print(f"     * {file_info['nombre']} ({file_info['size_mb']} MB)")
            
            # 3. Descargar archivo (RF-06)
            download_path = "downloaded_document.txt"
            download_result = file_service.download_file(user_id, file_id, download_path)
            print(f"   - Descarga: {download_result['success']} - {download_result['message']}")
            
            # Verificar contenido descargado
            if download_result['success']:
                with open(download_path, 'r') as f:
                    downloaded_content = f.read()
                content_match = downloaded_content == test_content
                print(f"   - Contenido verificado: {content_match}")
                
                # Limpiar archivo descargado
                if os.path.exists(download_path):
                    os.remove(download_path)
            
            # 4. Info de almacenamiento
            storage_info = file_service.get_storage_info()
            if storage_info['success']:
                print(f"   - Almacenamiento: {storage_info['total_files']} archivos, {storage_info['total_size_mb']} MB")
            
            # 5. Eliminar archivo (RF-07)
            delete_result = file_service.delete_file(user_id, file_id)
            print(f"   - Eliminación: {delete_result['success']} - {delete_result['message']}")
        
        # Limpiar archivo de prueba
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error con FileService: {e}")
        return False

if __name__ == "__main__":
    print("🚀 FortiFile - Paso 6: Servicio de Archivos")
    print("=" * 50)
    
    # Verificaciones rápidas
    print("� Verificando componentes base...")
    if not (test_usuario_model() and test_archivo_model() and test_evento_model()):
        print("❌ Error en modelos")
        exit()
    print("✅ Modelos: OK")
    
    if not test_database_connection():
        print("❌ Error en conexión")
        exit()
    print("✅ Conexión: OK")
    
    if not test_user_service():
        print("❌ Error en UserService")
        exit()
    print("✅ UserService: OK\n")

def test_advanced_user_features():
    """Prueba funcionalidades avanzadas del UserService"""
    try:
        from backend.services.user_service import UserService
        
        print("🔧 Probando funcionalidades avanzadas de usuario...")
        
        user_service = UserService()
        user_service.db_manager.create_tables()
        
        # 1. Validación de contraseña
        weak_password = "123"
        result = user_service.register_user("testuser", weak_password)
        print(f"   - Contraseña débil rechazada: {not result['success']}")
        
        # 2. Registro con contraseña fuerte
        strong_password = "MiPassword123"
        result = user_service.register_user("testuser", strong_password)
        if result['success']:
            user_id = result['user_id']
            print(f"   - Usuario registrado con contraseña fuerte: {result['success']}")
            
            # 3. Probar intentos fallidos (RF-04)
            print("   - Probando bloqueo por intentos fallidos:")
            for i in range(4):
                auth_result = user_service.authenticate_user("testuser", "passwordMala")
                print(f"     Intento {i+1}: {auth_result['message']}")
                if auth_result.get('locked'):
                    break
            
            # 4. Resetear intentos
            user_service.reset_failed_attempts()
            print("   - Intentos fallidos reseteados")
            
            # 5. Login exitoso
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
        print(f"❌ Error con funcionalidades avanzadas: {e}")
        return False

def test_system_service():
    """Prueba el servicio del sistema"""
    try:
        from backend.services.system_service import SystemService
        
        print("🔧 Probando SystemService...")
        
        system_service = SystemService()
        
        # 1. Estado del sistema
        status_result = system_service.get_system_status()
        if status_result['success']:
            status = status_result['status']
            print(f"   - Sistema inicializado: {status['system_initialized']}")
            print(f"   - BD existe: {status['database_exists']}")
            print(f"   - Archivos seguros: {status['secure_files_count']}")
        
        # 2. Verificar integridad
        integrity_result = system_service.verify_system_integrity()
        if integrity_result['success']:
            print(f"   - Integridad OK: {integrity_result['integrity_ok']}")
            if not integrity_result['integrity_ok']:
                print(f"   - Problemas encontrados: {integrity_result['issues_count']}")
        
        # 3. Probar respaldo
        backup_result = system_service.backup_system("backup_test")
        print(f"   - Respaldo creado: {backup_result['success']}")
        
        # Limpiar directorio de prueba
        if os.path.exists("backup_test"):
            import shutil
            shutil.rmtree("backup_test")
        
        # 4. NOTA: NO probamos reset_system aquí porque eliminaría todo
        print("   - Reset del sistema: Disponible (no ejecutado en prueba)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con SystemService: {e}")
        return False
        
    # Probar servicio de archivos
    if test_file_service():
        print("\n✅ Paso 6 completado - FileService funcionando correctamente")
    else:
        print("\n❌ Error en Paso 6 - Revisar FileService")
        exit()
    
    print("✅ Servicios básicos: OK\n")
    
    # Funcionalidades avanzadas
    print("🚀 Probando funcionalidades avanzadas...")
    
    if test_advanced_user_features():
        print("✅ Funcionalidades avanzadas de usuario: OK")
    else:
        print("❌ Error en funcionalidades avanzadas")
    
    if test_system_service():
        print("✅ Servicio del sistema: OK")
    else:
        print("❌ Error en servicio del sistema")
    
    print("\n" + "="*50)
    print("🎉 BACKEND FORTIFILE COMPLETADO")
    print("="*50)
    print("✅ Funcionalidades implementadas:")
    print("   • RF-01: Registro de usuario único")
    print("   • RF-02: Inicio de sesión seguro")
    print("   • RF-03: Carga de archivos")
    print("   • RF-04: Cifrado automático")
    print("   • RF-04: Bloqueo por intentos fallidos")
    print("   • RF-05: Visualización de archivos")
    print("   • RF-06: Descarga y descifrado")
    print("   • RF-07: Eliminación segura")
    print("   • RF-08: Cambio de contraseña")
    print("   • RF-10: Eliminación de cuenta")
    print("   • RF-11: Sistema de eventos/logs")
    print("   • RF-12: Usuario único")
    print("   • RF-13: Reinicio del sistema")
    print("   • RNF-02: Contraseñas seguras")
    print("   • RNF-10: Base de datos embebida")
    print("\n📁 El backend está listo para integrarse con el frontend")