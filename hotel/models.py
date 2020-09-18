from django.db import models
from core.models import Localidad, Categoria, Servicio, TipoHabitacion

# Habitación
class Habitacion(models.Model):
    #Piso, Numero
    pass

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
    habitaciones = models.ManyToManyField(Habitacion, through='HabitacionHotel', through_fields=('hotel', 'habitacion'))

class HabitacionHotel(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE)
    alta = models.DecimalField(max_digits=20, decimal_places=2)
    baja = models.DecimalField(max_digits=20, decimal_places=2)

# Temporada Alta
class TemporadaAlta(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=800)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    inicio = models.DateField()
    fin = models.DateField()

# Descuentos
class Descuento(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    cantidad = models.PositiveSmallIntegerField()
    coeficiente = models.DecimalField(max_digits=3, decimal_places=2)

# Paquete Turistico
class PaqueteTuristico(models.Model):
    nombre = models.CharField(max_length=200)
    coeficiente = models.DecimalField(max_digits=3, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    inicio = models.DateField()
    fin = models.DateField()
    habitaciones = models.ManyToManyField(Habitacion)
