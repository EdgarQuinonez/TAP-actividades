import sys, os
from PySide6.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QTableWidget,
    QMenuBar,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QMessageBox,
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QFileDialog,
    QAbstractItemView,
    QDialogButtonBox,
    QLabel
)
from PySide6.QtCore import Qt, QRegularExpression, QMimeData
from PySide6.QtGui import QRegularExpressionValidator, QAction

from contacto import Contacto

class VentanaPrincipal(QMainWindow):
    def __init__(self, centralWidget):
        """
        Constructor
        """
        super().__init__()
        self.setWindowTitle("Agenda")
        self.tablaRef = centralWidget
        self.setCentralWidget(self.tablaRef)
        
        
        self.setMinimumSize(500, 600)

        # Actions

        importAction = QAction("&Importar", self)
        importAction.setShortcut("Ctrl+I")
        importAction.triggered.connect(lambda: self.importarDatos(self.tablaRef))

        exportAction = QAction("&Exportar", self)
        exportAction.setShortcut("Ctrl+E")
        exportAction.triggered.connect(lambda: self.tablaRef.onExportar(self))
        


        # Components
        menuBar = QMenuBar(self)
        menuItemDatos = QMenu("&Datos")
        menuItemDatos.addAction(importAction)
        menuItemDatos.addAction(exportAction)
        menuItemAyuda = QMenu("&Ayuda")
        menuItemAyuda.addAction("&Acerca de...", self.abrirAcerca)

        menuBar.addMenu(menuItemDatos)
        menuBar.addMenu(menuItemAyuda)

        self.setMenuBar(menuBar)

    def importarDatos(self, tablaRef):
        dialogo = QFileDialog(self)
        dialogo.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialogo.setNameFilter("Contactos separados por comas (*.csv)")
        dialogo.setViewMode(QFileDialog.ViewMode.List)

        if dialogo.exec():
            archivo = dialogo.selectedFiles()[0]
            if archivo.endswith(".csv"):
                self.read_csv(archivo, tablaRef)
            elif archivo.endswith(".xls") or archivo.endswith(".xlsx"):
                self.read_excel(archivo)
            else:
                QMessageBox.warning(self, "Error", "Unsupported file type.")

    def exportarDatos(self, tablaRef):
        try:                    
            open('contactos_export.csv', "w").close()        
            with open('contactos_export.csv', "a", encoding = 'utf-8') as f:
                for row in range(tablaRef.tabla.rowCount()):
                    fileData = tablaRef.tabla.item(row, 0).data(Qt.UserRole)                    
                    f.write(f"{fileData["paterno"]},{fileData["materno"]},{fileData["nombres"]},{fileData["telefono"]},{fileData["sexo"]}\n")                
                    
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error writting CSV: {e}")

    def abrirAcerca(self):
        QMessageBox.information(
            self, "Acerca de", "<p>Hecho por EOBL.</p><p>Materia de TAP.</p>"
        )

    def read_csv(self, archivo, tablaRef):
        try:
            with open(archivo, encoding = 'utf-8') as f:
                file = f.readlines()
                contactos = []
                for row in file:
                    
                        
                    rowItems = row.split(',')        
                    strippedRowItems = [item.strip() for item in rowItems]                    
                    
                    contacto = {
                        'paterno': strippedRowItems[0],
                        'materno': strippedRowItems[1],
                        'nombres': strippedRowItems[2],
                        'telefono': strippedRowItems[3],
                        'sexo': strippedRowItems[4],
                    }
                    contactos.append(Contacto(contacto)) 
                    
                tablaRef.agregarContactos(contactos)
                  
                    
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error reading CSV: {e}")

    def read_excel(self, archivo):
        pass
        # try:
        #     df = pd.read_excel(archivo)
        #     for index, row in df.iterrows():
        #         print(row)  # Process each line here
        # except Exception as e:
        #     QMessageBox.warning(self, "Error", f"Error reading Excel: {e}")


