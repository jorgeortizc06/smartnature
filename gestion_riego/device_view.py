from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Device
from .forms import DeviceForm
from django.http import JsonResponse, HttpResponseRedirect
import serial, json

#Vistas basadas en clases
#Recomendable y haca a la aplicacion facilmente escalable
class DeviceCreate(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'gestion_riego/device/device_create.html'
    success_url = reverse_lazy('device_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo dispositivo'
        context['entity'] = 'Device'
        context['list_url'] = reverse_lazy('device_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context
    """def post(self, request, *args, **kwargs):
        print(request.POST)
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        return render(request, self.template_name, {'form':form})"""

class DeviceUpdate(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'gestion_riego/device/device_create.html'
    success_url = reverse_lazy('device_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de dispositivo'
        context['entity'] = 'Device'
        context['list_url'] = reverse_lazy('device_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context
class DeviceDelete(DeleteView):
    model = Device
    template_name = 'gestion_riego/device/device_verificacion.html'
    success_url = reverse_lazy('device_list')

class DeviceList(ListView):
    model = Device
    template_name = 'gestion_riego/device/device_list.html'

    ####Sobreescribir metodos####
    #Metodos para devolver algo especifico
    def get_queryset(self):
        return Device.objects.all()

    @method_decorator(csrf_exempt) #Al hacer post, va a salir forbideen 404, necesitas proteger la vista
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs): #recuerda poner csrf_exempt a traves de un decorador. En este caso ya esta definido
        data = {}
        try:
            data = Device.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    #Metodo para modificar el context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de dispositivos'
        context['entity'] = 'Device'
        context['list_url'] = reverse_lazy('device_list')
        context['action'] = 'add'
        #context['object_list'] = Device.objects.all()
        return context

def device_dashboard(request):
    return render(request, 'gestion_riego/dashboard/index.html')
