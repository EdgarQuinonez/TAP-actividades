import sys
from PySide6.QtWidgets import QWidget, QApplication


class Formulario(QWidget):
    """

    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setWindowTitle("Título")


# Punto de inicio de ejecución del programa:
if __name__ == "__main__":
    app = QApplication([])

    widget = Formulario()
    widget.show()

    sys.exit(app.exec())