from django.conf import settings
from django.db import models
from decimal import Decimal
from core.models import Vendedor, Cliente
from hotel.models import Habitacion, PaqueteTuristico
from .exceptions import MaxPasajerosException

# Liquidar Comision
class Liquidacion(models.Model):
    fecha = models.DateField(auto_now_add=True)
    abonado = models.DateField(null=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=20, decimal_places=2)

    def abonada(self):
        return self.abonado != None

    @staticmethod
    def generar_para_vendedor(vendedor):
        facturas = Factura.objects.filter(liquidacion__isnull=True, vendedor=vendedor)
        total = sum([f.total() for f in facturas]) * vendedor.coeficiente
        liquidacion = Liquidacion.objects.create(total=total, vendedor=vendedor)
        for f in facturas:
            f.liquidacion = liquidacion
            f.save()
        return liquidacion

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    liquidacion = models.ForeignKey(Liquidacion, null=True, blank=True, on_delete=models.SET_NULL)
    # medio_de_pago
    # Tipo, Monto
    fecha = models.DateField(auto_now_add=True)

    def alquilar_habitaciones(self, habitaciones_con_fecha):
        alquileres = []
        for (habitacion, huespedes, desde, hasta) in habitaciones_con_fecha:
            alquiler = self.alquilar_habitacion(habitacion, huespedes, desde, hasta)
            if alquiler not in alquileres:
                alquileres.append(alquiler)
        return alquileres 

    def alquilar_habitacion(self, habitacion, huespedes, desde, hasta, paquete = None):
        if huespedes > habitacion.tipo.pasajeros + settings.TOLERANCIA_PASAJEROS:
            #TODO: Custom exception
            raise MaxPasajerosException(f"No puede superar la cantidad de pasajeros permitida: {habitacion.tipo.pasajeros}")
        hotel = habitacion.hotel
        alquiler = self.alquileres.filter(habitaciones__hotel__in=[hotel], inicio=desde, fin=hasta).first()
        if alquiler is None:
            alquiler = Alquiler.objects.create(cantidad_huespedes=huespedes, inicio=desde, fin=hasta, factura=self, paquete=paquete)
        alquiler.habitaciones.add(habitacion)
        descuento = hotel.obtener_descuento(alquiler.habitaciones.all())
        alquiler.total = sum([h.precio_alquiler(desde, hasta) for h in alquiler.habitaciones.all()])
        alquiler.total -= alquiler.total * descuento.coeficiente
        alquiler.save()
        #TODO: Aplicar descuento
        return alquiler

    def alquilar_paquete(self, paquete, huespedes):
        for index, habitacion in enumerate(paquete.habitaciones.all()):
            alquiler = self.alquilar_habitacion(habitacion, huespedes[index], paquete.inicio, paquete.fin, paquete=paquete) 
        alquiler.total -= alquiler.total * paquete.coeficiente
        alquiler.save()
        return alquiler
    
    def total(self):
        return sum([a.total for a in self.alquileres.all()])

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
