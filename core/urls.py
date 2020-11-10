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
from core.views import correctaAdmin, correctaVendedor, localidadModificar, tipoHabitacionModificar
from django.contrib import admin
from django.contrib.admin.sites import all_sites
from django.urls import path, include
from core import views
app_name="core"



urlpatterns = [
  
    path('logout', views.logout),
    path('homeAdministrador', views.correctaAdmin, name="administrador"),
    path('hometaVendedor', views.correctaVendedor,name="vendedor"),
    path('region',views.regionAdmin, name="opcionRegion"),

    path('tipoHabitacion',views.tipoHabitacion, name="opcionTipoHabitacion"),
    path('servicio',views.servicio, name="servicio"),

    path('crearLocalidad',views.localidadCrear, name="modalCrearLocalidad"),
    path('modificarLocalidad/<ciudad>',views.localidadModificar, name="modalModificarLocalidad"),
    path('crearProvincia',views.provinciaCrear, name="modalCrearProvincia"),
    path('modificarProvincia/<provincia>',views.provinciaModificar, name="modalModificarProvincia"),
    path('crearPais',views.paisCrear, name="modalCrearPais"),
    path('modificarPais/<pais>',views.paisModificar, name="modalModificarPais"),
    path('crearTipoHabitacion',views.tipoHabitacionCrear, name="modalCrearTipoHabitacion"),

    path('modificarTipoHabitacion/<tipoHabitacion>',views.tipoHabitacionModificar, name="modalModificarTipoHabitacion"),
    path('crearServicio',views.servicioCrear, name="modalCrearServicio"),
    path('modificarServicio/<servicio>',views.serviciosModificar, name="modalModificarServicio"),
]
