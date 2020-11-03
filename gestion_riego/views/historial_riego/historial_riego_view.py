from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from gestion_riego.models import HistorialRiego

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable

class HistorialRiegoList(ListView):
    model = HistorialRiego
    template_name = 'gestion_riego/historial_riego/historial_riego.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()