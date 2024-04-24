from PySide6.QtGui import QFocusEvent, QFont
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import Qt, Signal

class RequiredLineEdit(QLineEdit):
    focusOut = Signal(name="focusOut")
    def __init__(self):
        super().__init__()
    
        
        
    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.focusOut.emit()
        super().focusOutEvent(event)
        
    
        
        

class Componente(QWidget):
    # Es un campo obligatorio. Checar estado focus. Si entro y coloco texto, se pone verde el borde y el *. Si entra y no pone nada, se pone rojo.
    # css en pyside6?
    def __init__(self, specialChar="*", fontSizeBase=16, fontSizeScale=1.5):
        super().__init__()
        
        mainHLayout = QHBoxLayout(self)
        
        # self.editWithNoChanges = Signal()
        
        
        self.__lineEdit = RequiredLineEdit()
        self.__specialChar = QLabel(specialChar)
        
        # Set fonts
        self.lineEditFont = QFont("Arial")
        self.lineEditFont.setPointSize(fontSizeBase)
        self.labelFont = QFont("Arial")
        self.labelFont.setPointSize(fontSizeBase * fontSizeScale)
        
        self.__lineEdit.setFont(self.lineEditFont)
        self.__specialChar.setFont(self.labelFont)
        
        mainHLayout.addWidget(self.__lineEdit)
        mainHLayout.addWidget(self.__specialChar)
        
        self.__lineEdit.setFocusPolicy(Qt.TabFocus | Qt.ClickFocus)
        self.__lineEdit.focusOut.connect(self.changeStyles)
        
    def changeSpecialChar(self, newSpecialChar: str):
        self.__specialChar.setText((newSpecialChar))
        
    def changeFontScale(self, newFontScale):
        self.labelFont.setPointSize(self.lineEditFont.pointSize() * newFontScale)
        self.__specialChar.setFont(self.labelFont)
        
    def checkNotEmpty(self):
        if self.__lineEdit.text() != "":
            return True
        else:
            return False
        
    def changeStyles(self):
        isNotEmpty = self.checkNotEmpty()
        
        if isNotEmpty:
            self.__lineEdit.setStyleSheet("background-color: #66FF99; border: 1px solid green")
        else:
            self.__lineEdit.setStyleSheet("background-color: #FFCCCB; border: 1px solid red")
        