from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import Sensor
from .forms import SensorForm
import serial, json

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
        return self.model.objects.all()[:5] #Trae solo dos objetos

def lectura(request):
    sensor = Sensor.objects.first()
    print(sensor)
    contexto = {
        'id': sensor.id,
        'temp_ambiental': sensor.temp_ambiente,
        'humed_ambiental' : sensor.humed_ambiente,
        'humed_suelo' : sensor.humed_suelo,
    }
    return render(request, 'gestion_riego/sensor/dashboard.html', contexto)