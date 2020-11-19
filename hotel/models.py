from django.db import models
from decimal import Decimal
from datetime import date, datetime, timedelta
from core.models import Localidad, Categoria, Servicio, TipoHabitacion, Vendedor, Encargado
from .exceptions import DescuentoException, TipoHotelException

class HotelManager(models.Manager):
    def en_zona(self, zona):
        return self.model.objects.filter(localidad__in=zona)

class HotelQuerySet(models.QuerySet):
    pass

# Hotel (Asignar Vendedor)
class Hotel(models.Model):
    objects = HotelManager.from_queryset(HotelQuerySet)()
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=800)
    #TODO: Email
    email = models.EmailField(max_length=200)
    telefono = models.CharField(max_length=200)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)
    encargado= models.ForeignKey(Encargado, on_delete=models.CASCADE, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(Servicio)
    tipos = models.ManyToManyField(TipoHabitacion, through='PrecioPorTipo', through_fields=('hotel', 'tipo'))
    vendedores = models.ManyToManyField(Vendedor)
   

    def tengo_tipos(self):
        return self.tipos.count()>0

    def es_comercializable(self):
        return self.vendedores.count() > 0

    def es_hospedaje(self):
        return self.categoria.estrellas in [Categoria.ESTRELLA_A, Categoria.ESTRELLA_B, Categoria.ESTRELLA_C]

    def __str__(self):
        return f"Hospedaje {self.nombre}" if self.es_hospedaje() else f"Hotel {self.nombre}"

    def agregar_habitacion(self, tipo, numero):
        # TODO: Validar que el tipo seleccionado sea un tipo del hotel
        if not self.tipos.filter(pk=tipo.pk).exists():
            raise TipoHotelException(f"El hotel no trabaja con el tipo de habitación {tipo}")
        return Habitacion.objects.create(tipo=tipo, numero=numero, hotel=self)

    def agregar_tarifa(self, tipo, baja, alta):
        # Que pasa si ya tengo el tipo cargado en el hotel?
        # que pasa si baja es mas grande que alta?
        pass 

    def get_habitaciones(self):
        return Habitacion.objects.filter(hotel=self)

    def get_paquetes(self):
        return PaqueteTuristico.objects.filter(hotel=self)

    def get_temporadas(self):
        return TemporadaAlta.objects.filter(hotel=self)

    def agregar_descuento(self, habitaciones, coeficiente):
        if habitaciones <= 0:
            raise DescuentoException("El mínimo de habitaciones para aplicar descuento es de 1")
        if coeficiente < 0:
            raise DescuentoException("El descuento no puede ser negativo")
        # Condicion loca?
        if self.descuentos.filter(cantidad_habitaciones__lt=habitaciones, coeficiente__gt=coeficiente).exists():
            raise DescuentoException("No se puede crear un descuento menor a un descuento ya otorgado por menos habitaciones")
        return self.descuentos.create(cantidad_habitaciones=habitaciones, coeficiente=coeficiente)

    def obtener_descuento(self, habitaciones):
        return self.obtener_descuento_por_cantidad(len(habitaciones))

    def obtener_descuento_por_cantidad(self, cantidad):
        return self.descuentos.filter(cantidad_habitaciones__gte=cantidad).first()

class PrecioPorTipo(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='tarifario')
    tipo = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE, related_name='hoteles')
    # Precio por noche
    baja = models.DecimalField(max_digits=20, decimal_places=2)
    alta = models.DecimalField(max_digits=20, decimal_places=2)

# Habitación
class Habitacion(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="habitaciones", on_delete=models.CASCADE)
    numero = models.PositiveSmallIntegerField() # 403 <Piso><Cuarto>
    tipo = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE)
    baja = models.BooleanField(default=False) #Baja Logica 

    class Meta:
        unique_together = (('hotel', 'numero'), )

    def __str__(self):
        return f"{self.hotel}, Habitacion: {self.numero}"

    def precio_por_noche(self, fecha):
        precio_por_tipo = self.hotel.tarifario.filter(tipo=self.tipo).first()
        if precio_por_tipo is None:
            #TODO: Custom exception
            raise Exception("No puedo calcular el precio")
        if self.hotel.temporadas.filter(inicio__lte=fecha, fin__gte=fecha).exists():
            return precio_por_tipo.alta
        return precio_por_tipo.baja

    def precio_temp_baja(self):
        precio_por_tipo = self.hotel.tarifario.filter(tipo=self.tipo).first()
        if precio_por_tipo is None:
            #TODO: Custom exception
            raise Exception("No puedo calcular el precio")
        return precio_por_tipo.baja

    def precio_temp_alta(self):
        precio_por_tipo = self.hotel.tarifario.filter(tipo=self.tipo).first()
        if precio_por_tipo is None:
            #TODO: Custom exception
            raise Exception("No puedo calcular el precio")
        return precio_por_tipo.alta

    def precio_alquiler(self, desde, hasta):
        if desde >= hasta:
            #TODO: Custom exception
            raise Exception("No puedo calcular el precio")
        total = Decimal(0)
        while desde < hasta:
            total += self.precio_por_noche(desde)
            desde += timedelta(days=1)
        return total
    
    def dar_baja(self):
        self.baja=True
        


# Temporada Alta
class TemporadaAlta(models.Model):
    nombre = models.CharField(max_length=200)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="temporadas")
    inicio = models.DateField()
    fin = models.DateField()

# Descuentos
class Descuento(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="descuentos")
    # 1 = coeficiente1 = 0 opcionalmente
    # 2 = coeficiente1
    # 3 = coeficiente2
    # 4 = coeficiente3
    # 5 = coeficiente4
    cantidad_habitaciones = models.PositiveSmallIntegerField()
    coeficiente = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        ordering = ["cantidad_habitaciones"]

# Paquete Turistico
class PaqueteTuristico(models.Model):
    nombre = models.CharField(max_length=200)
    coeficiente = models.DecimalField(max_digits=3, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    inicio = models.DateField()
    fin = models.DateField()
    habitaciones = models.ManyToManyField(Habitacion)
    vendido = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2)


    def actualizar_precio(self):
        self.precio=0
        
        habitaciones = Habitacion.objects.filter(paqueteturistico = self)
        
        for habitacion in habitaciones:
            self.precio += habitacion.precio_por_noche(self.inicio)

    def cantidad_dias(self):
        return abs(self.fin - self.inicio).days

    def get_costo(self):
        self.actualizar_precio()
        return "{0:.2f}".format((1-self.coeficiente) * (self.precio * self.cantidad_dias()))

    def tengo_habitacion(self,habitacion): 
        for item in self.habitaciones:
            if item.pk == habitacion.pk:
                return True
        return False

    def estoy_vigente(self):
        return (not self.vendido) and (self.fin < date.today())
            
    def marcar_venta(self):
        self.vendido=True
        

        