from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from gestion_riego.models import TipoSuelo
from gestion_riego.forms import TipoSueloForm
import serial, json

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class TipoSueloCreate(CreateView):
    model = TipoSuelo
    form_class = TipoSueloForm
    template_name = 'gestion_riego/tipo_suelo/tipo_suelo_create.html'
    success_url = reverse_lazy('tipo_suelo_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Tipo Suelo'
        context['entity'] = 'tipo_suelo'
        context['list_url'] = reverse_lazy('tipo_suelo_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context

class TipoSueloUpdate(UpdateView):
    model = TipoSuelo
    form_class = TipoSueloForm
    template_name = 'gestion_riego/tipo_suelo/tipo_suelo_create.html'
    success_url = reverse_lazy('tipo_suelo_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Tipo Suelo'
        context['entity'] = 'tipo_suelo'
        context['list_url'] = reverse_lazy('tipo_suelo_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context

class TipoSueloDelete(DeleteView):
    model = TipoSuelo
    template_name = 'gestion_riego/tipo_suelo/tipo_suelo_verificacion.html'
    success_url = reverse_lazy('tipo_suelo_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class TipoSueloList(ListView):
    model = TipoSuelo
    template_name = 'gestion_riego/tipo_suelo/tipo_suelo_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Suelos'
        context['entity'] = 'tipo_suelo'
        context['list_url'] = reverse_lazy('tipo_suelo_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context
