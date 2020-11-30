from datetime import date, datetime
from django.db.models import fields
from django.db.models.fields import DateField
from django.forms.widgets import DateInput
from django.shortcuts import render
from typing import Reversible
import django
from django.forms import forms
from django.http import request, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from hotel.models import Habitacion, Hotel, PrecioPorTipo, TemporadaAlta, PaqueteTuristico
from .forms import  HabitacionForm, HotelForm, TemporadaHotelForm, AgregarTipoAHotelForm, HabitacionForm, PaqueteTuristicoForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.utils import timezone
from django.views.generic.edit import CreateView
from core.models import Vendedor, Categoria, TipoHabitacion, Servicio


# Create your views here.
def hotel(request):
    colHoteles=Hotel.objects.all()
    return render(request, "hotel/hotelAdmin.html",{"colHoteles": colHoteles})

def hotelCrear(request):
    colHoteles = Hotel.objects.all()
    form = HotelForm(request.POST)
    
    if request.method == "POST":
            if form.is_valid():
                hotelInstancia=form.save()
                for servicio in hotelInstancia.categoria.servicios.all():
                    hotelInstancia.servicios.add(servicio)
                hotelInstancia.save()
                return redirect('hotel:hotel')
    return render(request, "hotel/modals/modal_hotel_crear.html", {"colHoteles": colHoteles, "formulario": form})

def hotelModificar(request, hotel):
    hotelInstancia = get_object_or_404(Hotel, pk= hotel )
    colHoteles = Hotel.objects.all()
    if request.method == 'POST':
        form=HotelForm(request.POST,instance=hotelInstancia)
        if form.is_valid():
            hotelInstancia = form.save()
            hotelInstancia.nombre=request.POST['nombre']
            hotelInstancia.direccion=request.POST['direccion']
            hotelInstancia.email=request.POST['email']
            categoria = get_object_or_404( Categoria , pk=request.POST['categoria'])
            
            hotelInstancia.categoria=categoria
            for servicio in hotelInstancia.categoria.servicios.all():
                    hotelInstancia.servicios.add(servicio)
            #hotelInstancia.localidad=request.POST['localidad']
            hotelInstancia.save()
            #form.save_m2m()
            return redirect('hotel:hotel')
        else:
            form=HotelForm(request.POST,instance=hotelInstancia)
    else:
        form=HotelForm(instance=hotelInstancia)
        form.fields['nombre'].widget.attrs['readonly'] = True
        form.fields['localidad'].widget.attrs['style'] = 'display:none;'
        form.fields['localidad'].label = ''
        form.fields['direccion'].widget.attrs['readonly'] = True
        form.fields['encargado'].widget.attrs['style'] = 'display:none;'
        form.fields['encargado'].label = ''
        """
        form.fields['direccion'].widget.attrs['readonly'] = True
        form.fields['encargado'].widget.attrs['readonly'] = True
        """
    return render(request, "hotel/modals/modal_hotel_modificar.html", {"colHoteles": colHoteles, "formulario": form, "hotel": hotelInstancia})


def detalleHotel(request,hotel):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)  
    return render(request, "hotel/vistaHotelAdmin.html",{"hotel":hotelInstancia })


#-------------------------- INICIO: TIPO DE HABITACION ----------------------------------------

def vistaTipoHabitacionHotel(request,hotel):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)
    tarifas_hotel=hotelInstancia.tarifario.all()
    return render(request, "hotel/tipoHabitacion_Hotel_Admin.html",{"hotel":hotelInstancia, "tarifas":tarifas_hotel })

def tipoHabitacionCrear(request,hotel):
    formulario=AgregarTipoAHotelForm(request.POST)
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)
    if request.method == "POST":
            formulario=AgregarTipoAHotelForm(request.POST)
            if formulario.is_valid():
                formulario=AgregarTipoAHotelForm(request.POST)
                tipoHabitacionRecibido=formulario.save(commit=False)
                tipoHabitacionRecibido.hotel= hotelInstancia
                tipoHabitacionRecibido.save()
                return redirect('hotel:tipoHabitacionHotel', hotel)
    return render(request, "hotel/modals/modal_tipoHabitacionHotel_crear.html",{"hotel": hotelInstancia,"formulario":formulario})


