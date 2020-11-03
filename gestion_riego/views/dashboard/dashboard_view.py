from django.core import serializers
from django.shortcuts import render

from gestion_riego.models import Device


def dashboard(request):
    devices = Device.objects.all()
    data = serializers.serialize('json', devices)
    print(data)
    contexto = {
        'devices': devices,
    }
    return render(request, 'gestion_riego/dashboard/dashboard.html', contexto)
