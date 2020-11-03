from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from gestion_riego.forms import DeviceForm
from gestion_riego.models import Device


# Vistas basadas en clases
# Recomendable y haca a la aplicacion facilmente escalable
class DeviceCreateView(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'gestion_riego/device/device_create.html'
    success_url = reverse_lazy('gestion_riego:device_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo dispositivo'
        context['entity'] = 'Device'
        context['list_url'] = reverse_lazy('gestion_riego:device_list')
        context['action'] = 'add'
        # context['object_list'] = Device.objects.all()
        return context

    """def post(self, request, *args, **kwargs):
        print(request.POST)
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        return render(request, self.template_name, {'form':form})"""


class DeviceUpdateView(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'gestion_riego/device/device_create.html'
    success_url = reverse_lazy('gestion_riego:device_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de dispositivo'
        context['entity'] = 'Device'
        context['list_url'] = reverse_lazy('gestion_riego:device_list')
        context['action'] = 'edit'
        # context['object_list'] = Device.objects.all()
        return context


class DeviceDeleteView(DeleteView):
    model = Device
    template_name = 'gestion_riego/device/device_verificacion.html'
    success_url = reverse_lazy('gestion_riego:device_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Categoria'
        context['entity'] = 'Device'
        context['list_url'] = reverse_lazy('gestion_riego:device_list')
        return context


class DeviceListView(ListView):
    model = Device
    template_name = 'gestion_riego/device/device_list.html'

    ####Sobreescribir metodos####
    # Metodos para devolver algo especifico
    def get_queryset(self):
        return Device.objects.all()

    @method_decorator(csrf_exempt)  # Al hacer post, va a salir forbideen 404, necesitas proteger la vista
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Metodo para modificar el context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de dispositivos'
        context['entity'] = 'Device'
        context['create_url'] = reverse_lazy('gestion_riego:device_create')
        context['list_url'] = reverse_lazy('gestion_riego:device_list')
        # context['object_list'] = Device.objects.all()
        return context


def device_dashboard(request):
    return render(request, 'gestion_riego/dashboard/index.html')