def tipoHabitacionModificar(request,hotel,tipo):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)
    tipoHabitacionInstancia=get_object_or_404(PrecioPorTipo,pk=tipo)
    if request.method == 'POST':
        formulario=AgregarTipoAHotelForm(request.POST,instance=tipoHabitacionInstancia)
        if formulario.is_valid():
            tipoHabitacionInstancia = formulario.save()
            tipoHabitacionInstancia.alta=request.POST['alta']
            tipoHabitacionInstancia.baja=request.POST['baja']
            tipoHabitacionInstancia.save()
            return redirect('hotel:tipoHabitacionHotel', hotel)
        else:
            formulario=AgregarTipoAHotelForm(request.POST,instance=tipoHabitacionInstancia)
    else:
        formulario=AgregarTipoAHotelForm(instance=tipoHabitacionInstancia)
        formulario.fields['tipo'].widget.attrs['style'] = 'display:none;'
        formulario.fields['tipo'].label = ''
    return render(request, "hotel/modals/modal_tipoHabitacionHotel_modificar.html",{"formulario":formulario, "hotel":hotelInstancia ,"tipo":tipoHabitacionInstancia})


def tipoHabitacionEliminar(request,hotel,tipo): 
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)
    tipoHabitacionInstancia=get_object_or_404(PrecioPorTipo,pk=tipo)
    if request.method == 'POST':
        tipoHabitacionInstancia.delete()
        return redirect('hotel:tipoHabitacionHotel', hotel)
    return render(request, "hotel/modals/modal_tipoHabitacionHotel_eliminar.html",{"hotel":hotelInstancia ,"tipo":tipoHabitacionInstancia})
    



#-------------------------- FIN TIPO DE HABITACION ----------------------------------------




#-------------------------- GESTION HABITACIONES ----------------------------------------

def habitacionCrear(request,hotel):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)
    formulario=HabitacionForm(request.POST)
    if request.method == "POST":
            if formulario.is_valid():
                habitacionInstancia=formulario.save(commit=False)
                habitacionInstancia.hotel= hotelInstancia
                habitacionInstancia.save()
                return redirect('hotel:vistaHotel',hotel)
    else:
        formulario=HabitacionForm(request.GET)
        formulario.fields['tipo'].choices=[(t.pk,t.nombre) for t in hotelInstancia.get_tipos()]

    return render(request, "hotel/modals/modal_habitacionHotel_crear.html",{"hotel":hotelInstancia,'formulario':formulario })


def habitacionEliminar(request,hotel,habitacion):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)
    habitacionInstancia=get_object_or_404(Habitacion,pk=habitacion)
    if request.method == "POST":
        habitacionInstancia.dar_baja()
        habitacionInstancia.save()
        return redirect('hotel:vistaHotel',hotel)
    return render(request, "hotel/modals/modal_habitacionHotel_eliminar.html",{"hotel":hotelInstancia,'habitacion':habitacionInstancia })

def habitacionReciclar(request,hotel,habitacion):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)
    habitacionInstancia=get_object_or_404(Habitacion,pk=habitacion)
    if request.method == "POST":
        habitacionInstancia.dar_alta()
        habitacionInstancia.save()
        return redirect('hotel:vistaHotel',hotel)
    return render(request, "hotel/modals/modal_habitacionHotel_reciclar.html",{"hotel":hotelInstancia,'habitacion':habitacionInstancia })

#-------------------------- GESTION HABITACIONES ----------------------------------------




#-------------------------- INICIO: GESTION TEMPORADAS ----------------------------------------

def temporadaHotel(request,hotel):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)    
    return render(request, "hotel/temporada_Hotel_Admin.html",{"hotel":hotelInstancia })


def temporadaHotelCrear(request, hotel):
    form = TemporadaHotelForm(request.POST)
    hotelInstancia=get_object_or_404(Hotel, pk=hotel)
    if request.method == "POST":
            form = TemporadaHotelForm(request.POST)
            if form.is_valid():
                form = TemporadaHotelForm(request.POST)
                temporadaInstancia=form.save(commit=False)
                temporadaInstancia.hotel= hotelInstancia
                temporadaInstancia.save()
                return redirect('hotel:temporadaHotel', hotel)
    return render(request, "hotel/modals/modal_temporadaHotel_crear.html", { "hotel": hotelInstancia, "formulario": form})

def temporadaEliminar(request,hotel,temporada):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)
    temporadaInstancia=get_object_or_404(TemporadaAlta,pk=temporada)
    if request.method == "POST":
        temporadaInstancia.delete()
        
        return redirect('hotel:temporadaHotel',hotel)
    return render(request, "hotel/modals/modal_temporadaHotel_eliminar.html",{"hotel":hotelInstancia,'temporada':temporadaInstancia })


def temporadaModificar(request,hotel,temporada):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)
    temporadaInstancia=get_object_or_404(TemporadaAlta,pk=temporada)
    form = TemporadaHotelForm(request.POST or None,instance=temporadaInstancia)
    if request.method=="POST":
        if form.is_valid():
            temporada=form.save(commit=False)
            temporada.save()
            return redirect('hotel:temporadaHotel',hotel)
    else:
        form.initial['inicio']=str(temporadaInstancia.inicio)
        form.initial['fin']=str(temporadaInstancia.fin)
    return render(request, "hotel/modals/modal_temporadaHotel_modificar.html",{"formulario":form,"hotel":hotelInstancia,'temporada':temporadaInstancia })

