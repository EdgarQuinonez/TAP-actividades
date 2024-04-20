from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel

class Componente(QWidget):
    # Es un campo obligatorio. Checar estado focus. Si entro y coloco texto, se pone verde el borde y el *. Si entra y no pone nada, se pone rojo.
    # css en pyside6?
    def __init__(self):
        super().__init__()
        
        mainHLayout = QHBoxLayout(self)
        
        self.value = QLineEdit()
        
        mainHLayout.addWidget(self.value)
        mainHLayout.addWidget(QLabel("*"))
        
        self.value.focusOutEvent.connect(self.changeStyles)
        
    def checkNotEmpty(self):
        if self.value.text() != "":
            return True
        else:
            return False
        
    def changeStyles(self):
        isNotEmpty = self.checkNotEmpty()
        
        if isNotEmpty:
            
            self.value.setStyleSheet(
            """
            border-color: green 
            """
            )
        else:
            self.value.setStyleSheet(
            """
            border-color: red 
            """
            )
            
        
        