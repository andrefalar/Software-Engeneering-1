"""
Tests para los modelos de datos de FortiFile
"""

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

def test_base_model():
    """Prueba que la Base compartida funciona correctamente"""
    try:
        from backend.models.base import Base
        from backend.models.user_model import Usuario
        from backend.models.file_model import Archivo  
        from backend.models.event_model import Evento
        
        print("✅ Base compartida importada correctamente")
        
        # Verificar que todos los modelos usan la misma Base
        print(f"   - Usuario usa Base: {Usuario.__bases__[0] == Base}")
        print(f"   - Archivo usa Base: {Archivo.__bases__[0] == Base}")
        print(f"   - Evento usa Base: {Evento.__bases__[0] == Base}")
        
        # Verificar metadatos
        tables = list(Base.metadata.tables.keys())
        print(f"   - Tablas registradas: {tables}")
        
        return True
    except Exception as e:
        print(f"❌ Error con Base compartida: {e}")
        return False

def run_all_model_tests():
    """Ejecuta todos los tests de modelos"""
    print("🧪 TESTS DE MODELOS")
    print("=" * 40)
    
    tests = [
        ("Usuario", test_usuario_model),
        ("Archivo", test_archivo_model), 
        ("Evento", test_evento_model),
        ("Base compartida", test_base_model)
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
    success = run_all_model_tests()
    exit(0 if success else 1)
