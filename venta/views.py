
from venta.models import Factura, Tipo_pago
from venta.forms import ClienteForm
from django.shortcuts import render, redirect, get_object_or_404
from hotel.models import Hotel, PaqueteTuristico
from core.models import Persona, Vendedor, Cliente
from hotel.models import Hotel
from django.contrib.auth.decorators import login_required
from datetime import datetime
from venta.carrito import Carrito
from venta.services import cargar_liquidaciones_pendientes, cargar_precio_habitacion_por_temporada, documento_valido, filtrar_habitaciones, liquidar_liquidaciones_pendientes, preparar_hoteles


# Create your views here.

@login_required
def vendedor(request):
    carrito = Carrito(request)
    if carrito.get_cliente()!=None: 
        print(carrito.get_cliente().persona.nombre)
    else:
        print("Aun no se ha seleccionado Cliente")
    contador=carrito.get_cantidad()
    print("contenido de mi carrito antes: ",request.session['carrito'])
    personaInstancia = request.user.persona
    vendedorInstancia = get_object_or_404(Vendedor, persona = personaInstancia.id)
    colHoteles= Hotel.objects.filter(vendedores__persona=vendedorInstancia.persona)
    fecha_inicio=  request.session['fecha_inicio'] if "fecha_inicio" in request.session else None
    fecha_fin=  request.session['fecha_fin'] if "fecha_fin" in request.session else None
    pasajeros =  int(request.session['pasajeros']) if "pasajeros" in request.session else None
    hoteles_finales = []
    if fecha_inicio:
        formulario_enviado="enviado"
        hoteles_finales = preparar_hoteles(colHoteles,fecha_inicio,fecha_fin,pasajeros)
    else:
        formulario_enviado="no_enviado"
    
    return render(request, "venta/vendedor.html", {"colHoteles": hoteles_finales,"vendedor":vendedorInstancia,
        "pasajeros": pasajeros,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "formulario_enviado":formulario_enviado,
        "contador":contador
         })


        
def buscarHabitaciones(request,hotel):
    personaInstancia = request.user.persona
    vendedorInstancia = get_object_or_404(Vendedor, persona = personaInstancia.id)
    carrito = Carrito(request)
    contador=carrito.get_cantidad()
    print("contenido de mi carrito antes: ",request.session['carrito'])   
    fecha_inicio=  datetime.strptime(request.session['fecha_inicio'], '%Y-%m-%d').date() if "fecha_inicio" in request.session else None
    fecha_fin=  datetime.strptime(request.session['fecha_fin'], '%Y-%m-%d').date() if "fecha_fin" in request.session else None
    pasajeros = int(request.session['pasajeros']) if "pasajeros" in request.session else None
    hotelInstancia = get_object_or_404(Hotel, pk=hotel)
    coleccionHabitaciones = hotelInstancia.get_habitaciones_busqueda(fecha_inicio,fecha_fin,pasajeros)
    colHabitaciones = [habitacion for habitacion in coleccionHabitaciones if habitacion.baja == False]
    print("habitaciones hoteeeeel" , colHabitaciones)
    ventas_habitaciones_en_carrito=carrito.get_alquileres_habitaciones()
    for venta in ventas_habitaciones_en_carrito:
        fecha_inicio_venta=datetime.strptime(venta.fecha_inicio, '%Y-%m-%d').date()
        fecha_fin_venta=datetime.strptime(venta.fecha_fin, '%Y-%m-%d').date()
        for habitacion in colHabitaciones:
            pksiguales=str(habitacion.pk)==venta.habitacion
            inicio_alquiler_en_fechas_ingresadas=(fecha_inicio_venta>=fecha_inicio and fecha_inicio_venta<=fecha_fin)
            fin_alquiler_en_fechas_ingresadas=(fecha_fin_venta>=fecha_inicio and fecha_fin_venta<=fecha_fin)
            contenido_fechas=(fecha_inicio_venta<=fecha_inicio and fecha_fin_venta>=fecha_fin)
            if (pksiguales and (inicio_alquiler_en_fechas_ingresadas or fin_alquiler_en_fechas_ingresadas or contenido_fechas)):
                colHabitaciones.remove(habitacion)
    print(colHabitaciones)
    ventas_paquetes_en_carrito=carrito.get_alquileres_paquetes()
    colPaquetes = hotelInstancia.get_paquetes_busqueda(fecha_inicio,fecha_fin,pasajeros)
    print("col paquetes" , colPaquetes)
    for venta in ventas_paquetes_en_carrito:
        paquete=get_object_or_404(PaqueteTuristico,pk=venta.paquete)
        if paquete in colPaquetes:
            colPaquetes.remove(paquete)
    habitaciones_filtradas = filtrar_habitaciones(colHabitaciones , colPaquetes)
    print("habitaciones : " , habitaciones_filtradas)
    habitaciones_con_precio_final = cargar_precio_habitacion_por_temporada(colHabitaciones, hotelInstancia.pk, fecha_inicio, fecha_fin )
    return render(request, "venta/buscarHabitaciones.html", {"hotel":hotelInstancia,
        "habitaciones_disponibles": habitaciones_con_precio_final,
        "paquetes_disponibles":colPaquetes,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "vendedor":vendedorInstancia,
        "contador":contador
        })




