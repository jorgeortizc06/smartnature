from django.shortcuts import render, redirect
from .models import Device

def dashboard(request):
    devices = Device.objects.all()
    print(devices)
    contexto = {
        'devices': devices
    }
    return render(request, 'gestion_riego/dashboard/dashboard.html', contexto)