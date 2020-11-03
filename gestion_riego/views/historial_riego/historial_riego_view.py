from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from gestion_riego.models import HistorialRiego


# Vistas basadas en clases
# Recomendable y haca a la aplicacion facilmente escalable
class HistorialRiegoListView(ListView):
    model = HistorialRiego
    template_name = 'gestion_riego/historial_riego/historial_riego.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Riego'
        context['entity'] = 'HistorialRiego'
        context['list_url'] = reverse_lazy('gestion_riego:historial_riego')
        return context
