from django.forms import widgets, MultipleChoiceField, CheckboxSelectMultiple
from django.forms import ModelForm, ValidationError, forms
from django.contrib.auth.forms import AuthenticationForm
from hotel.models import Hotel

class HotelForm(ModelForm):
    class Meta:
        model=Hotel
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(HotelForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})   
        self.fields['localidad'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['encargado'].widget.attrs.update({'class': 'form-control'})
        self.fields['categoria'].widget.attrs.update({'class': 'form-control'})