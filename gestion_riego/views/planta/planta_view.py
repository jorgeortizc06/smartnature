from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from gestion_riego.models import Planta
from gestion_riego.forms import PlantaForm
import serial, json

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class PlantaCreateView(CreateView):
    model = Planta
    form_class = PlantaForm
    template_name = 'gestion_riego/planta/planta_create.html'
    success_url = reverse_lazy('gestion_riego:planta_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Planta'
        context['entity'] = 'Planta'
        context['list_url'] = reverse_lazy('gestion_riego:planta_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context
    

class PlantaUpdateView(UpdateView):
    model = Planta
    form_class = PlantaForm
    template_name = 'gestion_riego/planta/planta_create.html'
    success_url = reverse_lazy('gestion_riego:planta_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Planta'
        context['entity'] = 'Planta'
        context['list_url'] = reverse_lazy('planta_list')
        context['action'] = 'edit'
        #context['object_list'] = Device.objects.all()
        return context

class PlantaDeleteView(DeleteView):
    model = Planta
    template_name = 'gestion_riego/planta/planta_verificacion.html'
    success_url = reverse_lazy('gestion_riego:planta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Planta'
        context['entity'] = 'Planta'
        context['list_url'] = reverse_lazy('gestion_riego:device_list')
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class PlantaListView(ListView):
    model = Planta
    template_name = 'gestion_riego/planta/planta_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listas de Plantas'
        context['entity'] = 'Planta'
        context['create_url'] = reverse_lazy('gestion_riego:planta_create')
        context['list_url'] = reverse_lazy('gestion_riego:planta_list')
        context['action'] = 'edit'
        #context['object_list'] = Device.objects.all()
        return context
