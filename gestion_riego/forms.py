from django import forms
from .models import Persona, Sensor, TipoSensor, Device

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__' #tambien ('nombre', 'apellido',....)

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = '__all__' #tambien ('nombre', 'apellido',....)

class TipoSensorForm(forms.ModelForm):
    class Meta:
        model = TipoSensor
        fields = '__all__'

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'