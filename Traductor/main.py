# Edgar Felipe Quiñónez Ramos 22410043
# Librería: googletrans
# Instalación: pip install googletrans==4.0.0-rc1
# Documentación: https://github.com/ssut/py-googletrans/blob/master/docs/index.rst 

import sys
from PySide6.QtWidgets import QWidget, QApplication, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import Qt
from googletrans import Translator


class Traductor(QWidget):
    """
    
    """


    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setWindowTitle("Traductor")

        self.langList = [['Español', 'es'], ['Inglés', 'en'], ['Alemán', 'de'], ['Japonés', 'ja'], ['Italiano', 'it']]
        self.translator = Translator()
        
        # Components
        self.inputLangCB = QComboBox()
        self.outputLangCB = QComboBox()
        
        self.inputTextEdit = QTextEdit()
        self.outputTextEdit = QTextEdit()
        
        self.outputTextEdit.setReadOnly(True)
        
        self.traducirBtn = QPushButton('Traducir')
        
        # Layout
        self.mainVLayout = QVBoxLayout(self)
        
        self.mainVLayout.addWidget(self.inputLangCB)
        self.mainVLayout.addWidget(self.inputTextEdit)
        
        self.btnHLayout = QHBoxLayout()
        
        self.btnHLayout.addWidget(self.traducirBtn, 1, Qt.AlignmentFlag.AlignRight)
        self.mainVLayout.addLayout(self.btnHLayout)
        
        self.mainVLayout.addWidget(self.outputLangCB)
        self.mainVLayout.addWidget(self.outputTextEdit)
        
        # Añadir los lenguajes
        self.setLanguages()
        
        # Default langs en CBs
        self.inputLangCB.setCurrentIndex(0)
        self.outputLangCB.setCurrentIndex(0)
        
        # Listeners
        self.inputLangCB.currentIndexChanged.connect(self.updateOutputCBLang)
        self.traducirBtn.clicked.connect(self.handleClick)
        
        
    def updateOutputCBLang(self, inputCurrIndex):
        self.outputLangCB.clear()
        for lang in self.langList:
            nombre, _  = lang
            self.outputLangCB.addItem(nombre)
        
        self.outputLangCB.removeItem(inputCurrIndex)
        
    def setLanguages(self):
        self.inputLangCB.clear()
        self.outputLangCB.clear()
        # Añadir lenguajes a los CB
        for lang in self.langList:
            nombre, _  = lang
            self.inputLangCB.addItem(nombre)
            self.outputLangCB.addItem(nombre)
            
        self.outputLangCB.removeItem(0)    
            
    def translateInput(self, inputText, src, dest):
        translatedObj = self.translator.translate(inputText, src=src, dest=dest)
        outputText = translatedObj.text
        
        return outputText
    
    
    def handleClick(self):
        if len(self.inputTextEdit.toPlainText()) > 0:
            _, inputLangCode = self.langList[self.inputLangCB.currentIndex()]
            _, outputLangCode = self.langList[self.getShiftedIndex(self.inputLangCB.currentIndex())]
            
            translatedText = self.translateInput(self.inputTextEdit.toPlainText(), inputLangCode, outputLangCode)
            
            self.outputTextEdit.setText(translatedText)
        
    def getShiftedIndex(self, removedItemIndex):     
        if removedItemIndex <= self.outputLangCB.currentIndex():
            return self.outputLangCB.currentIndex() + 1
        else:
            return self.outputLangCB.currentIndex()
        
        
        
        
        
        
        
        


# Punto de inicio de ejecución del programa:
if __name__ == "__main__":
    app = QApplication([])

    widget = Traductor()
    widget.show()

    sys.exit(app.exec())