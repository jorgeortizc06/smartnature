from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import Planta
from .forms import PlantaForm
import serial, json

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class PlantaCreate(CreateView):
    model = Planta
    form_class = PlantaForm
    template_name = 'gestion_riego/planta/planta_create.html'
    success_url = reverse_lazy('planta_list')
    

class PlantaUpdate(UpdateView):
    model = Planta
    form_class = PlantaForm
    template_name = 'gestion_riego/planta/planta_create.html'
    success_url = reverse_lazy('planta_list')

class PlantaDelete(DeleteView):
    model = Planta
    template_name = 'gestion_riego/planta/planta_verificacion.html'
    success_url = reverse_lazy('planta_list')

class PlantaList(ListView):
    model = Planta
    template_name = 'gestion_riego/planta/planta_list.html'