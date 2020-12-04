from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from hotel.models import Hotel
from core.models import Persona, Vendedor
from hotel.models import Hotel, Habitacion, TipoHabitacion
from django.contrib.auth.models import User
# Create your views here.

def vendedor(request, usuario):
    usuarioInstancia = get_object_or_404(User, username=usuario)
    personaInstancia = get_object_or_404(Persona, usuario = usuarioInstancia.id)
    vendedorInstancia = get_object_or_404(Vendedor, persona = personaInstancia.id)
    colHoteles= Hotel.objects.filter(vendedores__persona=vendedorInstancia.persona)
    return render(request, "venta/vendedor.html", {"colHoteles": colHoteles})


def alquilar(request,fechaInicio,fechaFin,cantPasajeros,hotel):
    hotelInstancia = get_object_or_404(Hotel, pk=hotel)
    colHabitaciones = hotelInstancia.get_habitaciones()
    return render(request, "venta/buscarHabitaciones.html", {"habitaciones_disponibles": colHabitaciones})

