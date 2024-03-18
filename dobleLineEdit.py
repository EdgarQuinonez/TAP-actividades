import sys
from PySide6.QtWidgets import QWidget, QApplication, QLineEdit, QVBoxLayout
from PySide6.QtCore import Qt 





class Formulario(QWidget):
    """

    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setWindowTitle("Espejo")

        mainLayout = QVBoxLayout(self)

        self.lineEdit1 = MyLineEdit(self)
        self.lineEdit2 = MyLineEdit(self)

        self.lineEdit2.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        mainLayout.addWidget(self.lineEdit1)
        mainLayout.addWidget(self.lineEdit2)

    def reflejarTexto(self, lineEdit: QLineEdit):
        texto = lineEdit.text()
        self.lineEdit2.setText(texto)


class MyLineEdit(QLineEdit):

    def __init__(self, padre: Formulario):
        """
        Constructor
        """
        super().__init__(padre)

        self.padre = padre        

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.padre.reflejarTexto(self)
        


        
        

# Punto de inicio de ejecución del programa:
if __name__ == "__main__":
    app = QApplication([])

    widget = Formulario()
    widget.show()

    sys.exit(app.exec())