def alquilar_habitacion(request, habitacion, hotel):
    carrito = Carrito(request)
    fecha_inicio=  datetime.strptime(request.session['fecha_inicio'], '%Y-%m-%d').date() if "fecha_inicio" in request.session else None
    fecha_fin=  datetime.strptime(request.session['fecha_fin'], '%Y-%m-%d').date() if "fecha_fin" in request.session else None
    pasajeros = int(request.session['pasajeros']) if "pasajeros" in request.session else None
    carrito.agregar_habitacion(habitacion, fecha_inicio, fecha_fin, pasajeros)
    return redirect("venta:buscarHabitaciones", hotel)


def alquilar_paquete(request, paquete, hotel):
    carrito = Carrito(request)
    pasajeros = int(request.session['pasajeros']) if "pasajeros" in request.session else None
    carrito.agregar_paquete(paquete, pasajeros)
    return redirect("venta:buscarHabitaciones",hotel)


def iniciar_venta(request):
    fechaInicio=request.POST['fecha_inicio']
    fechaFin=request.POST['fecha_fin']
    pasajeros=request.POST['pasajeros']
    request.session['fecha_inicio']=fechaInicio
    request.session['fecha_fin']=fechaFin
    request.session['pasajeros']=pasajeros
    return redirect('venta:vendedor')

def cancelar_venta(request):
    request.session.flush()
    #request.session['venta']=None TODO
    return redirect("venta:vendedor", request.user)


def vista_cliente(request):
    colClientes=Cliente.objects.all()
    personaInstancia = request.user.persona
    vendedorInstancia = get_object_or_404(Vendedor, persona = personaInstancia.id)
    carrito = Carrito(request)
    contador=carrito.get_cantidad()
    return render(request, "venta/vista_cliente.html", {"colClientes": colClientes,"vendedor":vendedorInstancia,"contador":contador})


def cliente_aniadir(request):
    form = ClienteForm(request.POST)
    if request.method == "POST":
        dni_nuevo_cliente = request.POST['documento']
        if documento_valido(dni_nuevo_cliente , form):
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

    
def vista_carrito(request):
    carrito=Carrito(request)
    coleccion_ventas = []
    total = 0
    if carrito.get_cantidad() > 0:
        coleccion_ventas = carrito.mostrar_carrito()
        total=float(str(coleccion_ventas['total']).strip("['|{|}]"))
    personaInstancia = request.user.persona
    vendedorInstancia = get_object_or_404(Vendedor, persona = personaInstancia.id)
    contador=carrito.get_cantidad()
    cliente=carrito.get_cliente()
    try:
        print(cliente.persona.nombre)
    except Exception:
        print("no hay persona seleccionada")
    print(carrito.get_vendedor().persona.nombre)
    return render(request,"venta/carrito.html",{"cliente":cliente,"vendedor":vendedorInstancia, "contador":contador, "coleccion_ventas":coleccion_ventas,"total":total})


def quitar_paquete_carrito(request, paquete):
    carrito=Carrito(request)
    carrito.quitar_paquete(paquete.strip("p"))
    return redirect('venta:vistaCarrito')

def quitar_habitacion_carrito(request, habitacion, desde, hasta):
    carrito=Carrito(request)
    print("holaaaaaaaa ", habitacion)
    habitacion=habitacion.split("-")
    print("holaaaaaaaaaa ", habitacion)
    fecha_desde=datetime.strptime(desde, '%Y-%m-%d').date()
    fecha_hasta=datetime.strptime(hasta, '%Y-%m-%d').date()
    carrito.quitar_habitacion(habitacion[1], fecha_desde, fecha_hasta)
    return redirect('venta:vistaCarrito')


