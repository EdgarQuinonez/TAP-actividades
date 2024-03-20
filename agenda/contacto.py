class Contacto:
    def __init__(self, formData):
        self.paterno = formData["paterno"]
        self.materno = formData["materno"]
        self.nombres = formData["nombres"]
        self.telefono = formData["telefono"]
        self.sexo = formData["sexo"]

    def prettyData(self):
        prettyData = {
            "nombreCompleto": f"{self.paterno} {self.materno} {self.nombres}",
            "telefono": self.telefono,
            "sexo": self.sexo,
        }
        return prettyData

    def normalizeData(self):
        normalizedData = {
            "paterno": self.paterno,
            "materno": self.materno,
            "nombres": self.nombres,
            "telefono": f"{self.telefono[0:3] + self.telefono[3:6] + self.telefono[6:]}",
            "sexo": "m" if self.sexo == "Masculino" else "f",
        }

        return normalizedData
