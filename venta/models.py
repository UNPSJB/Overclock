from django.db import models
from decimal import Decimal
from core.models import Vendedor, Cliente
from hotel.models import Habitacion, PaqueteTuristico

# Liquidar Comision
class Liquidacion(models.Model):
    fecha = models.DateField(auto_now_add=True)
    abonado = models.DateField(null=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=20, decimal_places=2)

    def abonada(self):
        return self.abonado != None

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    liquidacion = models.ForeignKey(Liquidacion, null=True, blank=True, on_delete=models.SET_NULL)
    # medio_de_pago
    # Tipo, Monto
    fecha = models.DateField(auto_now_add=True)
    #total = models.DecimalField(max_digits=20, decimal_places=2)

    #def alquilar_paquete(self, paquete):
    #    return Alquiler(habitaciones=paquete.habitaciones, inicio=paquete.inicio, fin=paquete.fin)

    def alquilar_habitaciones_de_hotel(self, hotel, habitaciones, huespedes, desde, hasta):
        total = sum([h.precio_alquiler(desde, hasta) for h in habitaciones])
        alquiler = Alquiler.objects.create(cantidad_huespedes=huespedes, inicio=desde, fin=hasta, factura=self, total=total)
        alquiler.habitaciones.set(habitaciones)
        return alquiler

# Alquiler
class Alquiler(models.Model):
    factura = models.ForeignKey(Factura, related_name="alquileres", on_delete=models.CASCADE)
    # De un mismo hotel
    habitaciones = models.ManyToManyField(Habitacion)
    paquete = models.ForeignKey(PaqueteTuristico, null=True, blank=True, on_delete=models.SET_NULL)
    cantidad_huespedes = models.PositiveSmallIntegerField()
    inicio = models.DateField()
    fin = models.DateField()
    total = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0))
