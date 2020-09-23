from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import TipoSuelo
from .forms import TipoSueloForm
import serial, json

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class TipoSueloCreate(CreateView):
    model = TipoSuelo
    form_class = TipoSueloForm
    template_name = 'gestion_riego/tipo_suelo/tipo_suelo_create.html'
    success_url = reverse_lazy('tipo_suelo_list')
    

class TipoSueloUpdate(UpdateView):
    model = TipoSuelo
    form_class = TipoSueloForm
    template_name = 'gestion_riego/tipo_suelo/tipo_suelo_create.html'
    success_url = reverse_lazy('tipo_suelo_list')

class TipoSueloDelete(DeleteView):
    model = TipoSuelo
    template_name = 'gestion_riego/tipo_suelo/tipo_suelo_verificacion.html'
    success_url = reverse_lazy('tipo_suelo_list')

class TipoSueloList(ListView):
    model = TipoSuelo
    template_name = 'gestion_riego/tipo_suelo/tipo_suelo_list.html'