#-------------------------- FIN: GESTION TEMPORADAS ----------------------------------------

#-------------------------- INICIO: GESTION PAQUETES TURISTICOS ----------------------------------------

def paqueteTuristicoHotel(request,hotel):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)    
    return render(request, "hotel/vistaHotelAdmin.html",{"hotel":hotelInstancia })
    
def paqueteTuristicoHotelCrear(request, hotel):
    form = PaqueteTuristicoForm(request.POST)
    hotelInstancia=get_object_or_404(Hotel, pk=hotel)
    if request.method == "POST":
            if form.is_valid():
                paqueteTuristicoInstancia=form.save(commit=False)
                paqueteTuristicoInstancia.hotel= hotelInstancia
                paqueteTuristicoInstancia.precio=1
                paqueteTuristicoInstancia.save()
                form.save_m2m()
                return redirect('hotel:paqueteTuristicoHotel', hotel)
    else:
        form.fields['habitaciones'].choices=[(c.pk,c.numero) for c in Habitacion.objects.filter(hotel=hotelInstancia)]
        
    return render(request, "hotel/modals/modal_paqueteTuristicoHotel_crear.html", { "hotel": hotelInstancia, "formulario": form})

def paqueteTuristicoHotelModificar(request,hotel,paquete):
    hotelInstancia=get_object_or_404(Hotel, pk=hotel)
    paqueteInstancia=get_object_or_404(PaqueteTuristico, pk=paquete)
    form = PaqueteTuristicoForm(request.POST or None,instance=paqueteInstancia)
    if request.method == "POST":
        print("POST!!!!!!!!!!!!!!!!!")
        if form.is_valid():
            print("<<<<<<FORMULARIO VALIDO>>>>>>>>>>>")
            paquete=form.save(commit=False)
            paquete.save()
            return redirect('hotel:paqueteTuristicoHotel', hotel)
    else:
        form.fields['habitaciones'].choices=[(c.pk,c.numero) for c in Habitacion.objects.filter(hotel=hotelInstancia)]
        arregloHabitacionesSeleccionadas = paqueteInstancia.habitaciones.all()
        preseleccion=[]
        for habitacion in arregloHabitacionesSeleccionadas:
                preseleccion.append(habitacion.pk)
        form.initial['habitaciones'] = preseleccion
        form.initial['inicio']=str(paqueteInstancia.inicio)
        form.initial['fin']=str(paqueteInstancia.fin)
        dicc={'nombre','habitaciones','inicio','fin'}
        for campo in dicc:
            form.fields[campo].widget.attrs['style'] = 'display:none;'
            form.fields[campo].label = ''
        form.fields['coeficiente'].label='coeficiente de descuento'
        return render(request, "hotel/modals/modal_paqueteTuristicoHotel_modificar.html",{'formulario':form,'hotel':hotelInstancia,'paquete':paqueteInstancia})

def paqueteTuristicoHotelEliminar(request,hotel,paquete):
    hotelInstancia=get_object_or_404(Hotel, pk=hotel)
    paqueteInstancia=get_object_or_404(PaqueteTuristico, pk=paquete)
    if request.method=='POST':
        paqueteInstancia.delete()
        return redirect('hotel:paqueteTuristicoHotel', hotel)
    return render(request, "hotel/modals/modal_paqueteTuristicoHotelEliminar.html",{'hotel':hotelInstancia,'paquete':paqueteInstancia})


#-------------------------- FIN: GESTION PAQUETES TURISTICOS ----------------------------------------

#-------------------------- INICIO: GESTION PAQUETES TURISTICOS ----------------------------------------

def serviciosHotel(request,hotel):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)
    categoria=hotelInstancia.get_categoria()
    print(categoria.nombre)
   
    return render(request, "hotel/servicios_Hotel_Admin.html",{"hotel":hotelInstancia,"categoria":categoria})

def aniadirServicioHotel(request,hotel):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)
    categoria=hotelInstancia.get_categoria()
    form=HotelForm(request.POST or None,instance=hotelInstancia)
    if request.method =="POST":
        pass
    else:
        dic={}
        
        
        #listaDeServicios=[]
        #for servicio in Servicio.objects.all():
        #    if servicio not in hotelInstancia.get_servicios():
        #        listaDeServicios.append(get_object_or_404(Servicio, pk=servicio.pk))
        #print(listaDeServicios)
        return render(request, "hotel/modals/modal_servicio_Hotel_aniadir.html",{"formulario":form,"hotel":hotelInstancia,"categoria":categoria})
    

