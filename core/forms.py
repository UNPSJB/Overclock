from django.forms import ModelForm, ValidationError
from core.models import Localidad, Pais, Provincia, Persona, TipoHabitacion, Servicio
from django.contrib.auth.forms import AuthenticationForm

# 
class PaisForm(ModelForm):
    class Meta:
        model = Pais
        fields = '__all__'
   
    
    def __init__(self, *args, **kwargs):
        super(PaisForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})


class ProvinciaForm(ModelForm):
    class Meta:
        model = Provincia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProvinciaForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})


class LocalidadForm(ModelForm):
    class Meta:
        model = Localidad
        fields = '__all__'
        

    def __init__(self, *args, **kwargs):
        super(LocalidadForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        

class AutenticacionForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(AutenticacionForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Ingrese su usuario'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Ingrese su Clave'})
        self.fields['username'].label = ''
        self.fields['password'].label = ''

class TipoHabitacionForm(ModelForm):
    class Meta:
        model=TipoHabitacion
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(TipoHabitacionForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})   
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})
        self.fields['pasajeros'].widget.attrs.update({'class': 'form-control'})
        self.fields['cuartos'].widget.attrs.update({'class': 'form-control'})

class ServicioForm(ModelForm):
    class Meta:
        model=Servicio
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})   
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})

