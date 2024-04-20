import sys
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout
from main import Componente



class PruebaComponente(QWidget):
    """

    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setWindowTitle("Prueba Componente")
        
        firstComponent = Componente()
        secondComponent = Componente()
        
        mainVLayout = QVBoxLayout(self)
        
        mainVLayout.addWidget(firstComponent)
        mainVLayout.addWidget(secondComponent)


# Punto de inicio de ejecución del programa:
if __name__ == "__main__":
    app = QApplication([])

    widget = PruebaComponente()
    widget.show()

    sys.exit(app.exec())