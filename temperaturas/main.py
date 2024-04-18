# pycountry nombres y codigos
# geopy coordenadas
# meteostat obtener datos de temperatura promedio por dia en un intervalo de fechas
# matplotlib grafica


import sys
import os
import csv
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QComboBox, QHBoxLayout, QLabel, QPushButton, QDateEdit
from PySide6.QtCore import QDate
import pycountry
from meteostat import Point, Daily
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from datetime import datetime




class HistoricoTemperatura(QWidget):
    """

    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setWindowTitle("Histórico de Temperaturas")
        
        self.selectedCountry = None
        self.selectedState = None
        self.selectedCity = None
        
        # Layout
        self.mainVLayout = QVBoxLayout(self)
        headerHLayout = QHBoxLayout()
        
        self.mainVLayout.addLayout(headerHLayout)
        
        # Header H layout components
        
        locationVLayout = QVBoxLayout()
        dateIntervalHLayout = QHBoxLayout()
        dateAndButtonLayout = QVBoxLayout()
        
        headerHLayout.addLayout(locationVLayout)
        headerHLayout.addLayout(dateAndButtonLayout)
        
        # Location components
        
        self.countryCB = QComboBox()
        self.stateCB = QComboBox()
        self.cityCB = QComboBox()
        
        countryRowLayout = QHBoxLayout()
        
        countryRowLayout.addWidget(QLabel("País"))
        countryRowLayout.addWidget(self.countryCB)
        
        stateRowLayout = QHBoxLayout()
        
        stateRowLayout.addWidget(QLabel("Estado"))
        stateRowLayout.addWidget(self.stateCB)
        
        cityRowLayout = QHBoxLayout()
        
        cityRowLayout.addWidget(QLabel("Ciudad"))
        cityRowLayout.addWidget(self.cityCB)
        
        locationVLayout.addLayout(countryRowLayout)
        locationVLayout.addLayout(stateRowLayout)
        locationVLayout.addLayout(cityRowLayout)
        
        # Start-End Date layout
        startDateVLayout = QVBoxLayout()
        endDateVLayout = QVBoxLayout()
        self.startDate =  QDateEdit()
        self.endDate = QDateEdit()
        
        # setup QDateEdits
        date = QDate()
        self.startDate.setMaximumDate(date.currentDate())
        self.endDate.setMaximumDate(date.currentDate())
        
        self.endDate.setDate(date.currentDate())
        self.startDate.setDate(date.currentDate().addDays(-7))
        
        startDateVLayout.addWidget(QLabel("Fecha de Inicio"))
        startDateVLayout.addWidget(self.startDate)
        endDateVLayout.addWidget(QLabel("Fecha final"))
        endDateVLayout.addWidget(self.endDate)
        
        dateIntervalHLayout.addLayout(startDateVLayout)
        dateIntervalHLayout.addLayout(endDateVLayout)
        
        # Boton graficar
        btnVLayout = QVBoxLayout()
        self.graficarBtn = QPushButton("Graficar")
        btnVLayout.addWidget(self.graficarBtn)
        
        dateAndButtonLayout.addLayout(dateIntervalHLayout)
        dateAndButtonLayout.addLayout(btnVLayout)
        
        # Listeners
        self.countryCB.currentIndexChanged.connect(self.onCountrySelectionChanged)
        self.stateCB.currentIndexChanged.connect(self.onStateSelectionChanged)
        self.cityCB.currentIndexChanged.connect(self.onCitySelectionChanged)
        self.graficarBtn.clicked.connect(self.setupPlot)
        
        self.setupCountries()
        # self.setupStates()
        # self.setupCities()
        self.figure = Figure(figsize=(7,8))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.mainVLayout.addWidget(self.canvas)
        
        
        
    def setupCountries(self):
        countries = list(pycountry.countries)
        
        for country in countries:
            self.countryCB.addItem(country.name, country)
        self.countryCB.setCurrentIndex(self.countryCB.findText('Mexico'))
        self.selectedCountry = self.countryCB.itemData(self.countryCB.currentIndex())
            
    def setupStates(self):
        self.stateCB.clear()
        if self.selectedCountry:
            country_object = pycountry.countries.get(alpha_2=self.selectedCountry.alpha_2)            
            subdivisions = pycountry.subdivisions.get(country_code=country_object.alpha_2)

            if subdivisions:
                for subdivision in subdivisions:
                    self.stateCB.addItem(subdivision.name, subdivision)
                
            else:
                print(f"{self.selectedCountry.name} No tiene subdivisiones")
                
    def setupCities(self):
        self.cityCB.clear()
        scriptPath = os.path.dirname(__file__)
        folderPath = os.path.join(scriptPath, 'ciudades')
        citiesCSVFilePath = os.path.join(folderPath, 'cities.csv')
        
        with open(citiesCSVFilePath, 'r', encoding='utf8') as f:
            
            csvReader = csv.reader(f)
            
            if self.selectedCountry and self.selectedState:
                for row in csvReader:
                    stateCode = self.selectedState.country_code + '-' + row[3]
                    if stateCode == self.selectedState.code:
                        self.cityCB.addItem(row[1], row)
                    
                self.selectedCity = self.cityCB.itemData(self.cityCB.currentIndex())
 
            
    def setupPlot(self):
        
        
        city = Point(float(self.selectedCity[8]), float(self.selectedCity[9]))
        
        start = datetime(self.startDate.date().year(), self.startDate.date().month(), self.startDate.date().day())
        end = datetime(self.endDate.date().year(), self.endDate.date().month(), self.endDate.date().day())
        
        data = Daily(city, start, end)
        data = data.fetch()
        
        x = data.index

        y = data['tavg']

        self.figure.clear() 
        ax = self.figure.add_subplot(111) 
        ax.plot(x, y)

        ax.set_xlabel('Día')
        ax.set_ylabel('Temperatura Promedio en C°')
        ax.set_title('Temperatura Promedio en el Intervalo')

        self.canvas.draw()  
        
    def onCountrySelectionChanged(self, index):
        self.selectedCountry = self.countryCB.itemData(index)
        self.setupStates()
        
    def onStateSelectionChanged(self, index):
        self.selectedState = self.stateCB.itemData(index)
        self.setupCities()
        
    def onCitySelectionChanged(self, index):
        self.selectedCity = self.cityCB.itemData(index)
        
        



# Punto de inicio de ejecución del programa:
if __name__ == "__main__":
    app = QApplication([])

    widget = HistoricoTemperatura()
    widget.show()

    sys.exit(app.exec())