import django
from django.forms import forms
from django.http import request, JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from core.models import Pais, Provincia, Localidad
from .forms import PaisForm, LocalidadForm, AutenticacionForm, ProvinciaForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.utils import timezone

from django.views.generic.edit import CreateView


def ingresoAdmin(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "administrador.html")
    # En otro caso redireccionamos al login
    return redirect('/home.html')


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
                return render(request, "home.html", {'form': form})

    # Si llegamos al final renderizamos el formulario
    return render(request, "home.html", {'form': form})


def correctaAdmin(request):
   #aca van los listados de hoteles
   return render(request, "base/administrador.html")

def correctaVendedor(request):
    #aca van tambien listados de hoteles
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
                formPais.save(commit=True)
            else:
                formPais.save(commit=False)
        elif request.POST["accion"] == "localidad":
            if formLocalidad.is_valid():
                formLocalidad.save()
    return render(request, "core/regionAdmin.html", {"paises": paises, "localidades": localidades, "provincias": provincias, "formPais": formPais, "formProvincia": formProvincia, "formLocalidad": formLocalidad})
    

def logout(request):
    if not request.user.is_authenticated:
        logout(request)

    # Redirect to a success page.
    return redirect(home)
