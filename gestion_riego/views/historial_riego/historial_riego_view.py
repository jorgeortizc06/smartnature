from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from rest_framework import viewsets
from gestion_riego.serializers import HistorialRiegoSerializer
from django.db.models import Sum
from django.db.models.functions import Coalesce
from gestion_riego.models import HistorialRiego


# Vistas basadas en clases
# Recomendable y haca a la aplicacion facilmente escalable
class HistorialRiegoListView(ListView):
    model = HistorialRiego
    template_name = 'gestion_riego/historial_riego/historial_riego.html'

    @method_decorator(csrf_exempt)# para el post desabilito la protección, recuerda que sin la csrf no podra procesar info
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

    #Listar con ajax
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'load_historial_riegos':
                data = []
                for i in HistorialRiego.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) #como uso coleccion de satos agrego safe=False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Riego'
        context['entity'] = 'HistorialRiego'
        context['list_url'] = reverse_lazy('gestion_riego:historial_riego')
        return context

class UsoAguaPorTipoLogicaDifusa(TemplateView):
    model = HistorialRiego
    template_name = 'gestion_riego/historial_riego/uso_agua_tipo_logica_difusa.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}

    def get_graph_historial_riego_month(self, mes, anio):
        data_historial_riego_1_variable = []
        data_historial_riego_3_variable = []
        data_historial_riego_4_variable = []

        data = []
        riego = {}
        try:
            for d in range(1, 32):
                sum_riego_1_variable = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                                   fecha_riego__year=anio, codigo_sensor=5).aggregate(
                    r=Coalesce(Sum('tiempo_riego_1_variable'), 0)).get('r')
                print(sum_riego_1_variable)
                consumo_agua_1_variable = round(float(sum_riego_1_variable)*2.03,2)

                sum_riego_3_variable = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                                   fecha_riego__year=anio, codigo_sensor=5).aggregate(
                    r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                consumo_agua_3_variable = round(float(sum_riego_3_variable)*2.03,2)

                sum_riego_4_variable = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                                     fecha_riego__year=anio, codigo_sensor=5).aggregate(
                    r=Coalesce(Sum('tiempo_riego_4_variable'), 0)).get('r')
                consumo_agua_4_variable = round(float(sum_riego_4_variable)*2.03,2)

                data.append({'dia': d,'data_historial_riego_1_variable': float(sum_riego_1_variable), 'consumo_agua_1_variable': float(consumo_agua_1_variable),
                             'data_historial_riego_3_variable': float(sum_riego_3_variable), 'consumo_agua_3_variable': float(consumo_agua_3_variable),
                             'data_historial_riego_4_variable': float(sum_riego_4_variable), 'consumo_agua_4_variable': float(consumo_agua_4_variable)})



            print(data)

        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #data_historial_riego_month = self.get_graph_historial_riego_month(mes = datetime.now().month, anio = datetime.now().year)
        data_historial_riego_month = self.get_graph_historial_riego_month(mes = 12, anio = 2020)
        context['title'] = 'Consumo de Agua'
        context['entity'] = 'Device'
        context['consumo_agua'] = data_historial_riego_month

        return context

class HistorialRiegoViewSet(viewsets.ModelViewSet):
    serializer_class = HistorialRiegoSerializer
    queryset = HistorialRiego.objects.all() #ordenados por id

