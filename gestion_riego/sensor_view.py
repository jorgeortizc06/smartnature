from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import Sensor
from .forms import SensorForm
import serial

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class SensorCreate(CreateView):
    model = Sensor
    form_class = SensorForm
    template_name = 'gestion_riego/sensor/sensor_create.html'
    success_url = reverse_lazy('sensor_list')
    

class SensorUpdate(UpdateView):
    model = Sensor
    form_class = SensorForm
    template_name = 'gestion_riego/sensor/sensor_create.html'
    success_url = reverse_lazy('sensor_list')

class SensorDelete(DeleteView):
    model = Sensor
    template_name = 'gestion_riego/sensor/sensor_verificacion.html'
    success_url = reverse_lazy('sensor_list')

class SensorList(ListView):
    model = Sensor
    template_name = 'gestion_riego/sensor/sensor_list.html'
    def get_queryset(self):
        return self.model.objects.all()[:1] #Trae solo dos objetos

def lectura(request):
    arduino = serial.Serial("COM3", 9600)
    
    val = arduino.readline()
    print(val)
    humed_ambiente = val.decode().split(";")[0]
    temp_ambiente = val.decode().split(";")[1]
    humed_suelo = val.decode().split(";")[2]

    #Contexto: para enviar personas a html se almacena en un diccionario
    contexto = {
        'temp_ambiente' : temp_ambiente,
        'humed_ambiente' : humed_ambiente,
        'humed_suelo':humed_suelo
    }
    
    arduino.close()
    return render(request, 'gestion_riego/sensor/dashboard.html', contexto)