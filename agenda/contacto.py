class Contacto:
    def __init__(self, formData):
        self.paterno = formData["paterno"]
        self.materno = formData["materno"]
        self.nombres = formData["nombres"]
        self.telefono = f"{formData["telefono"][0:3] + formData["telefono"][3:6] + formData["telefono"][6:]}"
        self.sexo = "m" if formData["sexo"] == "0" or formData["sexo"] == "m" else "f"

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
        return {
            "paterno": self.paterno,
            "materno": self.materno,
            "nombres": self.nombres,
            "telefono": self.telefono,
            "sexo": self.sexo
        }
