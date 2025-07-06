"""
Ejecutor principal de todos los tests de FortiFile Backend
"""
import sys
from datetime import datetime

def run_test_suite(test_name, test_runner_func):
    """
    Ejecuta una suite de tests y maneja errores
    
    Args:
        test_name (str): Nombre de la suite de tests
        test_runner_func (function): Función que ejecuta los tests
        
    Returns:
        bool: True si todos los tests pasaron
    """
    try:
        print(f"\n{'='*60}")
        print(f"🧪 EJECUTANDO: {test_name}")
        print(f"{'='*60}")
        
        result = test_runner_func()
        
        if result:
            print(f"\n🎉 {test_name}: TODOS LOS TESTS PASARON")
        else:
            print(f"\n❌ {test_name}: ALGUNOS TESTS FALLARON")
        
        return result
        
    except Exception as e:
        print(f"\n💥 ERROR EJECUTANDO {test_name}: {e}")
        return False

def run_all_tests():
    """Ejecuta todos los tests del backend de FortiFile"""
    
    print("🚀 FORTIFILE BACKEND - SUITE COMPLETA DE TESTS")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Definir todas las suites de tests
    test_suites = [
        ("MODELOS DE DATOS", lambda: __import__('backend.tests.test_models', fromlist=['run_all_model_tests']).run_all_model_tests()),
        ("BASE DE DATOS", lambda: __import__('backend.tests.test_database', fromlist=['run_all_database_tests']).run_all_database_tests()),
        ("USER SERVICE", lambda: __import__('backend.tests.test_user_service', fromlist=['run_all_user_service_tests']).run_all_user_service_tests()),
        ("FILE SERVICE", lambda: __import__('backend.tests.test_file_service', fromlist=['run_all_file_service_tests']).run_all_file_service_tests()),
        ("SYSTEM SERVICE", lambda: __import__('backend.tests.test_system_service', fromlist=['run_all_system_service_tests']).run_all_system_service_tests())
    ]
    
    # Ejecutar todas las suites
    results = []
    
    for suite_name, test_runner in test_suites:
        result = run_test_suite(suite_name, test_runner)
        results.append((suite_name, result))
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL DE TESTS")
    print("="*60)
    
    passed_suites = 0
    total_suites = len(results)
    
    for suite_name, passed in results:
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"{status:12} - {suite_name}")
        if passed:
            passed_suites += 1
    
    print("-" * 60)
    print(f"RESULTADO: {passed_suites}/{total_suites} suites pasaron")
    
    if passed_suites == total_suites:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ El backend de FortiFile está funcionando correctamente")
        print("✅ Todas las funcionalidades están implementadas y probadas")
        print("✅ El sistema está listo para integración con frontend")
    else:
        print(f"\n⚠️  {total_suites - passed_suites} suite(s) tienen problemas")
        print("❌ Revisar los tests fallidos antes de continuar")
    
    print("\n" + "="*60)
    print("🔧 COMANDOS ÚTILES:")
    print("="*60)
    print("# Ejecutar tests individuales:")
    print("python -m backend.tests.test_models")
    print("python -m backend.tests.test_database") 
    print("python -m backend.tests.test_user_service")
    print("python -m backend.tests.test_file_service")
    print("python -m backend.tests.test_system_service")
    print("\n# Ejecutar todos los tests:")
    print("python -m backend.tests.test_runner")
    print("="*60)
    
    return passed_suites == total_suites

def run_quick_tests():
    """Ejecuta solo tests rápidos (modelos y database)"""
    print("⚡ TESTS RÁPIDOS DE FORTIFILE")
    print("=" * 40)
    
    quick_suites = [
        ("MODELOS", lambda: __import__('backend.tests.test_models', fromlist=['run_all_model_tests']).run_all_model_tests()),
        ("BASE DE DATOS", lambda: __import__('backend.tests.test_database', fromlist=['run_all_database_tests']).run_all_database_tests())
    ]
    
    results = []
    for suite_name, test_runner in quick_suites:
        result = run_test_suite(suite_name, test_runner)
        results.append(result)
    
    all_passed = all(results)
    print(f"\n⚡ TESTS RÁPIDOS: {'✅ PASARON' if all_passed else '❌ FALLARON'}")
    
    return all_passed

def main():
    """Función principal"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            success = run_quick_tests()
        elif sys.argv[1] == "--help":
            print("🧪 FortiFile Test Runner")
            print("Uso:")
            print("  python -m backend.tests.test_runner           # Todos los tests")
            print("  python -m backend.tests.test_runner --quick   # Solo tests rápidos")
            print("  python -m backend.tests.test_runner --help    # Esta ayuda")
            return True
        else:
            print(f"❌ Opción desconocida: {sys.argv[1]}")
            print("Usa --help para ver opciones disponibles")
            return False
    else:
        success = run_all_tests()
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
