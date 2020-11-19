"""BuenaVista URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.admin.sites import all_sites
from django.urls import path, include
from hotel import views as hviews
from core import views as cviews
app_name="hotel"



urlpatterns = [
    path('logout', cviews.logout),

    path('hotel',hviews.hotel, name="hotel"),
    path('crearHotel',hviews.hotelCrear, name="modalCrearHotel"),
    path('modificarHotel/<hotel>',hviews.hotelModificar, name="modalModificarHotel"),

    path('vistaHotel/<hotel>', hviews.detalleHotel, name="vistaHotel"),
    
    path('tipoHabitacionHotel/<hotel>', hviews.vistaTipoHabitacionHotel, name="tipoHabitacionHotel"),
    path('crearTipoHabitacion/<hotel>', hviews.tipoHabitacionCrear, name="modalCrearTipoHabitacion"),

    path('temporadaHotel/<hotel>', hviews.temporadaHotel, name="temporadaHotel"),
    path('crearTemporadaHotel/<hotel>',hviews.temporadaHotelCrear, name="modalCrearTemporadaHotel"),

]
