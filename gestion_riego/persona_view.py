from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import Persona
from .forms import PersonaForm

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class PersonaList(ListView):
    model = Persona
    template_name = 'gestion_riego/persona/persona_list.html'

    """
    def get_queryset(self):
        return self.model.objects.all()[:2] #Trae solo dos objetos"""

class PersonaCreate(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'gestion_riego/persona/persona_create.html'
    success_url = reverse_lazy('persona_list')

class PersonaUpdate(UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'gestion_riego/persona/persona_create.html'
    success_url = reverse_lazy('persona_list')

class PersonaDelete(DeleteView):
    model = Persona
    template_name = 'gestion_riego/persona/persona_verificacion.html'
    success_url = reverse_lazy('persona_list')