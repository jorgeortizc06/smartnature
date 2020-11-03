from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from gestion_riego.models import Planta
from gestion_riego.forms import PlantaForm
import serial, json

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class PlantaCreate(CreateView):
    model = Planta
    form_class = PlantaForm
    template_name = 'gestion_riego/planta/planta_create.html'
    success_url = reverse_lazy('planta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Planta'
        context['entity'] = 'Planta'
        context['list_url'] = reverse_lazy('planta_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context
    

class PlantaUpdate(UpdateView):
    model = Planta
    form_class = PlantaForm
    template_name = 'gestion_riego/planta/planta_create.html'
    success_url = reverse_lazy('planta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Planta'
        context['entity'] = 'Planta'
        context['list_url'] = reverse_lazy('planta_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context

class PlantaDelete(DeleteView):
    model = Planta
    template_name = 'gestion_riego/planta/planta_verificacion.html'
    success_url = reverse_lazy('planta_list')

class PlantaList(ListView):
    model = Planta
    template_name = 'gestion_riego/planta/planta_list.html'