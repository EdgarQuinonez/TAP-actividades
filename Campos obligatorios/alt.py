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
        
        self.firstComponent = Componente(specialChar="-")
        self.secondComponent = Componente()
        
        mainVLayout = QVBoxLayout(self)
        
        mainVLayout.addWidget(self.firstComponent)
        mainVLayout.addWidget(self.secondComponent)
        
        self.changeComponentSpecialChar(self.secondComponent, "+")
        self.changeComponentFontScale(self.secondComponent, 5)
        
    def changeComponentSpecialChar(self, componentRef, newSpecialChar):
        componentRef.changeSpecialChar(newSpecialChar)
        
    def changeComponentFontScale(self, componentRef, newFontScale):
        componentRef.changeFontScale(newFontScale)
        
        
        


# Punto de inicio de ejecución del programa:
if __name__ == "__main__":
    app = QApplication([])

    widget = PruebaComponente()
    widget.show()

    sys.exit(app.exec())