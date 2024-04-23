from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel

class Componente(QWidget):
    # Es un campo obligatorio. Checar estado focus. Si entro y coloco texto, se pone verde el borde y el *. Si entra y no pone nada, se pone rojo.
    # css en pyside6?
    def __init__(self):
        super().__init__()
        
        mainHLayout = QHBoxLayout(self)
        
        self.lineEdit = QLineEdit()
        
        mainHLayout.addWidget(self.lineEdit)
        mainHLayout.addWidget(QLabel("*"))
        
        
    def checkNotEmpty(self):
        if self.lineEdit.text() != "":
            return True
        else:
            return False
        
    def changeStyles(self):
        isNotEmpty = self.checkNotEmpty()
        
        if isNotEmpty:
            
            self.lineEdit.setStyleSheet(
            """
            border-color: green;
            background-color: light-green;
            """
            )
        else:
            self.lineEdit.setStyleSheet(
            """
            border-color: red;
            background-color = pink;
            """
            )
            
        
        