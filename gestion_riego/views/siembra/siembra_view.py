from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from gestion_riego.models import Siembra
from gestion_riego.forms import SiembraForm
import serial, json

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class SiembraCreateView(CreateView):
    model = Siembra
    form_class = SiembraForm
    template_name = 'gestion_riego/siembra/siembra_create.html'
    success_url = reverse_lazy('gestion_riego:siembra_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Siembra'
        context['entity'] = 'Siembra'
        context['list_url'] = reverse_lazy('gestion_riego:siembra_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context

class SiembraUpdateView(UpdateView):
    model = Siembra
    form_class = SiembraForm
    template_name = 'gestion_riego/siembra/siembra_create.html'
    success_url = reverse_lazy('gestion_riego:siembra_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Siembra'
        context['entity'] = 'Siembra'
        context['list_url'] = reverse_lazy('gestion_riego:siembra_list')
        context['action'] = 'edit'
        #context['object_list'] = Device.objects.all()
        return context

class SiembraDeleteView(DeleteView):
    model = Siembra
    template_name = 'gestion_riego/siembra/siembra_verificacion.html'
    success_url = reverse_lazy('gestion_riego:siembra_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Siembra'
        context['entity'] = 'Siembra'
        context['list_url'] = reverse_lazy('gestion_riego:siembra_list')
        context['action'] = 'delete'
        return context

class SiembraListView(ListView):
    model = Siembra
    template_name = 'gestion_riego/siembra/siembra_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Siembra'
        context['entity'] = 'Siembra'
        context['create_url'] = reverse_lazy('gestion_riego:siembra_create')
        context['list_url'] = reverse_lazy('gestion_riego:siembra_list')
        return context