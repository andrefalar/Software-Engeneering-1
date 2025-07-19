import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Agregar el directorio del proyecto al path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'frontend'))

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QSize

class TestMainApp(unittest.TestCase):
    """Test suite para la clase MainApp"""
    
    @classmethod
    def setUpClass(cls):
        """Configuración que se ejecuta una vez para toda la clase"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def setUp(self):
        """Configuración que se ejecuta antes de cada test"""
        # Crear mocks de widgets que hereden de QWidget
        self.start_view_mock = QWidget()
        self.login_view_mock = QWidget()
        self.register_view_mock = QWidget()  
        self.file_view_mock = QWidget()
        
        # Patches para las clases importadas
        self.patches = [
            patch('ui.start_view.StartView', return_value=self.start_view_mock),
            patch('ui.login_view.LoginView', return_value=self.login_view_mock),
            patch('ui.register_view.RegisterView', return_value=self.register_view_mock),
            patch('ui.file_view.FileManagerUI', return_value=self.file_view_mock)
        ]
        
        # Iniciar todos los patches
        for p in self.patches:
            p.start()
        
        # Importar y crear la aplicación después de los patches
        from frontend.app import MainApp
        self.main_app = MainApp()
    
    def tearDown(self):
        """Limpieza después de cada test"""
        if hasattr(self, 'main_app'):
            self.main_app.deleteLater()
        
        # Detener todos los patches
        for p in getattr(self, 'patches', []):
            p.stop()
    
    def test_mainapp_initialization(self):
        """Test 1: Verifica que MainApp se inicializa correctamente"""
        # Verificar atributos iniciales
        self.assertIsNone(self.main_app.current_user_id)
        self.assertEqual(self.main_app.windowTitle(), "FortiFile")
        self.assertEqual(self.main_app.size().width(), 900)
        self.assertEqual(self.main_app.size().height(), 500)
        
        # Verificar que se añadieron los widgets iniciales
        self.assertEqual(self.main_app.count(), 4)  # start, login, register, file
        
        print("✅ Test de inicialización pasado")
    
    def test_handle_logout_clears_user_id(self):
        """Test 2: Verifica que handle_logout limpia el current_user_id"""
        # Establecer un user_id
        self.main_app.current_user_id = 123
        
        # Mock del método show_start_view para evitar errores de UI
        with patch.object(self.main_app, 'show_start_view'):
            self.main_app.handle_logout()
        
        # Verificar que se limpió el user_id
        self.assertIsNone(self.main_app.current_user_id)
        
        print("✅ Test de logout pasado")
    
    def test_handle_login_success_sets_user_id(self):
        """Test 3: Verifica que handle_login_success establece el user_id correctamente"""
        test_user_id = 42
        
        # Mock de los métodos específicos que se llaman en handle_login_success
        with patch('ui.file_view.FileManagerUI') as mock_file_ui:
            with patch('ui.account_view.AccountWindow') as mock_account:
                # Configurar los mocks para retornar widgets válidos
                mock_file_ui.return_value = QWidget()
                mock_account.return_value = QWidget()
                
                # Mock de métodos de la aplicación
                with patch.object(self.main_app, 'show_file_view'):
                    with patch.object(self.main_app, 'removeWidget'):
                        with patch.object(self.main_app, 'addWidget'):
                            # Ejecutar el método
                            self.main_app.handle_login_success(test_user_id)
        
        # Verificar que se estableció el user_id correctamente
        self.assertEqual(self.main_app.current_user_id, test_user_id)
        print("✅ Test de login success pasado")
    
    def test_handle_login_success_fallback_user_id(self):
        """Test bonus: Verifica el fallback cuando user_id es None"""
        # Mock de los métodos necesarios
        with patch('ui.file_view.FileManagerUI') as mock_file_ui:
            with patch('ui.account_view.AccountWindow') as mock_account:
                # Configurar los mocks para retornar widgets válidos
                mock_file_ui.return_value = QWidget()
                mock_account.return_value = QWidget()
                
                # Mock de métodos de la aplicación
                with patch.object(self.main_app, 'show_file_view'):
                    with patch.object(self.main_app, 'removeWidget'):
                        with patch.object(self.main_app, 'addWidget'):
                            # Ejecutar el método con user_id None
                            self.main_app.handle_login_success(None)
        
        # Verificar que se estableció el fallback user_id = 1
        self.assertEqual(self.main_app.current_user_id, 1)
        print("✅ Test de fallback user_id pasado")

if __name__ == '__main__':
    unittest.main()
