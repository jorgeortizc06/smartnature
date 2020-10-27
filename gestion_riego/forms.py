from django.forms import *
from .models import Persona, Sensor, TipoSensor, Device, TipoSuelo, Planta, Plataforma, Siembra

class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = '__all__' #tambien ('nombre', 'apellido',....)

class PlataformaForm(ModelForm):
    class Meta:
        model = Plataforma
        fields = '__all__'

class SensorForm(ModelForm):
    class Meta:
        model = Sensor
        fields = '__all__' #tambien ('nombre', 'apellido',....)

class TipoSueloForm(ModelForm):
    class Meta:
        model = TipoSuelo
        fields = '__all__'

class TipoSensorForm(ModelForm):
    class Meta:
        model = TipoSensor
        fields = '__all__'

class PlantaForm(ModelForm):
    class Meta:
        model = Planta
        fields = '__all__'

class SiembraForm(ModelForm):
    class Meta:
        model = Siembra
        fields = '__all__'

class DeviceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True
    class Meta:
        model = Device
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre al dispositivo',
                }
            ),
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la descripcion',
                }
            ),
        }