class Tabla(QWidget):
    """ """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Nombre completo", "Teléfono", "Sexo"])
        addBtn = QPushButton("Añadir")
        self.deleteBtn = QPushButton("Eliminar")
        
        # Actions
        
        deleteAction = QAction("Eliminar", self)
        deleteAction.setShortcut("Delete")
        deleteAction.triggered.connect(self.deleteSelectedRows)
        
        self.deleteBtn.addAction(deleteAction)
       

        # Layouts
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.tabla)

        self.tabla.setColumnWidth(0, 240)
        self.tabla.setColumnWidth(1, 120)
        self.tabla.setColumnWidth(2, 50)

        # Botones layout
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(addBtn, alignment=Qt.AlignLeft)
        btnLayout.addWidget(self.deleteBtn, alignment=Qt.AlignRight)

        mainLayout.addLayout(btnLayout)

        # Listeners
        self.tabla.itemDoubleClicked.connect(self.handleCellDoubleClick)
        self.tabla.itemSelectionChanged.connect(self.onSelectionChanged)
        addBtn.clicked.connect(self.onAgregarContacto)
        self.deleteBtn.clicked.connect(self.deleteSelectedRows)

        # Flags?
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        if len(self.tabla.selectedItems()) == 0:
            self.deleteBtn.setDisabled(True)
            
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def agregarContactos(self, contactos):
        
        filteredContactos = [contacto for contacto in contactos if self.isNonDuplicate(contacto)]        
        duplicatesCount = len(contactos) - len(filteredContactos)
        
        if duplicatesCount == 0:
            numRows = self.tabla.rowCount()
            self.tabla.setRowCount(numRows + len(filteredContactos))
            
            for contacto in filteredContactos:
                formData = contacto.prettyData()
                fileData = contacto.normalizeData()
                
                
                itemNombreCompleto = QTableWidgetItem(formData["nombreCompleto"])
                itemNombreCompleto.setData(Qt.UserRole, fileData)

                self.tabla.setItem(numRows, 0, itemNombreCompleto)
                self.tabla.setItem(numRows, 1, QTableWidgetItem(formData["telefono"]))
                self.tabla.setItem(numRows, 2, QTableWidgetItem(formData["sexo"]))
                self.tabla.selectRow(itemNombreCompleto.row())                    
                
                numRows += 1            
                
            self.tabla.sortByColumn(0, Qt.SortOrder.AscendingOrder)            
            
        else:            
            QMessageBox.warning(self, f"{duplicatesCount} Elemento(s) duplicados no agregados", f"No se pudieron agregar {duplicatesCount} elementos duplicados. Ya existe un contacto con el mismo nombre.")
                
             
    def isNonDuplicate(self, contacto):
        formData = contacto.prettyData()
        for row in range(self.tabla.rowCount()):            
            nombreCompletoItem = self.tabla.item(row, 0)
            if nombreCompletoItem.text() == formData["nombreCompleto"]:
                return False                    
        return True
             
    def onAgregarContacto(self):
        form = FrmAgregar(self)
        form.open()
        
    def onExportar(self, parent):
        dialog = ExportDialog(self)
        if dialog.exec():
           parent.exportarDatos(self)
    
        


    def handleCellDoubleClick(self, item):
        # Imprime contenido de cualquier celda
        # self.tabla.selectRow(item.row())
        # print(item.text())
        # Imprime nombre, desde cualquier celda
        print(self.tabla.item(item.row(), 0).text())

    def deleteSelectedRows(self):
        selectedRows = list(set(item.row() for item in self.tabla.selectedItems()))

        for row in sorted(selectedRows, reverse=True):
            self.tabla.removeRow(row)

    def onSelectionChanged(self):
        if len(self.tabla.selectedItems()) > 0:
            self.deleteBtn.setDisabled(False)
        else:
            self.deleteBtn.setDisabled(True)

    def editItem(self):
        pass


