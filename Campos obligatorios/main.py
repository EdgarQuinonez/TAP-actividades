import sys
from PySide6.QtWidgets import QWidget, QApplication, QFormLayout, QPushButton
from alt import Componente



class PruebaComponente(QWidget):
    """

    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setWindowTitle("Prueba Componente")
        
        self.firstComponent = Componente(placeholderText="Nombres")
        self.secondComponent = Componente(fontSizeBase=20, fontFamilyName="Times New Roman", fontSizeScale=1.7, placeholderText="Apellidos")
        self.acceptBtn = QPushButton("&Aceptar")
        
        
        mainFormLayout = QFormLayout(self)
        
        mainFormLayout.addRow("&Nombres:", self.firstComponent)
        mainFormLayout.addRow("&Apellidos:", self.secondComponent)
        mainFormLayout.addWidget(self.acceptBtn)
        
        # Listeners
        self.acceptBtn.clicked.connect(self.handleAcceptButtonClick)
        
    # Cambiar propiedades después de su construcción
    def changeComponentSpecialChar(self, componentRef, newSpecialChar):
        componentRef.changeSpecialChar(newSpecialChar)
        
    def changeComponentFontScale(self, componentRef, newFontScale):
        componentRef.changeFontScale(newFontScale)
        
    def changeComponentPlaceholderText(self, componentRef, newPlaceholderText):
        componentRef.changePlaceholderText(newPlaceholderText)
        
    def focusInvalidField(self, componentRef):
        componentRef.setFocusOnInvalid()        
        return
        
    def handleAcceptButtonClick(self):
        if not self.firstComponent.checkNotEmpty():            
            self.focusInvalidField(self.firstComponent)
        elif not self.secondComponent.checkNotEmpty():
            self.focusInvalidField(self.secondComponent)
        else:
            self.close()
            app.quit()
        
        
        
        
        


# Punto de inicio de ejecución del programa:
if __name__ == "__main__":
    app = QApplication([])

    widget = PruebaComponente()
    widget.show()

    sys.exit(app.exec())