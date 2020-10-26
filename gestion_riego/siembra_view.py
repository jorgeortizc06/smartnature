from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import Siembra
from .forms import SiembraForm
import serial, json

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class SiembraCreate(CreateView):
    model = Siembra
    form_class = SiembraForm
    template_name = 'gestion_riego/siembra/siembra_create.html'
    success_url = reverse_lazy('siembra_list')
    

class SiembraUpdate(UpdateView):
    model = Siembra
    form_class = SiembraForm
    template_name = 'gestion_riego/siembra/siembra_create.html'
    success_url = reverse_lazy('siembra_list')

class SiembraDelete(DeleteView):
    model = Siembra
    template_name = 'gestion_riego/siembra/siembra_verificacion.html'
    success_url = reverse_lazy('siembra_list')

class SiembraList(ListView):
    model = Siembra
    template_name = 'gestion_riego/siembra/siembra_list.html'