class FrmAgregar(QDialog):
    def __init__(self, tablaRef):
        """
        Constructor
        """
        super().__init__(tablaRef)

        self.setWindowTitle("Agregar contacto")

        # components

        self.lePaterno = QLineEdit()
        self.leMaterno = QLineEdit()
        self.leNombres = QLineEdit()
        self.leTelefono = QLineEdit()

        self.comboBoxSexo = QComboBox()
        self.comboBoxSexo.addItem("Masculino")
        self.comboBoxSexo.addItem("Femenino")
        self.comboBoxSexo.setPlaceholderText("--Seleccionar--")
        self.comboBoxSexo.setCurrentIndex(-1)

        self.btnAceptar = QPushButton("Aceptar")
        self.btnCancelar = QPushButton("Cancelar")

        # Layouts
        mainLayout = QVBoxLayout(self)
        formLayout = QFormLayout()
        btnHLayout = QHBoxLayout()

        btnHLayout.addWidget(self.btnAceptar)
        btnHLayout.addWidget(self.btnCancelar)

        formLayout.addRow("Apellido Paterno", self.lePaterno)
        formLayout.addRow("Apellido Materno", self.leMaterno)
        formLayout.addRow("Nombre(s)", self.leNombres)
        formLayout.addRow("Teléfono", self.leTelefono)
        formLayout.addRow("Sexo", self.comboBoxSexo)

        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(btnHLayout)

        # Listeners
        self.btnAceptar.clicked.connect(lambda: self.handleAgregar(tablaRef))
        self.btnCancelar.clicked.connect(lambda: self.reject())

        # Regex
        textRegex = QRegularExpression("[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ\s]+")
        textValidator = QRegularExpressionValidator(textRegex)

        self.lePaterno.setValidator(textValidator)
        self.leMaterno.setValidator(textValidator)
        self.leNombres.setValidator(textValidator)

        # Input mask
        self.leTelefono.setInputMask("999-999-9999")

        # placeholders
        self.lePaterno.setPlaceholderText("ej. Quiñónez")
        self.leMaterno.setPlaceholderText("ej. Ramos")
        self.leNombres.setPlaceholderText("ej. Edgar Felipe")

    def validarCampos(self):
        if self.lePaterno.text() == "":
            self.lePaterno.setFocus()
            return False

        elif self.leMaterno.text() == "":
            self.leMaterno.setFocus()
            return False
        elif self.leNombres.text() == "":
            self.leNombres.setFocus()
            return False
        elif self.leTelefono.text() == "":
            self.leTelefono.setFocus()
            return False
        elif self.comboBoxSexo.currentIndex() == -1:
            self.comboBoxSexo.showPopup()
            return False

        return True

    def handleAgregar(self, tablaRef):
        success = self.validarCampos()
        formData = {
            "paterno": self.lePaterno.text(),
            "materno": self.leMaterno.text(),
            "nombres": self.leNombres.text(),
            "telefono": self.leTelefono.text(),
            "sexo": self.comboBoxSexo.currentIndex(),
        }

        if success:
            # cargar contacto desde clase, ya normalizado?
            contacto = [Contacto(formData)]
            tablaRef.agregarContactos(contacto)
            self.accept()

        else:
            QMessageBox.critical(
                self, "Error al enviar el formulario", "Rellena todos los campos"
            )
            
            
class ExportDialog(QDialog):
   def __init__(self, parent=None):
       super().__init__(parent)

       self.setWindowTitle("My Dialog")

       # Add more dialog content as needed (labels, text fields, etc.)

       button_box = QDialogButtonBox(
           QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
           Qt.Horizontal,
           self,
       )
       button_box.accepted.connect(self.accept)
       button_box.rejected.connect(self.reject)

       main_layout = QVBoxLayout()
       textLbl = QLabel("¿Deseas exportar el archivo (.csv)?")
       main_layout.addWidget(textLbl)
       main_layout.addWidget(button_box)
       self.setLayout(main_layout)


# Punto de inicio de ejecución del programa:
if __name__ == "__main__":
    app = QApplication([])

    widget = VentanaPrincipal(Tabla())
    widget.show()

    sys.exit(app.exec())
