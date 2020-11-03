from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from gestion_riego.models import Sensor
from gestion_riego.forms import SensorForm


# Vistas basadas en clases
# Recomendable y haca a la aplicacion facilmente escalable
class SensorCreateView(CreateView):
    model = Sensor
    form_class = SensorForm
    template_name = 'gestion_riego/sensor/sensor_create.html'
    success_url = reverse_lazy('gestion_riego:sensor_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Sensor'
        context['entity'] = 'Sensor'
        context['list_url'] = reverse_lazy('gestion_riego:sensor_list')
        context['action'] = 'add'
        # context['object_list'] = Device.objects.all()
        return context


class SensorUpdateView(UpdateView):
    model = Sensor
    form_class = SensorForm
    template_name = 'gestion_riego/sensor/sensor_create.html'
    success_url = reverse_lazy('gestion_riego:sensor_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Sensor'
        context['entity'] = 'Sensor'
        context['list_url'] = reverse_lazy('gestion_riego:sensor_list')
        context['action'] = 'add'
        # context['object_list'] = Device.objects.all()
        return context


class SensorDeleteView(DeleteView):
    model = Sensor
    template_name = 'gestion_riego/sensor/sensor_verificacion.html'
    success_url = reverse_lazy('gestion_riego:sensor_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Sensor'
        context['entity'] = 'Sensor'
        context['list_url'] = reverse_lazy('gestion_riego:sensor_delete')
        return context


class SensorListView(ListView):
    model = Sensor
    template_name = 'gestion_riego/sensor/sensor_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()[:50]  # Trae solo dos objetos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Sensores Sensor'
        context['entity'] = 'Sensor'
        context['create_url'] = reverse_lazy('gestion_riego:sensor_create')
        context['list_url'] = reverse_lazy('gestion_riego:sensor_list')
        return context


def lectura(request):
    sensor = Sensor.objects.first()
    print(sensor)
    contexto = {

    }
    return render(request, 'gestion_riego/sensor/dashboard.html', contexto)
