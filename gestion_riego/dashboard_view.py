from django.shortcuts import render, redirect
import json
from .models import Device
from django.core import serializers

def dashboard(request):
    sensores = Device.objects.all()
    data = serializers.serialize('json', sensores)
    print(data)
    contexto = {
        'sensores': sensores
    }
    return render(request, 'gestion_riego/dashboard/dashboard.html', contexto)  