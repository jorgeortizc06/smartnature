from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from gestion_riego.forms import TipoSueloForm
from gestion_riego.models import TipoSuelo


# Vistas basadas en clases
# Recomendable y haca a la aplicacion facilmente escalable
class TipoSueloCreateView(CreateView):
    model = TipoSuelo
    form_class = TipoSueloForm
    template_name = 'gestion_riego/tipo_suelo/tipo_suelo_create.html'
    success_url = reverse_lazy('gestion_riego:tipo_suelo_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Tipo Suelo'
        context['entity'] = 'tipo_suelo'
        context['list_url'] = reverse_lazy('gestion_riego:tipo_suelo_list')
        context['action'] = 'add'
        return context


class TipoSueloUpdateView(UpdateView):
    model = TipoSuelo
    form_class = TipoSueloForm
    template_name = 'gestion_riego/tipo_suelo/tipo_suelo_create.html'
    success_url = reverse_lazy('gestion_riego:tipo_suelo_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Suelo'
        context['entity'] = 'tipo_suelo'
        context['list_url'] = reverse_lazy('gestion_riego:tipo_suelo_list')
        context['action'] = 'edit'
        return context


class TipoSueloDeleteView(DeleteView):
    model = TipoSuelo
    template_name = 'gestion_riego/tipo_suelo/tipo_suelo_verificacion.html'
    success_url = reverse_lazy('gestion_riego:tipo_suelo_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Suelo'
        context['entity'] = 'tipo_suelo'
        context['list_url'] = reverse_lazy('gestion_riego:tipo_suelo_list')
        return context


class TipoSueloListView(ListView):
    model = TipoSuelo
    template_name = 'gestion_riego/tipo_suelo/tipo_suelo_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Suelos'
        context['entity'] = 'tipo_suelo'
        context['create_url'] = reverse_lazy('gestion_riego:tipo_suelo_create')
        context['list_url'] = reverse_lazy('gestion_riego:tipo_suelo_list')
        return context
