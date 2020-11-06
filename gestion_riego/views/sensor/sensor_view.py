from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.http import JsonResponse
from gestion_riego.forms import SensorForm
from gestion_riego.models import Sensor


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

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(action)
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

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
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(action)
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

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