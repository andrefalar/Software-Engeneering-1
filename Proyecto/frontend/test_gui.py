# test_gui.py
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication([])
label = QLabel("¡Hola desde WSLg con PyQt5!")
label.show()
app.exec_()