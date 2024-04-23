from PySide6.QtGui import QFocusEvent
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import Qt, Signal

class RequiredLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        
    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.changeStyles()
        super().focusOutEvent(event)
        
    def checkNotEmpty(self):
        if self.text() != "":
            return True
        else:
            return False
        
    def changeStyles(self):
        isNotEmpty = self.checkNotEmpty()
        
        if isNotEmpty:
            self.setStyleSheet("background-color: #66FF99; border: 1px solid green")
        else:
            self.setStyleSheet("background-color: #FFCCCB; border: 1px solid red")
        
        

class Componente(QWidget):
    # Es un campo obligatorio. Checar estado focus. Si entro y coloco texto, se pone verde el borde y el *. Si entra y no pone nada, se pone rojo.
    # css en pyside6?
    def __init__(self):
        super().__init__()
        
        mainHLayout = QHBoxLayout(self)
        
        # self.editWithNoChanges = Signal()
        
        self.lineEdit = RequiredLineEdit()
        
        mainHLayout.addWidget(self.lineEdit)
        mainHLayout.addWidget(QLabel("*"))
        
        self.lineEdit.setFocusPolicy(Qt.TabFocus | Qt.ClickFocus)
        # self.lineEdit.editingFinished.connect(self.changeStyles)