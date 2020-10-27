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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Sensor'
        context['entity'] = 'Sensor'
        context['list_url'] = reverse_lazy('sensor_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context
    

class SensorUpdate(UpdateView):
    model = Sensor
    form_class = SensorForm
    template_name = 'gestion_riego/sensor/sensor_create.html'
    success_url = reverse_lazy('sensor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Sensor'
        context['entity'] = 'Sensor'
        context['list_url'] = reverse_lazy('sensor_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context

class SensorDelete(DeleteView):
    model = Sensor
    template_name = 'gestion_riego/sensor/sensor_verificacion.html'
    success_url = reverse_lazy('sensor_list')

class SensorList(ListView):
    model = Sensor
    template_name = 'gestion_riego/sensor/sensor_list.html'

    def get_queryset(self):
        return self.model.objects.all()[:50] #Trae solo dos objetos

def lectura(request):
    sensor = Sensor.objects.first()
    print(sensor)
    contexto = {
        
    }
    return render(request, 'gestion_riego/sensor/dashboard.html', contexto)