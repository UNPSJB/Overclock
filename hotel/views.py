from django.shortcuts import render
from typing import Reversible
import django
from django.forms import forms
from django.http import request, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from hotel.models import Hotel, PrecioPorTipo, TemporadaAlta
from .forms import HotelForm, TemporadaHotelForm, AgregarTipoAHotelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.utils import timezone
from django.views.generic.edit import CreateView
from core.models import Vendedor, Categoria

# Create your views here.
def hotel(request):
    colHoteles=Hotel.objects.all()
    #for hotel in colHoteles:
        #print(hotel.es_comercializable())
    return render(request, "hotel/hotelAdmin.html",{"colHoteles": colHoteles})

def hotelCrear(request):
    print("Entre a la vista")
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
    print(hotelInstancia.temporadas.first().fin)  
    return render(request, "hotel/vistaHotelAdmin.html",{"hotel":hotelInstancia })


#-------------------------- TIPO DE HABITACION ----------------------------------------

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
    



#-------------------------- TIPO DE HABITACION ----------------------------------------



def temporadaHotel(request,hotel):
    hotelInstancia =get_object_or_404(Hotel, pk=hotel)    
    return render(request, "hotel/temporada_Hotel_Admin.html",{"hotel":hotelInstancia })


def temporadaHotelCrear(request, hotel):
    form = TemporadaHotelForm(request.POST)
    hotelInstancia=get_object_or_404(Hotel, pk=hotel)
    if request.method == "POST":
            form = TemporadaHotelForm(request.POST)
            if form.is_valid():
                print(hotelInstancia)
                form = TemporadaHotelForm(request.POST)
                temporadaInstancia=form.save(commit=False)
                
                temporadaInstancia.hotel= hotelInstancia
                print(temporadaInstancia.nombre)
                print(temporadaInstancia.inicio)
                print(temporadaInstancia.fin)
                
                temporadaInstancia.save()
                return redirect('hotel:temporadaHotel', hotel)
    return render(request, "hotel/modals/modal_temporadaHotel_crear.html", { "hotel": hotelInstancia, "formulario": form})
