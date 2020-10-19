from django.forms import ModelForm
from core.models import Pais, Provincia, Persona
from django.contrib.auth.forms import AuthenticationForm



class PaisForm(ModelForm):
    class Meta:
        model = Pais
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(PaisForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control'})


class AutenticacionForm(AuthenticationForm):
    
    
       
    def __init__(self, *args, **kwargs):
        super(AutenticacionForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Ingrese su usuario'})
        self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'Ingrese su Clave'})
        self.fields['username'].label = ''
        self.fields['password'].label = ''