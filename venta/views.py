from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from hotel.models import Hotel
from core.models import Persona, Vendedor
from hotel.models import Hotel, Habitacion, TipoHabitacion
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime



# Create your views here.

@login_required
def vendedor(request):
    personaInstancia = request.user.persona
    vendedorInstancia = get_object_or_404(Vendedor, persona = personaInstancia.id)
    colHoteles= Hotel.objects.filter(vendedores__persona=vendedorInstancia.persona)


    fecha_inicio=  datetime.strptime(request.session['fecha_inicio'], '%Y-%m-%d').date() if "fecha_inicio" in request.session else None
    fecha_fin=  datetime.strptime(request.session['fecha_fin'], '%Y-%m-%d').date() if "fecha_fin" in request.session else None
    return render(request, "venta/vendedor.html", {"colHoteles": colHoteles,
        "pasajeros": int(request.session['pasajeros']) if "pasajeros" in request.session else None, 
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
         })


def buscarHabitaciones(request,hotel):
    fecha_inicio=  datetime.strptime(request.session['fecha_inicio'], '%Y-%m-%d').date() if "fecha_inicio" in request.session else None
    fecha_fin=  datetime.strptime(request.session['fecha_fin'], '%Y-%m-%d').date() if "fecha_fin" in request.session else None
    pasajeros = int(request.session['pasajeros']) if "pasajeros" in request.session else None
    hotelInstancia = get_object_or_404(Hotel, pk=hotel)
    colHabitaciones = hotelInstancia.get_habitaciones()
    colPaquetes = hotelInstancia.get_paquetes_busqueda(fecha_inicio,fecha_fin,pasajeros)
    print(colHabitaciones)
    return render(request, "venta/buscarHabitaciones.html", {"hotel":hotelInstancia,
        "habitaciones_disponibles": colHabitaciones,
        "paquetes_disponibles":colPaquetes,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        })


def iniciar_venta(request):
    fechaInicio=request.POST['fecha_inicio']
    fechaFin=request.POST['fecha_fin']
    pasajeros=request.POST['pasajeros']
    request.session['fecha_inicio']=fechaInicio
    request.session['fecha_fin']=fechaFin
    request.session['pasajeros']=pasajeros
    #request.session['venta']={'fecha_inicio': fechaInicio, '}

    return redirect("venta:vendedor")

def cancelar_venta(request):
    request.session.flush()
    #request.session['venta']=None

    return redirect("venta:vendedor", request.user)