from django.shortcuts import render, redirect
from .models import Persona
from .forms import PersonaForm
# Create your views here.
#Vistas basadas en funciones. No es recomendable y hace mas dificil la escalacion
def list_persona(request):
    personas = Persona.objects.all()           #select * from persona
    print(personas)
    #Contexto: para enviar personas a html se almacena en un diccionario
    contexto = {
        'personas':personas
    }
    return render(request, 'gestion_riego/list_persona.html', contexto)

def new_persona(request):
    if request.method == 'GET':
        form = PersonaForm()
        contexto = {
            'form': form
        }
    else:
        form = PersonaForm(request.POST)
        print(form)
        contexto = {
            'form': form
        }
        if form.is_valid():
            form.save()
            return redirect('list_persona')
    return render(request, 'gestion_riego/new_persona.html', contexto)

def edit_persona(request, id):
    persona = Persona.objects.get(id = id)
    if request.method == 'GET':
        form = PersonaForm(instance = persona)
        contexto = {
            'form': form
        }
    else:
        form = PersonaForm(request.POST, instance = persona)
        contexto = {
            'form': form
        }
        if form.is_valid():
            form.save()
            return redirect('list_persona')
    return render(request, 'gestion_riego/new_persona.html', contexto)

def delete_persona(request, id):
    persona = Persona.objects.get(id = id)
    persona.delete()
    return redirect('list_persona')


