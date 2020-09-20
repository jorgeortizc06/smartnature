from django import forms
from .models import Persona, Sensor

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__' #tambien ('nombre', 'apellido',....)

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = '__all__' #tambien ('nombre', 'apellido',....)