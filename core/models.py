from django.db import models

# Pais, Provincia, Localidad
class Pais(models.Model):
    nombre = models.CharField(max_length=200)

class Provincia(models.Model):
    nombre = models.CharField(max_length=200)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

class Localidad(models.Model):
    nombre = models.CharField(max_length=200)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

# Servicios, Categorias
class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=800)

class Categoria(models.Model):
    ESTRELLA_A = 0
    ESTRELLA_B = 1
    ESTRELLA_C = 2
    ESTRELLA_1 = 3
    ESTRELLA_2 = 4
    ESTRELLA_3 = 5
    ESTRELLA_4 = 6
    ESTRELLA_5 = 7
    ESTRELLAS = (
        (ESTRELLA_A, "A"), 
        (ESTRELLA_B, "B"), 
        (ESTRELLA_C, "C"), 
        (ESTRELLA_1, "Tourist"), 
        (ESTRELLA_2, "Standard"), 
        (ESTRELLA_3, "Comfort"), 
        (ESTRELLA_4, "First Class"), 
        (ESTRELLA_5, "Luxury"), 
    )
    estrellas = models.PositiveSmallIntegerField(choices=ESTRELLAS)
    nombre = models.CharField(max_length=200)
    servicios = models.ManyToManyField(Servicio)

# Tipo De Habitacion
class TipoHabitacion(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=800)
    tipo_documento = models.PositiveSmallIntegerField()

# Encargados, Clientes, Vendedores
class Persona(models.Model):
    tipo_documento = models.PositiveSmallIntegerField() # 0 - 32767
    documento = models.CharField(max_length=13)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)

    def __str__(self):
        return "{0}, {1}".format(self.apellido, self.nombre)

    def como(self, Klass):
        return self.roles.get(tipo=Klass.TIPO).related()

    def agregar_rol(self, rol):
        if not self.sos(rol.__class__):
            rol.persona = self
            rol.save()

    def roles_related(self):
        return [rol.related() for rol in self.roles.all()]

    def sos(self, Klass):
        return any([isinstance(rol, Klass) for rol in self.roles_related()])

class Rol(models.Model):
    TIPO = 0
    TIPOS = [
        (0, "rol")
    ]
    persona = models.ForeignKey(Persona, related_name="roles", on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.tipo = self.__class__.TIPO
        super(Rol, self).save(*args, **kwargs)

    def related(self):
        return self.__class__ != Rol and self or getattr(self, self.get_tipo_display())

    @classmethod
    def register(cls, klass):
        cls.TIPOS.append((klass.TIPO, klass.__name__.lower()))

class Encargado(Rol):
    TIPO = 1
    # Clave 

class Vendedor(Rol):
    TIPO = 2
    # Coeficiente de Ganancia

class Cliente(Rol):
    TIPO = 3
    # Puntos

for Klass in [Encargado, Vendedor, Cliente]:
    Rol.register(Klass)
