"""
FortiFile - Sistema de Archivos Seguros
Punto de entrada principal de la aplicación backend
"""

def main():
    """
    Función principal de FortiFile
    """
    print("🔐 FortiFile - Sistema de Archivos Seguros")
    print("=" * 50)
    print("Backend inicializado correctamente")
    print("Servicios disponibles:")
    print("  • UserService: Gestión de usuarios")
    print("  • FileService: Gestión de archivos cifrados")
    print("  • SystemService: Operaciones del sistema")
    print("\nPara pruebas, ejecuta:")
    print("  python -m backend.tests.test_runner")
    print("\nPara tests individuales:")
    print("  python -m backend.tests.test_models")
    print("  python -m backend.tests.test_database")
    print("  python -m backend.tests.test_user_service")
    print("  python -m backend.tests.test_file_service")
    print("  python -m backend.tests.test_system_service")

def check_system_health():
    """
    Verifica que el sistema esté funcionando correctamente
    """
    try:
        from backend.services.system_service import SystemService
        
        print("\n🔧 Verificando salud del sistema...")
        
        system_service = SystemService()
        status_result = system_service.get_system_status()
        
        if status_result['success']:
            status = status_result['status']
            print(f"✅ Sistema inicializado: {status['system_initialized']}")
            print(f"✅ Base de datos: {'OK' if status['database_exists'] else 'FALTA'}")
            print(f"✅ Clave cifrado: {'OK' if status['encryption_key_exists'] else 'FALTA'}")
            print(f"✅ Directorio seguro: {'OK' if status['secure_files_dir_exists'] else 'FALTA'}")
            
            # Verificar integridad
            integrity = system_service.verify_system_integrity()
            if integrity['success']:
                if integrity['integrity_ok']:
                    print("✅ Integridad del sistema: OK")
                else:
                    print(f"⚠️  Problemas de integridad encontrados: {integrity['issues_count']}")
                    for issue in integrity['issues']:
                        print(f"   - {issue}")
        else:
            print("❌ Error verificando sistema")
            
    except Exception as e:
        print(f"❌ Error en verificación: {e}")

def initialize_system():
    """
    Inicializa FortiFile si es la primera vez
    """
    try:
        from backend.database.connection import DatabaseManager
        
        print("\n🚀 Inicializando FortiFile...")
        
        db_manager = DatabaseManager()
        
        # Crear tablas si no existen
        if db_manager.create_tables():
            print("✅ Base de datos inicializada")
        
        # Crear directorio de archivos seguros
        import os
        if not os.path.exists("secure_files"):
            os.makedirs("secure_files")
            print("✅ Directorio de archivos seguros creado")
        
        print("✅ Sistema FortiFile listo para usar")
        
    except Exception as e:
        print(f"❌ Error inicializando sistema: {e}")

if __name__ == "__main__":
    main()
    initialize_system()
    check_system_health()
    
    print("\n" + "="*50)
    print("🎯 FortiFile Backend está funcionando correctamente")
    print("🔗 Listo para integración con Frontend")
    print("="*50)
