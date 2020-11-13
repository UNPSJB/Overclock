from django.forms import widgets, MultipleChoiceField, CheckboxSelectMultiple
from django.forms import ModelForm, ValidationError, forms
from django.contrib.auth.forms import AuthenticationForm
from hotel.models import Hotel
from core.models import Servicio, TipoHabitacion

class HotelForm(ModelForm):
    class Meta:
        model=Hotel
        fields = '__all__'
        exclude = ['vendedores'] 
        # Debemos quitar vendedores de aca ya que nosotros tenemos un crear vendedor
        # y asignar vendedor a hotel
    
    def __init__(self, *args, **kwargs):
        super(HotelForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})   
        self.fields['localidad'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['encargado'].widget.attrs.update({'class': 'form-control'})
        self.fields['categoria'].widget.attrs.update({'class': 'form-control'})
        self.fields['servicios'].widget.attrs.update({'class': 'form-check-input form-check-label laSeleccionBox'})
        self.fields['servicios'].choices=[(c.pk,c.nombre) for c in Servicio.objects.all()]
        self.fields['tipos'].widget.attrs.update({'class': 'form-check-input form-check-label laSeleccionBox'})
        self.fields['tipos'].choices=[(c.pk,c.nombre) for c in TipoHabitacion.objects.all()]

    servicios = MultipleChoiceField(
        widget=CheckboxSelectMultiple,        
    )
    tipos = MultipleChoiceField(
        widget=CheckboxSelectMultiple,        
    )