from django.forms import widgets, MultipleChoiceField, CheckboxSelectMultiple
from django.forms import ModelForm, ValidationError, forms, DateInput, DateField
from django.contrib.auth.forms import AuthenticationForm
from django.forms.fields import EmailField
from django.forms.widgets import NumberInput

from hotel.models import Hotel, PrecioPorTipo, TemporadaAlta, Habitacion
from core.models import Servicio, TipoHabitacion, Vendedor



class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'
        exclude = ['servicios', 'tipos', 'vendedores']
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


class TemporadaHotelForm(ModelForm):
    class Meta:
        model = TemporadaAlta
        fields = '__all__'
        exclude = ['hotel']
        widgets = {
            'inicio': DateInput(attrs={'type': 'date'}),
            'fin': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(TemporadaHotelForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['inicio'].widget.attrs.update({'class': 'form-control'})
        self.fields['fin'].widget.attrs.update({'class': 'form-control'})
   

class AgregarTipoAHotelForm(ModelForm):
    class Meta:
        model = PrecioPorTipo
        fields = '__all__'
        exclude = ['hotel']

    def __init__(self, *args, **kwargs):
        super(AgregarTipoAHotelForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs.update({'class': 'form-control'})
        self.fields['baja'].widget.attrs.update({'class': 'form-control'})
        self.fields['alta'].widget.attrs.update({'class': 'form-control'})

class HabitacionForm(ModelForm):
    class Meta:
        model = Habitacion
        fields='__all__'
        exclude=['hotel','baja']
     
    def __init__(self, *args, **kwargs):
        super(HabitacionForm, self).__init__(*args, **kwargs)
        self.fields['numero'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo'].widget.attrs.update({'class': 'form-control'})
        