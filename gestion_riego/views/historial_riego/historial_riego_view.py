from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from rest_framework import viewsets
from gestion_riego.serializers import HistorialRiegoSerializer

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
        return self.model.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Riego'
        context['entity'] = 'HistorialRiego'
        context['list_url'] = reverse_lazy('gestion_riego:historial_riego')
        return context

class HistorialRiegoViewSet(viewsets.ModelViewSet):
    serializer_class = HistorialRiegoSerializer
    queryset = HistorialRiego.objects.all().order_by('id') #ordenados por id