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
    def __init__(self, placeholderText="", specialChar="*", fontFamilyName="Arial", fontSizeBase=16, fontSizeScale=1.5):
        super().__init__()
        
        mainHLayout = QHBoxLayout(self)

        self.__lineEdit = RequiredLineEdit()
        self.__specialChar = QLabel(specialChar)
        
        # Set fonts
        self.lineEditFont = QFont(fontFamilyName)
        self.lineEditFont.setPointSize(fontSizeBase)
        self.labelFont = QFont(fontFamilyName)
        self.labelFont.setPointSize(fontSizeBase * fontSizeScale)
        
        self.__lineEdit.setFont(self.lineEditFont)
        self.__specialChar.setFont(self.labelFont)
        
        # Layout
        mainHLayout.addWidget(self.__lineEdit)
        mainHLayout.addWidget(self.__specialChar)
        
        self.__lineEdit.setFocusPolicy(Qt.TabFocus | Qt.ClickFocus)
        
        # lineEdit placeholder
        self.__lineEdit.setPlaceholderText(placeholderText)
        
        # Listeners
        self.__lineEdit.focusOut.connect(self.changeStyles)
        # Evaluación inicial
        self.changeStyles()
        
    def changeSpecialChar(self, newSpecialChar: str):
        self.__specialChar.setText((newSpecialChar))
        
    def changeFontScale(self, newFontScale):
        self.labelFont.setPointSize(self.lineEditFont.pointSize() * newFontScale)
        self.__specialChar.setFont(self.labelFont)
    
    def changePlaceholderText(self, newPlaceholderText):        
        self.__lineEdit.setPlaceholderText(newPlaceholderText)
    
    # Conocer estado del componente
    def checkNotEmpty(self):
        if self.__lineEdit.text().strip() != "":
            return True
        else:
            return False
        
    def setFocusOnInvalid(self):
        if self.checkNotEmpty() == False:            
            self.__lineEdit.setFocus()
        
    def changeStyles(self):
        isNotEmpty = self.checkNotEmpty()
        
        if isNotEmpty:
            self.__lineEdit.setStyleSheet("background-color: #66FF99; border: 1px solid green")
            self.__specialChar.setStyleSheet("color: green")
        else:
            self.__lineEdit.setStyleSheet("background-color: #FFCCCB; border: 1px solid red")
            self.__specialChar.setStyleSheet("color: red")
