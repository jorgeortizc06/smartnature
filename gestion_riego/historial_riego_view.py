from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import HistorialRiego

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable

class HistorialRiegoList(ListView):
    model = HistorialRiego
    template_name = 'gestion_riego/historial_riego/historial_riego.html'

    def get_queryset(self):
        return self.model.objects.all()[:10]