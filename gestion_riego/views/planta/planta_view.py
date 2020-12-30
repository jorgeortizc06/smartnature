from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, TemplateView
from django.http import JsonResponse
from gestion_riego.forms import PlantaForm
from gestion_riego.models import Planta


# Vistas basadas en clases
# Recomendable y haca a la aplicacion facilmente escalable
class PlantaCreateView(CreateView):
    model = Planta
    form_class = PlantaForm
    template_name = 'gestion_riego/planta/planta_create.html'
    success_url = reverse_lazy('gestion_riego:planta_list')

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
        context['title'] = 'Nueva Planta'
        context['entity'] = 'Planta'
        context['list_url'] = reverse_lazy('gestion_riego:planta_list')
        context['action'] = 'add'
        # context['object_list'] = Device.objects.all()
        return context


class PlantaUpdateView(UpdateView):
    model = Planta
    form_class = PlantaForm
    template_name = 'gestion_riego/planta/planta_create.html'
    success_url = reverse_lazy('gestion_riego:planta_list')

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
        context['title'] = 'Actualizar Planta'
        context['entity'] = 'Planta'
        context['list_url'] = reverse_lazy('gestion_riego:planta_list')
        context['action'] = 'edit'
        # context['object_list'] = Device.objects.all()
        return context


class PlantaDeleteView(DeleteView):
    model = Planta
    template_name = 'gestion_riego/planta/planta_verificacion.html'
    success_url = reverse_lazy('gestion_riego:planta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Planta'
        context['entity'] = 'Planta'
        context['list_url'] = reverse_lazy('gestion_riego:device_list')
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PlantaListView(TemplateView):
    model = Planta
    template_name = 'gestion_riego/planta/planta_list.html'

    @method_decorator(
        csrf_exempt)  # para el post desabilito la protección, recuerda que sin la csrf no podra procesar info
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'load_plantas':
                data = []
                for i in Planta.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listas de Plantas'
        context['entity'] = 'Planta'
        context['create_url'] = reverse_lazy('gestion_riego:planta_create')
        context['list_url'] = reverse_lazy('gestion_riego:planta_list')
        context['action'] = 'edit'
        # context['object_list'] = Device.objects.all()
        return context
