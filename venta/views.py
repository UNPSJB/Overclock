from venta.forms import ClienteForm
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from hotel.models import Hotel, PaqueteTuristico
from core.models import Persona, Vendedor, Cliente
from hotel.models import Hotel, Habitacion, TipoHabitacion
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from venta.carrito import Carrito

# Create your views here.

@login_required
def vendedor(request):
    carrito = Carrito(request)
    print("contenido de mi carrito antes: ",request.session['carrito'])
    personaInstancia = request.user.persona
    vendedorInstancia = get_object_or_404(Vendedor, persona = personaInstancia.id)
    colHoteles= Hotel.objects.filter(vendedores__persona=vendedorInstancia.persona)
    fecha_inicio=  datetime.strptime(request.session['fecha_inicio'], '%Y-%m-%d').date() if "fecha_inicio" in request.session else None
    fecha_fin=  datetime.strptime(request.session['fecha_fin'], '%Y-%m-%d').date() if "fecha_fin" in request.session else None
    if fecha_inicio:
        formulario_enviado="enviado"
    else:
        formulario_enviado="no_enviado"

    
    return render(request, "venta/vendedor.html", {"colHoteles": colHoteles,"vendedor":vendedorInstancia,
        "pasajeros": int(request.session['pasajeros']) if "pasajeros" in request.session else None, 
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "formulario_enviado":formulario_enviado
         })


def buscarHabitaciones(request,hotel):
    carrito = Carrito(request)
    print("contenido de mi carrito antes: ",request.session['carrito'])   
    
    fecha_inicio=  datetime.strptime(request.session['fecha_inicio'], '%Y-%m-%d').date() if "fecha_inicio" in request.session else None
    fecha_fin=  datetime.strptime(request.session['fecha_fin'], '%Y-%m-%d').date() if "fecha_fin" in request.session else None
    pasajeros = int(request.session['pasajeros']) if "pasajeros" in request.session else None
    
    #carrito.agregar_habitacion(1,fecha_inicio,fecha_fin,pasajeros)
    #print("contenido de mi carrito al agregar: ",request.session['carrito'])
    
    #carrito.quitar_habitacion(1,fecha_inicio,fecha_fin)
    #print("contenido de mi carrito al quitar: ",request.session['carrito'])
    
    carrito.quitar_paquete(1)
    print("contenido de mi carrito: ",request.session['carrito'])

    hotelInstancia = get_object_or_404(Hotel, pk=hotel)
    colHabitaciones = hotelInstancia.get_habitaciones_busqueda(fecha_inicio,fecha_fin,pasajeros)
    colPaquetes = hotelInstancia.get_paquetes_busqueda(fecha_inicio,fecha_fin,pasajeros)
    
    return render(request, "venta/buscarHabitaciones.html", {"hotel":hotelInstancia,
        "habitaciones_disponibles": colHabitaciones,
        "paquetes_disponibles":colPaquetes,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
        })


def iniciar_venta(request):
    fechaInicio=request.POST['fecha_inicio']
    fechaFin=request.POST['fecha_fin']
    pasajeros=request.POST['pasajeros']
    request.session['fecha_inicio']=fechaInicio
    request.session['fecha_fin']=fechaFin
    request.session['pasajeros']=pasajeros
    #request.session['venta']={'fecha_inicio': fechaInicio, '}

    return redirect('venta:vendedor')

def cancelar_venta(request):
    request.session.flush()
    #request.session['venta']=None TODO

    return redirect("venta:vendedor", request.user)


def vista_cliente(request):
    colClientes=Cliente.objects.all()
    return render(request, "venta/vista_cliente.html", {"colClientes": colClientes})

def cliente_aniadir(request):
    colClientes = Cliente.objects.all()
    form = ClienteForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            form.instance.hacer_cliente()                
            return redirect('venta:vistaCliente')
    return render(request,"venta/modals/modal_aniadir_cliente.html",{"formulario":form})


    

def cliente_modificar(request,cliente):
    clienteInstancia=get_object_or_404(Cliente,pk=cliente)
    colClientes = Cliente.objects.all()
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=clienteInstancia)
        if form.is_valid():
            clienteInstancia.persona.nombre = request.POST['nombre']
            clienteInstancia.persona.apellido = request.POST['apellido']
            clienteInstancia.persona.documento = request.POST['documento']
            clienteInstancia.persona.tipo_documento = request.POST['tipo_documento']
            clienteInstancia.persona.save()
            clienteInstancia.save()
            return redirect('venta:vistaCliente')
        else:
            form = ClienteForm(request.POST, instance=clienteInstancia)
    else:
        form = ClienteForm(instance=clienteInstancia)
        form.fields["nombre"].initial = clienteInstancia.persona.nombre
        form.fields["apellido"].initial = clienteInstancia.persona.apellido
        form.fields["documento"].initial = clienteInstancia.persona.documento
        form.fields["tipo_documento"].initial = clienteInstancia.persona.tipo_documento
    return render(request,"venta/modals/modal_modificar_cliente.html",{"cliente":clienteInstancia,"formulario":form})

    
    
