from django.shortcuts import render
from typing import Reversible
import django
from django.forms import forms
from django.http import request, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from hotel.models import Hotel
from .forms import HotelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.utils import timezone
from django.views.generic.edit import CreateView

# Create your views here.
def hotel(request):
    colHoteles=Hotel.objects.all()
    return render(request, "hotel/hotelAdmin.html",{"colHoteles": colHoteles})

def hotelCrear(request):
    print("Entre a la vista")
    colHoteles = Hotel.objects.all()
    form = HotelForm(request.POST)
    
    if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('hotel:hotel')
    return render(request, "hotel/modals/modal_hotel_crear.html", {"colHoteles": colHoteles, "formulario": form})

def hotelModificar(request):
    colHotel = Hotel.objects.all()
    form = HotelForm(request.POST)
    
    if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('hotel:hotel')
    return render(request, "hotel/modals/modal_hotel_crear.html", {"colHotel": colHotel, "formulario": form})