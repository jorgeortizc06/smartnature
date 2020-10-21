from django.shortcuts import render, redirect
import json
from .models import Device
from django.core import serializers

def dashboard(request):
    devices = Device.objects.all()
    data = serializers.serialize('json', devices)
    print(data)
    contexto = {
        'devices': devices,
    }
    return render(request, 'gestion_riego/dashboard/dashboard.html', contexto)  