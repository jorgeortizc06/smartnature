from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import TipoSensor
from .forms import TipoSensorForm
import serial, json

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class TipoSensorCreate(CreateView):
    model = TipoSensor
    form_class = TipoSensorForm
    template_name = 'gestion_riego/tipo_sensor/tipo_sensor_create.html'
    success_url = reverse_lazy('tipo_sensor_list')
    

class TipoSensorUpdate(UpdateView):
    model = TipoSensor
    form_class = TipoSensorForm
    template_name = 'gestion_riego/tipo_sensor/tipo_sensor_create.html'
    success_url = reverse_lazy('tipo_sensor_list')

class TipoSensorDelete(DeleteView):
    model = TipoSensor
    template_name = 'gestion_riego/tipo_sensor/tipo_sensor_verificacion.html'
    success_url = reverse_lazy('tipo_sensor_list')

class TipoSensorList(ListView):
    model = TipoSensor
    template_name = 'gestion_riego/tipo_sensor/tipo_sensor_list.html'
