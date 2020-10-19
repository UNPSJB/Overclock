from django.shortcuts import render, HttpResponse, redirect
from core.models import Pais, Provincia, Localidad
from .forms import PaisForm, AutenticacionForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User



# Create your views here.
def ingresoAdmin(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "administrador.html")
    # En otro caso redireccionamos al login
    return redirect('/home.html')

def home(request):
    form =AutenticacionForm()
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
                usr= User.objects.get(username=user)
                
                if usr.groups.filter(name='administrador').exists():
                    return redirect(correctaAdmin)
                else:
                # Y le redireccionamos a la portada
                    return redirect(correctaVendedor)
            else:
                return render(request, "home.html", {'form':form})

    # Si llegamos al final renderizamos el formulario
    return render(request, "home.html", {'form': form})






# def home(request):
#     paises=Pais.objects.all()
#     provincias=Provincia.objects.all()
#     form = UsuarioLoginForm()
#     return render(request, "home.html", {"form": form, "provincias": provincias})

def correctaAdmin(request):
    paises=Pais.objects.all()
    form=PaisForm()

    # Comprobamos si se ha enviado el formulario
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = PaisForm(request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Guardamos el formulario pero sin confirmarlo,
            # así conseguiremos una instancia para manejarla
            instancia = form.save(commit=False)
            # Podemos guardarla cuando queramos
            instancia.save()
            # Después de guardar redireccionamos a la lista
            return redirect('/correctaAdmin')
    return render(request, "base/administrador.html",{"paises": paises, "form":form})

 


def correctaVendedor(request):
    
    return render(request, "base/vendedor.html")




def logout(request):
    if not request.user.is_authenticated:
        logout(request)
    
    # Redirect to a success page.
    return redirect(home)



def paisAdd(request):
    # Creamos un formulario vacío
    paises=Pais.objects.all()
    provincias=Provincia.objects.all()
    form = PaisForm()

    # Comprobamos si se ha enviado el formulario
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = PaisForm(request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Guardamos el formulario pero sin confirmarlo,
            # así conseguiremos una instancia para manejarla
            instancia = form.save(commit=False)
            # Podemos guardarla cuando queramos
            instancia.save()
            # Después de guardar redireccionamos a la lista
            return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "base/agregaPais.html", {'form': form, "paises": paises, "provincias": provincias})