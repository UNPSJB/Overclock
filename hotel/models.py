from django.db import models
from core.models import Localidad, Categoria, Servicio, TipoHabitacion, Vendedor

# Hotel (Asignar Vendedor)
class Hotel(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=800)
    #TODO: Email
    email = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(Servicio)
    tipos = models.ManyToManyField(TipoHabitacion, through='PrecioPorTipo', through_fields=('hotel', 'tipo'))
    vendedores = models.ManyToManyField(Vendedor)

    def es_hospedaje(self):
        return self.categoria.estrellas in [Categoria.ESTRELLA_A, Categoria.ESTRELLA_B, Categoria.ESTRELLA_C]

    def __str__(self):
        return f"Hospedaje {self.nombre}" if self.es_hospedaje() else f"Hotel {self.nombre}"

class PrecioPorTipo(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE)
    # Precio por noche
    baja = models.DecimalField(max_digits=20, decimal_places=2)
    alta = models.DecimalField(max_digits=20, decimal_places=2)

# Habitación
class Habitacion(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="habitaciones", on_delete=models.CASCADE)
    numero = models.PositiveSmallIntegerField() # 403 <Piso><Cuarto>
    # TODO: Validar que el tipo seleccionado sea un tipo del hotel
    tipo = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('hotel', 'numero'), )

    def __str__(self):
        return f"{self.hotel}, Habitacion: {self.numero}"

# Temporada Alta
class TemporadaAlta(models.Model):
    nombre = models.CharField(max_length=200)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    inicio = models.DateField()
    fin = models.DateField()

# Descuentos
class Descuento(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    # 1 = coeficiente1 = 0 opcionalmente
    # 2 = coeficiente1
    # 3 = coeficiente2
    # 4 = coeficiente3
    # 5 = coeficiente4
    cantidad_habitaciones = models.PositiveSmallIntegerField()
    coeficiente = models.DecimalField(max_digits=3, decimal_places=2)

# Paquete Turistico
class PaqueteTuristico(models.Model):
    nombre = models.CharField(max_length=200)
    coeficiente = models.DecimalField(max_digits=3, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    inicio = models.DateField()
    fin = models.DateField()
    habitaciones = models.ManyToManyField(Habitacion)
