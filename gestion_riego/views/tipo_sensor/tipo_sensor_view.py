from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from gestion_riego.models import TipoSensor
from gestion_riego.forms import TipoSensorForm


# Vistas basadas en clases
# Recomendable y haca a la aplicacion facilmente escalable
class TipoSensorCreateView(CreateView):
    model = TipoSensor
    form_class = TipoSensorForm
    template_name = 'gestion_riego/tipo_sensor/tipo_sensor_create.html'
    success_url = reverse_lazy('gestion_riego:tipo_sensor_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Tipo Sensor'
        context['entity'] = 'tipo_sensor'
        context['list_url'] = reverse_lazy('gestion_riego:tipo_sensor_list')
        context['action'] = 'add'
        # context['object_list'] = Device.objects.all()
        return context


class TipoSensorUpdateView(UpdateView):
    model = TipoSensor
    form_class = TipoSensorForm
    template_name = 'gestion_riego/tipo_sensor/tipo_sensor_create.html'
    success_url = reverse_lazy('gestion_riego:tipo_sensor_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Tipo Sensor'
        context['entity'] = 'tipo_sensor'
        context['list_url'] = reverse_lazy('gestion_riego:tipo_sensor_list')
        context['action'] = 'edit'
        # context['object_list'] = Device.objects.all()
        return context


class TipoSensorDeleteView(DeleteView):
    model = TipoSensor
    template_name = 'gestion_riego/tipo_sensor/tipo_sensor_verificacion.html'
    success_url = reverse_lazy('gestion_riego:tipo_sensor_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Tipo Sensor'
        context['entity'] = 'tipo_sensor'
        context['action'] = 'delete'
        # context['object_list'] = Device.objects.all()
        return context


class TipoSensorListView(ListView):
    model = TipoSensor
    template_name = 'gestion_riego/tipo_sensor/tipo_sensor_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista Tipo de Sensores'
        context['entity'] = 'tipo_sensor'
        context['create_url'] = reverse_lazy('gestion_riego:tipo_sensor_create')
        context['list_url'] = reverse_lazy('gestion_riego:tipo_sensor_list')
        return context
