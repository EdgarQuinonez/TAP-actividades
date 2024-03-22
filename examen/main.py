import sys
from PySide6.QtWidgets import QWidget, QApplication, QTableWidget, QComboBox, QLabel, QVBoxLayout, QHBoxLayout, QTableWidgetItem
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class Operaciones(QWidget):
    """

    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setWindowTitle("Operaciones")
        self.setFixedSize(250, 400)
        # components operacion
        self.numIzq = "0"
        self.numDer = "0"
        self.op = "+"
        self.result = "0"
        
        
  
        
        # Components
        self.cbOperacion = QComboBox()
        
        self.tablaIzq = QTableWidget()
        self.tablaDer = QTableWidget()
        
        self.lblOperacion = QLabel(f'{self.numIzq} {self.op} {self.numDer} = {self.result}')
        
        # Fonts
        lblFont = QFont()
        lblFont.setPointSize(15)
        lblFont.setBold(True)
        self.lblOperacion.setFont(lblFont)
        
        # Layouts
        self.mainVLayout = QVBoxLayout(self)
        self.tablesHLayout = QHBoxLayout()
        
        self.mainVLayout.addWidget(self.cbOperacion)
        self.mainVLayout.addLayout(self.tablesHLayout)
        
        self.tablesHLayout.addWidget(self.tablaIzq)
        self.tablesHLayout.addWidget(self.tablaDer)
        
        self.mainVLayout.addWidget(self.lblOperacion)
        
        # Alignments
        self.lblOperacion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Configurar tablas
        self.tablaIzq.setRowCount(1001)
        self.tablaDer.setRowCount(1001)
        self.tablaIzq.setColumnCount(1)
        self.tablaDer.setColumnCount(1)
        
        for row in range(0, 1001):
            # self.tablaIzq.setRowCount(row + 1)
            # self.tablaDer.setRowCount(row + 1)
            tablaIzqItem = QTableWidgetItem(str(row))
            tablaDerItem = QTableWidgetItem(str(row))
            self.tablaIzq.setItem(row, 0, tablaIzqItem)
            self.tablaDer.setItem(row, 0, tablaDerItem)
        
        # Seleccion simple
        # self.tablaIzq.setSelectionMode()
        
        # Configurar combo
        self.cbOperacion.addItem('Sumar')
        self.cbOperacion.addItem('Restar')
        self.cbOperacion.addItem('Multiplicar')
        self.cbOperacion.addItem('Dividir')
        
        # Listeners
        # segun la operacion seleccionada
        self.cbOperacion.currentTextChanged.connect(self.setLblOperation)
        
        # segun los numeros seleccionados
        self.tablaIzq.itemClicked.connect(self.setLblOperationNumberIzq)
        self.tablaDer.itemClicked.connect(self.setLblOperationNumberDer)
        
        
    def setLblOperation(self, text):
        if text == "Sumar":
            self.op = "+"
            self.lblOperacion.setText(f'{self.numIzq} {self.op} {self.numDer} = {self.result}')
        elif text == "Restar":
            self.op = "-"
            self.lblOperacion.setText(f'{self.numIzq} {self.op} {self.numDer} = {self.result}')
        elif text == "Multiplicar":
            self.op = "*"
            self.lblOperacion.setText(f'{self.numIzq} {self.op} {self.numDer} = {self.result}')
        elif text == "Dividir":
            self.op = "/"
            self.lblOperacion.setText(f'{self.numIzq} {self.op} {self.numDer} = {self.result}')
            
        self.setResult()
            
    def setLblOperationNumberIzq(self, item):
        self.numIzq = item.text()
        self.setResult()
        
        
    def setLblOperationNumberDer(self, item):
        self.numDer = item.text()
        self.setResult()
        
    def setResult(self):
        if self.cbOperacion.currentText() == "Sumar":
            self.result = int(self.numIzq) + int(self.numDer)
        elif self.cbOperacion.currentText() == "Restar":
            self.result = int(self.numIzq) - int(self.numDer)
        elif self.cbOperacion.currentText() == "Multiplicar":
            self.result = int(self.numIzq) * int(self.numDer)
        elif self.cbOperacion.currentText() == "Dividir":
            if self.numDer != "0":
                self.result = int(self.numIzq) / int(self.numDer)
            else:
                self.lblOperacion.setText("Division por cero")
                return

        
        self.lblOperacion.setText(f'{self.numIzq} {self.op} {self.numDer} = {self.result}')
        
            
    
            
            
            
        


# Punto de inicio de ejecución del programa:
if __name__ == "__main__":
    app = QApplication([])

    widget = Operaciones()
    widget.show()

    sys.exit(app.exec())