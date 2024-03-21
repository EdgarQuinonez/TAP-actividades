class Contacto:
    def __init__(self, formData):
        self.paterno = formData["paterno"]
        self.materno = formData["materno"]
        self.nombres = formData["nombres"]
        self.telefono = formData["telefono"]
        self.sexo = formData["sexo"]

    def prettyData(self):
        telefono = self.telefono
        if len(self.telefono) == 10:
            telefono = f'{self.telefono[0:3]}-{self.telefono[3:6]}-{self.telefono[6:]}'
            
        
        sexo = 'masculino' if self.sexo == '0' or self.sexo == 'm' else 'femenino'
        prettyData = {
            "nombreCompleto": f"{self.nombres} {self.paterno} {self.materno}",
            "telefono": telefono,
            "sexo": sexo
        }
        return prettyData

    def normalizeData(self):
        normalizedData = {
            "paterno": self.paterno,
            "materno": self.materno,
            "nombres": self.nombres,
            "telefono": f"{self.telefono[0:3] + self.telefono[3:6] + self.telefono[6:]}",
            "sexo": "m" if self.sexo == '0' or self.sexo == "m" else "f",
        }

        return normalizedData
