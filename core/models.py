from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Pais, Provincia, Localidad
class Pais(models.Model):
    nombre = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Paises"

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre = models.CharField(max_length=200)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class LocalidadManager(models.Manager):
    def crear_zona(self, nombre):
        return self.model.objects.all()

class LocalidadQuerySet(models.QuerySet):
    pass

class Localidad(models.Model):
    objects = LocalidadManager.from_queryset(LocalidadQuerySet)()

    nombre = models.CharField(max_length=200)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Servicios, Categorias
class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=800)

    def __str__(self):
        return self.nombre

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

    def __str__(self):
        return self.nombre

# Tipo De Habitacion
class TipoHabitacion(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=800)
    pasajeros = models.PositiveSmallIntegerField()
    # Cuartos para cuando el tipo es Departamento
    cuartos = models.PositiveSmallIntegerField(default = 0)

    def es_departamento(self):
        return self.cuartos == 0

    def __str__(self):
        return self.nombre

# Las Personas
class Persona(models.Model):
    DNI = 0
    PASAPORTE = 1
    LIBRETA = 2
    TIPOS_DOCUMENTO = (
        (DNI, "DNI"), 
        (PASAPORTE, "PASAPORTE"), 
        (LIBRETA, "LIBRETA")
    )
    tipo_documento = models.PositiveSmallIntegerField(choices=TIPOS_DOCUMENTO)
    documento = models.CharField(max_length=13)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

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

# Usamos patron roles para
# Encargados, Clientes, Vendedores
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

    def __str__(self):
        return f"{self.get_tipo_display()} {self.persona}"

class Encargado(Rol):
    TIPO = 1

    # Clave Autogenerada? un token?
    clave = models.CharField(max_length=10)

class Vendedor(Rol):
    TIPO = 2

    # Coeficiente de Ganancia
    coeficiente = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(0))

class Cliente(Rol):
    TIPO = 3

    # Puntos
    puntos = models.PositiveIntegerField(default=0)

for Klass in [Encargado, Vendedor, Cliente]:
    Rol.register(Klass)
