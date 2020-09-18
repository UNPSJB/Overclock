class Rol:
    pass

class Vendedor(Rol):
    def __init__(self):
        self.hoteles = []

    def asignar_hotel(self, hotel):
        self.hoteles.append(hotel)
        print(f"Asignar {hotel}")

class Cliente(Rol):
    def __init__(self, puntos = 0):
        self.puntos = puntos

    def alquilar(self, habitacion):
        self.puntos += 1
        print(f"Alquilando {habitacion}")

class Persona:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        self.roles = []
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    def ser(self, rol):
        self.roles.append(rol)
    
    def __getattr__(self, nombre):
        for rol in self.roles:
            if hasattr(rol, nombre):
                return getattr(rol, nombre)
        return lambda *args, **kwargs: None

if __name__ == "__main__":
    persona = Persona("Brianna", "van Haaster")
    persona.ser(Cliente())
    persona.ser(Vendedor())
    persona.alquilar("PH")
    persona.asignar_hotel("El condor")
    print(persona)

class Person:
    nombre
    apellido
    documento
    tipodocumento

    def __str__(self):
        return "Minombre"

class Rol:
    persona

class Encargado(Rol):
    hotel

class Vendedor(Rol):
    ganancia

class Cliente(Rol):
    ganancia