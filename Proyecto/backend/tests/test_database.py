"""
Tests para la conexión y gestión de base de datos
"""
import os

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

def test_database_operations():
    """Prueba operaciones básicas de base de datos"""
    try:
        from backend.database.connection import DatabaseManager
        from backend.models.user_model import Usuario
        
        print("🔧 Probando operaciones de base de datos...")
        
        db_manager = DatabaseManager("test_operations.db")
        db_manager.create_tables()
        
        session = db_manager.get_session()
        
        # Crear un usuario de prueba
        test_user = Usuario(
            username="test_db_user",
            password_hash="test_hash_123"
        )
        
        session.add(test_user)
        session.commit()
        print("✅ Usuario insertado en BD")
        
        # Consultar usuario
        retrieved_user = session.query(Usuario).filter(Usuario.username == "test_db_user").first()
        if retrieved_user:
            print(f"✅ Usuario consultado: {retrieved_user.username}")
        else:
            print("❌ Error consultando usuario")
            return False
        
        session.close()
        
        # Limpiar archivo de prueba
        if os.path.exists("test_operations.db"):
            os.remove("test_operations.db")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con operaciones de BD: {e}")
        return False

def test_database_cleanup():
    """Prueba las operaciones de limpieza"""
    try:
        from backend.database.connection import DatabaseManager
        
        print("🔧 Probando limpieza de base de datos...")
        
        db_manager = DatabaseManager("test_cleanup.db")
        db_manager.create_tables()
        print("✅ Tablas creadas")
        
        # Probar drop_tables
        if db_manager.drop_tables():
            print("✅ Tablas eliminadas")
        else:
            return False
        
        # Limpiar archivo de prueba
        if os.path.exists("test_cleanup.db"):
            os.remove("test_cleanup.db")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con limpieza de BD: {e}")
        return False

def run_all_database_tests():
    """Ejecuta todos los tests de base de datos"""
    print("🧪 TESTS DE BASE DE DATOS")
    print("=" * 40)
    
    tests = [
        ("Conexión", test_database_connection),
        ("Operaciones", test_database_operations),
        ("Limpieza", test_database_cleanup)
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
    success = run_all_database_tests()
    exit(0 if success else 1)
