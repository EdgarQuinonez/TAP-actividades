import sys
from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QLabel, QGridLayout, QVBoxLayout, \
    QSizePolicy
from casilla import Casilla

class FrmGato(QWidget):
    """

    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")

        # Configuración layout arriba:
        self.btnIniciarX = QPushButton("Iniciar X")
        self.lblTurno = QLabel("Turno")
        self.lblTurno.setFixedWidth(200)
        self.lblTurno.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btnIniciarO = QPushButton("Iniciar O")

        layoutArriba = QHBoxLayout()
        layoutArriba.addWidget(self.btnIniciarX)
        layoutArriba.addWidget(self.lblTurno)
        layoutArriba.addWidget(self.btnIniciarO)

        layoutArriba.setAlignment(Qt.AlignCenter)

        # Configuración layout central:
        layoutCentro = QGridLayout()

        self.listaCasillas = []
        for row in range(3):
            for col in range(3):
                casilla = Casilla(self)
                layoutCentro.addWidget(casilla, row, col)
                self.listaCasillas.append(casilla)
                #btnCasilla.clicked.connect(partial(self.marcar, btnCasilla))


        # Configuración layout abajo:
        self.btnReiniciar = QPushButton("Reiniciar")

        layoutAbajo = QHBoxLayout()
        layoutAbajo.addWidget(self.btnReiniciar)

        layoutAbajo.setAlignment(Qt.AlignCenter)

        # Configuración layout principal:
        layoutPrincipal = QVBoxLayout(self)
        layoutPrincipal.addLayout(layoutArriba)
        layoutPrincipal.addLayout(layoutCentro)
        layoutPrincipal.addLayout(layoutAbajo)

        self.configurar_estado_inicial()

        self.btnIniciarX.clicked.connect(lambda: self.empezar("X"))
        self.btnIniciarO.clicked.connect(lambda: self.empezar("O"))

        # TODO Maximizar el formulario:
        self.showMaximized()

    def configurar_estado_inicial(self):
        self.btnReiniciar.setEnabled(False)

    def empezar(self, turno):
        for btnCasilla in self.listaCasillas:
            btnCasilla.setEnabled(True)

        self.btnReiniciar.setEnabled(True)
        self.btnIniciarX.setEnabled(False)
        self.btnIniciarO.setEnabled(False)

        self.lblTurno.setText(f"Turno de {turno}")

    def marcar(self, casilla):
        if casilla.text() == "":
            if self.lblTurno.text() == "Turno de X":
                casilla.setText("X")
                self.lblTurno.setText("Turno de O")
            else:
                casilla.setText("O")
                self.lblTurno.setText("Turno de X")

    def get_turno(self):
        if self.lblTurno == "Turno de X":
            return "X"
        else:
            return "O"

# Punto de inicio de ejecución del programa:
if __name__ == "__main__":
    app = QApplication([])

    widget = FrmGato()
    widget.show()

    sys.exit(app.exec())