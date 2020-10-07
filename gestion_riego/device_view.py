from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import Device
from .forms import DeviceForm
import serial, json

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class DeviceCreate(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'gestion_riego/device/device_create.html'
    success_url = reverse_lazy('device_list')
    

class DeviceUpdate(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'gestion_riego/device/device_create.html'
    success_url = reverse_lazy('device_list')

class DeviceDelete(DeleteView):
    model = Device
    template_name = 'gestion_riego/device/device_verificacion.html'
    success_url = reverse_lazy('device_list')

class DeviceList(ListView):
    model = Device
    template_name = 'gestion_riego/device/device_list.html'

def dashboard(request):
    return render(request, 'gestion_riego/dashboard/index.html')
