from django.shortcuts import get_object_or_404
from hotel.models import Hotel, Habitacion

class Carrito:
    def __init__(self,request):
        self.request=request
        self.session=request.session
        carrito=self.session.get("carrito")
        if not carrito:
            carrito=self.session["carrito"]={}
        self.carrito=carrito

    def agregar_habitacion(self,habitacion,desde,hasta):
        habitacion=get_object_or_404(Habitacion,pk=habitacion)
        if str(habitacion.pk) not in self.carrito.keys():
            self.carrito[habitacion.pk]={
                "habitacion_pk":habitacion.pk,
                "hotel_pk":habitacion.hotel,
                "habitacion_numero":habitacion.numero,
                "habitacion_precio":str(habitacion.precio_alquiler(desde,hasta)),
             }
        self.save()

    def save(self):
        self.session["carrito"]=self.carrito
        self.session.modified=True
    
    def quitar_habitacion(self, habitacion):
        if habitacion in self.carrito:
            del self.carrito[habitacion]
            self.save()

    