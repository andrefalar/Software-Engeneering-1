from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
import os

from themes import colors, fonts


class StartView(QWidget):
    """
    Vista de inicio de FortiFile.
    """

    def __init__(self, go_to_login):
        super().__init__()
        self.go_to_login = go_to_login
        self.setWindowTitle("FortiFile")
        self.setMinimumSize(500, 400)
        self.set_icon()
        self.setup_ui()

    def set_icon(self):
        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png")
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def setup_ui(self):
        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {colors.DARKEST};
                font-family: '{fonts.BODY_FONT}';
                color: {colors.WHITE};
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {colors.DARK};
                color: {colors.WHITE};
                border: none;
                padding: 12px 25px;
                font-size: 16px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {colors.GRAY};
            }}
            QLabel {{
                font-family: '{fonts.BODY_FONT}';
                font-size: 14px;
            }}
        """
        )

        layout = QVBoxLayout()
        layout.setSpacing(
            0
        )  # Removemos el spacing general para controlarlo manualmente

        logo_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png")
        )
        logo_label = QLabel()
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(
                pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            logo_label.setText("Sin logo")
        logo_label.setAlignment(Qt.AlignCenter)

        title_label = QLabel("FortiFile")
        title_label.setFont(QFont(fonts.TITLE_FONT, 42, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 42px; font-weight: bold; color: white;")

        ingresar_button = QPushButton("Ingresar")
        ingresar_button.clicked.connect(self.go_to_login)
        ingresar_button.setToolTip("Ir a la pantalla de inicio de sesión")
        ingresar_button.setFixedWidth(120)

        layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        layout.addWidget(logo_label)
        layout.addSpacing(10)  # Pequeño espacio entre logo y título
        layout.addWidget(title_label)
        layout.addSpacing(40)  # Espacio más grande antes del botón
        layout.addWidget(ingresar_button, alignment=Qt.AlignCenter)
        layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        layout.setContentsMargins(50, 40, 50, 40)

        self.setLayout(layout)