def seleccionar_cliente(request, cliente):
    persona = Persona.objects.get(id = cliente)
    request.session['nombre_cliente']= persona.nombre
    request.session['apellido_cliente']=  persona.apellido
    carrito=Carrito(request)
    carrito.set_cliente(cliente)
    return redirect("venta:vendedor")

def facturar_carrito(request):
    carrito=Carrito(request)
    personaInstancia = request.user.persona
    vendedorInstancia = get_object_or_404(Vendedor, persona = personaInstancia.id)
    cliente=carrito.get_cliente()
    factura=Factura()
    factura.set_atributos(vendedorInstancia,cliente)
    factura.save()
    coleccion_alquileres_habitaciones=(carrito.get_alquileres_habitaciones())
    factura.alquilar_habitaciones(coleccion_alquileres_habitaciones)
    for paquete in carrito.get_paquetes_para_alquilar():
        factura.alquilar_paquete(paquete)

    coleccion_ventas = carrito.mostrar_carrito()
    total_carrito=float(str(coleccion_ventas['total']).strip("['|{|}]"))

    alcanzanPuntos= factura.cliente.puntos>= int(factura.total())+1
    return render(request,"venta/facturar_carrito.html",{"factura":factura, "alcanzanPuntos": alcanzanPuntos })

def pagar_factura(request, factura):
    seleccionTipoPago=request.POST.get('opcionTipoPago')
    facturita= get_object_or_404(Factura, pk=factura)
    if seleccionTipoPago=="Puntos":   
        facturita.cliente.quitar_puntos(facturita)  
    else:
        if seleccionTipoPago=="Efectivo":
            facturita.cliente.agregar_puntos(facturita)
    tipoPago= get_object_or_404(Tipo_pago, nombre=seleccionTipoPago)
    facturita.tipo_pago=tipoPago
    facturita.save()
    carrito = Carrito(request)
    carrito.vaciar_carrito()
    return redirect("venta:vendedor")


def cancelar_venta(request,factura):
    print("CANCELANDO VENTAAAAAAAAAA!!!!!")
    facturita= get_object_or_404(Factura, pk=factura)
    for alquiler in facturita.get_alquileres():
        if alquiler.paquete is not None:
            alquiler.paquete.cancelar_venta()
    facturita.delete()
    carrito = Carrito(request)
    carrito.vaciar_carrito()
    return redirect("venta:vendedor")


def limpiar_preferencias(request):
    carrito = Carrito(request)
    carrito.set_cliente(None)
    if 'fecha_inicio' in request.session:
        del request.session['fecha_inicio']
    if 'fecha_fin' in request.session:
        del request.session['fecha_fin']
    if 'pasajeros' in request.session:
        del request.session['pasajeros']
    if 'nombre_cliente' in request.session:
        del request.session['nombre_cliente']
    if 'apellido_cliente' in request.session:
        del request.session['apellido_cliente']
    return redirect("venta:vendedor")

def listado_liquidaciones(request):
    personaInstancia = request.user.persona
    if request.method == "POST":
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        liquidaciones_pendientes = cargar_liquidaciones_pendientes(fecha_inicio, fecha_fin)
        context = {
            "liquidaciones_pendientes": liquidaciones_pendientes,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "administrador":personaInstancia,
        }
        print(f'retornando este arreglo : {liquidaciones_pendientes}')
        return render(request, "venta/listado_liquidaciones.html",context)
    else:
        context = {
            "liquidaciones_pendientes": [],
            "administrador":personaInstancia,
        }
        return render(request, "venta/listado_liquidaciones.html",context)

def liquidar(request, documento, fecha_inicio, fecha_fin):
    personaInstancia = request.user.persona
    liquidar_liquidaciones_pendientes(fecha_inicio, fecha_fin, documento)
    liquidaciones_pendientes = cargar_liquidaciones_pendientes(fecha_inicio, fecha_fin)
    context = {
        "liquidaciones_pendientes": liquidaciones_pendientes,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "administrador":personaInstancia,
    }
    return render(request, 'venta/listado_liquidaciones.html', context)


