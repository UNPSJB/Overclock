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
from core.views import correctaAdmin, correctaVendedor
from django.contrib import admin
from django.contrib.admin.sites import all_sites
from django.urls import path, include
from core import views
app_name="core"



urlpatterns = [
  
    path('paisAdd', views.paisAdd),
    path('localidades', views.correctaAdmin, name="listadoLocalidades"),
    path('altaPais', views.altaPais),
    path('correctaVendedor', views.correctaVendedor),
    path('altaProvincia',views.altaProvincia, name="crearProvincia"),
    
]
