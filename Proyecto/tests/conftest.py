import sys
import os
import pytest
from PyQt5.QtWidgets import QApplication

# Agregar el directorio del proyecto al path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


@pytest.fixture(scope="session")
def qapp():
    """Fixture para crear una instancia de QApplication para todos los tests GUI."""
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    yield app
    # No llamamos quit() aquí para evitar problemas entre tests
