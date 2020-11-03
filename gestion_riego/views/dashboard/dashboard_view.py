from django.shortcuts import render

from django.utils.decorators import method_decorator

from gestion_riego.models import Device
from django.core import serializers


def dashboard(request):
    devices = Device.objects.all()
    data = serializers.serialize('json', devices)
    print(data)
    contexto = {
        'devices': devices,
    }
    return render(request, 'gestion_riego/dashboard/dashboard.html', contexto)
