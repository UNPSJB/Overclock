from django.db import models
from core.models import Vendedor, Cliente
from hotel.models import Habitacion, PaqueteTuristico

class Factura(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    # Tipo, Monto
    fecha = models.DateField()
    #total = models.DecimalField(max_digits=20, decimal_places=2)

    def total(self):
        return "EL TOTAL" # Para cada alquiler el total del alquiler

# Alquiler
class Alquiler(models.Model):
    habitaciones = models.ManyToManyField(Habitacion)
    paquete = models.ForeignKey(PaqueteTuristico, null=True, on_delete=models.NULL)
    factura = models.ForeignKey(Factura, related_name="alquileres", null=True, on_delete=models.NULL)
    #cantidad_huespedes
    inicio = models.DateField()
    fin = models.DateField()

    @classmethod
    def alquilar_paquete(cls, paquete):
        return cls(habitaciones=paquete.habitaciones, inicio=paquete.inicio, fin=paquete.fin)

    def total(self):
        return "EL TOTAL" # Calcular cada habitacion por temporada y aplicar descuentos del hotel y si tiene paquete decuento 


# Venta Paquete Turistico
# Liquidar Comision