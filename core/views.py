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

# Modal
class PaisCreate(CreateView):
    model = Pais
    fields = '__all__'
    template_name = 'core/modals/pais_form.html'
    form = PaisForm
    success_url = "ok"

# Create your views here.
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
                    return redirect("core:listadoLocalidades")
                else:
                    # Y le redireccionamos a la portada
                    return redirect(correctaVendedor)
            else:
                return render(request, "home.html", {'form': form})

    # Si llegamos al final renderizamos el formulario
    return render(request, "home.html", {'form': form})


# def home(request):
#     paises=Pais.objects.all()
#     provincias=Provincia.objects.all()
#     form = UsuarioLoginForm()
#     return render(request, "home.html", {"form": form, "provincias": provincias})


def correctaAdmin(request):
    paises = Pais.objects.all()
    provincias = Provincia.objects.all()
    localidades = Localidad.objects.all()
    #FIXME cuando no vienen datos en el POST  por ser un GET, la instanciacion tendria que ser 
    formPais = PaisForm(request.POST)
    formProvincia = ProvinciaForm(request.POST)
    formLocalidad = LocalidadForm(request.POST)
    
    if request.method == "POST":
        #TODO garantizar que si los forms tienen errores las modales se vuelvan a abrir indicando el error
        #print(request.POST)
        if request.POST["accion"]=="provincia":
            if formProvincia.is_valid():
                formProvincia.save()
        elif request.POST["accion"]=="pais":
            if formPais.is_valid():
                formPais.save()
        elif request.POST["accion"]=="localidad":
            if formLocalidad.is_valid():
                formLocalidad.save()
    return render(request, "base/administrador.html", {"paises": paises, "localidades": localidades, "provincias": provincias, "formPais": formPais, "formProvincia": formProvincia, "formLocalidad": formLocalidad})


def altaPais(request):
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = PaisForm(request.POST)
        if form.is_valid():  # Si el formulario es válido...
            # Guardamos el formulario pero sin confirmarlo, así conseguiremos una instancia para manejarla
            instancia = form.save(commit=True)
            return redirect('core:listadoLocalidades')


def altaProvincia(request):
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = ProvinciaForm(request.POST)
        if form.is_valid():  # Si el formulario es válido...
            # Guardamos el formulario pero sin confirmarlo, así conseguiremos una instancia para manejarla
            instancia = form.save(commit=True)
        else:
            pass
           # mensajes.error("NOMBRE NO PUEDE SER CADENA VACIA...") ---> spike
    return redirect('core:listadoLocalidades')


def correctaVendedor(request):

    return render(request, "base/vendedor.html")


def logout(request):
    if not request.user.is_authenticated:
        logout(request)

    # Redirect to a success page.
    return redirect(home)
