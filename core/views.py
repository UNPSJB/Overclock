from typing import Reversible
import django
from django.forms import forms
from django.http import request, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from core.models import Pais, Provincia, Localidad
from .forms import PaisForm, LocalidadForm, AutenticacionForm, ProvinciaForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.utils import timezone

from django.views.generic.edit import CreateView


"""def ingresoAdmin(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "administrador.html")
    # En otro caso redireccionamos al login
    return redirect('/home.html')"""


def home(request):
    form = AutenticacionForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                usr = User.objects.get(username=user)
                if usr.groups.filter(name='Administrador').exists():
                    return redirect("core:administrador")
                else:
                    # Y le redireccionamos a la portada
                    return redirect("core:vendedor")
            else:
                print("ESTAMOS ACA <=========")
                return render(request, "home.html", {'form': form})

    # Si llegamos al final renderizamos el formulario
    return render(request, "home.html", {'form': form})


def correctaAdmin(request):
    # aca van los listados de hoteles
    return render(request, "base/administrador.html")


def correctaVendedor(request):
    # aca van tambien listados de hoteles
    return render(request, "base/vendedor.html")


def regionAdmin(request):
    paises = Pais.objects.all()
    provincias = Provincia.objects.all()
    localidades = Localidad.objects.all()
    # FIXME cuando no vienen datos en el POST  por ser un GET, la instanciacion tendria que ser
    formPais = PaisForm(request.POST)
    formProvincia = ProvinciaForm(request.POST)
    formLocalidad = LocalidadForm(request.POST)

    if request.method == "POST":
        # TODO garantizar que si los forms tienen errores las modales se vuelvan a abrir indicando el error
        # print(request.POST)

       # si la accion viene por el lado de un boton del modal nombre accion y valor pais....
        if request.POST["accion"] == "provincia":
            # tomamos el formulario recepcionado para trabajarlo
            form = ProvinciaForm(request.POST)
            if form.is_valid():  # si es valido
                # tomamos el formulario recibido
                provinciaIngresado = Provincia(
                    nombre=form.cleaned_data['nombre'])
                # declaramos una variable para poder seguir cuando realmente estamos frente a una ocurrencia o no
                ocurrencia = False
                for provincia in provincias:  # se recorren las provincias existentes
                    if (provincia.nombre == provinciaIngresado.nombre):  # si los nombres son iguales
                        ocurrencia = True  # con al menos una declaramos esa variable en verdadero
                    # debug de los valores
                    print(f"La ocurrencia dio ...{ocurrencia}")
                if ocurrencia == True:  # si es verdadero que hay ocurrencias iguales
                    print("LA PROVINCIA EXISTE INMUNDO ANIMAL")  # debug
                    print("====>    NO SE GRABA   :)")
                    # se vuelve a refrescar la pagina
                    return redirect('core:opcionRegion')
                else:  # si no se encontro que la provincia ya existe
                    print("====>    SE GRABA   :)")
                    formProvincia.save()  # se graba la provincia
            return redirect('core:opcionRegion')  # se recarga la pagina

        elif request.POST["accion"] == "pais":
            if formPais.is_valid():
                formPais.save()
            else:
                formPais.save()
        elif request.POST["accion"] == "localidad":
            if formLocalidad.is_valid():
                formLocalidad.save()
    return render(request, "core/regionAdmin.html", {"paises": paises, "localidades": localidades, "provincias": provincias, "formPais": formPais, "formProvincia": formProvincia, "formLocalidad": formLocalidad})


def logout(request):
    if not request.user.is_authenticated:
        logout(request)
    return redirect(home)


def localidadCrear(request):
    localidades = Localidad.objects.all() #tomo todas las localidades (la idea aca es usarlas para controlar entradas)
    formLocalidad = LocalidadForm(request.POST) #variable que toma el formulario con datos que se envia
    if request.method == "POST": # si se usa el envio ....
            if formLocalidad.is_valid(): # si es valido el formulario ...
                formLocalidad.save() # se graba!
                return redirect('core:opcionRegion') # se redirige hacia region
    return render(request, "core/modals/modal_localidad_crear.html", {"localidades": localidades, "formulario": formLocalidad}) #si el metodo es GET se renderiza el modal con un formulario vacio

def provinciaCrear(request):
    provincias = Provincia.objects.all()
    formProvincia = ProvinciaForm(request.POST)
    if request.method == "POST":
            if formProvincia.is_valid():
                formProvincia.save()
                return redirect('core:opcionRegion')
    return render(request, "core/modals/modal_provincia_crear.html", {"provincias": provincias, "formulario": formProvincia})

def paisCrear(request):
    paises = Pais.objects.all()
    formPais = PaisForm(request.POST)
    if request.method == "POST":
            if formPais.is_valid():
                formPais.save()
                return redirect('core:opcionRegion')
    return render(request, "core/modals/modal_pais_crear.html", {"paises": paises, "formulario": formPais})

def localidadModificar(request, ciudad): #se recibe la el objeto ciudad que corresponde a la linea donde se encontraba el boton modificar
    ciudadInstancia = get_object_or_404(Localidad, nombre=ciudad) #ciudadInstancia es el objeto Localidad que corresponde a la ciudad, esto es para modificar lo que ya existe
    localidades = Localidad.objects.all() #localidades se pretende usar para controlar los ingresos
    if request.method == 'POST': #si el metodo es post, esto es el envio de la modificacion
        form=LocalidadForm(request.POST,instance=ciudadInstancia) # el fomulario toma los datos del objeto correspondiente a la ciudad a modificar
        if form.is_valid(): #si el formulario es valido
            ciudadInstancia.nombre=request.POST['nombre'] #tomamos el campo nombre de la instancia que teniamos y la cambiamos por la que nos devuelve el formulario
            ciudadInstancia.save() # se graba la modificacion
            return redirect('core:opcionRegion') # se redirige a region
        else: #si el formulario no fue valido se devuelve para mostrar errores
            form=LocalidadForm(request.POST,instance=ciudadInstancia)
    else: #si el metodo es GET ...
        form=LocalidadForm(instance=ciudadInstancia)        
    return render(request, "core/modals/modal_localidad_modificar.html", {"localidades": localidades, "formulario": form, "ciudad": ciudadInstancia})


def provinciaModificar(request, provincia):
    provinciaInstancia = get_object_or_404(Provincia, nombre=provincia)
    provincias = Provincia.objects.all()
    if request.method == 'POST':
        form=ProvinciaForm(request.POST,instance=provinciaInstancia)
        if form.is_valid():
            provinciaInstancia.nombre=request.POST['nombre']
            provinciaInstancia.save()
            return redirect('core:opcionRegion')
        else:
            form=ProvinciaForm(request.POST,instance=provinciaInstancia)
    else:
        form=ProvinciaForm(instance=provinciaInstancia)
    return render(request, "core/modals/modal_provincia_modificar.html", {"provincias": provincias, "formulario": form, "provincia": provinciaInstancia})

def paisModificar(request, pais):
    paisInstancia = get_object_or_404(Pais, nombre=pais)
    paises = Pais.objects.all()
    if request.method == 'POST':
        form=PaisForm(request.POST,instance=paisInstancia)
        if form.is_valid():
            paisInstancia.nombre=request.POST['nombre']
            paisInstancia.save()
            return redirect('core:opcionRegion')
        else:
            form=PaisForm(request.POST,instance=paisInstancia)
    else:
        form=PaisForm(instance=paisInstancia)
    return render(request, "core/modals/modal_pais_modificar.html", {"paises": paises, "formulario": form, "pais": paisInstancia})
