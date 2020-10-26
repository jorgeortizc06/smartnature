from django import forms
from .models import Persona, Sensor, TipoSensor, Device, TipoSuelo, Planta, Plataforma, Siembra

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__' #tambien ('nombre', 'apellido',....)

class PlataformaForm(forms.ModelForm):
    class Meta:
        model = Plataforma
        fields = '__all__'

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = '__all__' #tambien ('nombre', 'apellido',....)

class TipoSueloForm(forms.ModelForm):
    class Meta:
        model = TipoSuelo
        fields = '__all__'

class TipoSensorForm(forms.ModelForm):
    class Meta:
        model = TipoSensor
        fields = '__all__'

class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = '__all__'

class SiembraForm(forms.ModelForm):
    class Meta:
        model = Siembra
        fields = '__all__'

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'