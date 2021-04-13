from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, TemplateView
from django.http import JsonResponse
from gestion_riego.forms import SensorForm
from gestion_riego.models import Sensor
from rest_framework import viewsets
from gestion_riego.serializers import SensorSerializer
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


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
        context['action'] = 'edit'
        # context['object_list'] = Device.objects.all()
        return context


class SensorDeleteView(DeleteView):
    model = Sensor
    template_name = 'gestion_riego/sensor/sensor_verificacion.html'
    success_url = reverse_lazy('gestion_riego:sensor_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Sensor'
        context['entity'] = 'Sensor'
        context['list_url'] = reverse_lazy('gestion_riego:sensor_list')
        return context


class SensorListView(TemplateView):
    model = Sensor
    template_name = 'gestion_riego/sensor/sensor_list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # Obtengo datos del mes actual, y sin el caudal y consumo de agua
                sensores = Sensor.objects.filter(fecha_registro__month=datetime.now().month,
                                                 fecha_registro__year=datetime.now().year).exclude(
                    tipo_sensor_id=4).exclude(tipo_sensor_id=5)
                for i in sensores:
                    data.append(i.toJSON())
            elif action == 'search_historial_sensores_month_datatable':
                dateForDatable = request.POST['fecha']
                fecha = datetime.strptime(dateForDatable, '%Y-%m-%d')  # convierto a fecha para que python lo entienda
                dia = fecha.day
                mes = fecha.month
                anio = fecha.year
                data = []
                sensores = Sensor.objects.filter(fecha_registro__day=dia, fecha_registro__month=mes,
                                                 fecha_registro__year=anio).exclude(tipo_sensor=4).exclude(
                    tipo_sensor=5)
                print(sensores)
                for sensor in sensores:
                    data.append(sensor.toJSON())

            elif action == 'search_historial_sensores_month':
                dateForChart = request.POST['fecha']
                fecha = datetime.strptime(dateForChart, '%Y-%m-%d')  # convierto a fecha para que python lo entienda
                formateo_fecha = datetime.strftime(fecha, '%B')  # ne sirve para visualizarlo en el chart
                dia = fecha.day
                mes = fecha.month
                anio = fecha.year
                data = []
                sensor_avgs = self.get_sensor_avgs(mes, anio)
                data = {'sensor_humedad_suelo_1_avgs': sensor_avgs['sensor_humedad_suelo_1_avgs'],
                        'sensor_humedad_suelo_2_avgs': sensor_avgs['sensor_humedad_suelo_2_avgs'],
                        'sensor_humedad_suelo_3_avgs': sensor_avgs['sensor_humedad_suelo_3_avgs'],
                        'sensor_humedad_suelo_4_avgs': sensor_avgs['sensor_humedad_suelo_4_avgs'],
                        'sensor_humedad_ambiente_1_avgs': sensor_avgs['sensor_humedad_ambiente_1_avgs'],
                        'sensor_temperatura_ambiente_1_avgs': sensor_avgs['sensor_temperatura_ambiente_1_avgs'],
                        'mes': formateo_fecha}
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    #Promedio de los sensores por dia
    def get_sensor_avgs(self, mes, anio):
        sensor_humedad_suelo_1_avgs = []
        sensor_humedad_suelo_2_avgs = []
        sensor_humedad_suelo_3_avgs = []
        sensor_humedad_suelo_4_avgs = []
        sensor_humedad_ambiente_1_avgs = []
        sensor_temperatura_ambiente_1_avgs = []
        sensor_avgs = {}
        try:

            for d in range(1, 32):
                sensor_humedad_suelo_1_avg = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                                   fecha_registro__year=anio, codigo_sensor=1,
                                                                   tipo_sensor=1).aggregate(
                    r=Coalesce(Avg('value'), 0)).get(
                    'r')
                sensor_humedad_suelo_2_avg = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                                   fecha_registro__year=anio, codigo_sensor=2,
                                                                   tipo_sensor=1).aggregate(
                    r=Coalesce(Avg('value'), 0)).get(
                    'r')

                sensor_humedad_suelo_3_avg = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                                   fecha_registro__year=anio, codigo_sensor=3,
                                                                   tipo_sensor=1).aggregate(
                    r=Coalesce(Avg('value'), 0)).get(
                    'r')
                sensor_humedad_suelo_4_avg = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                                   fecha_registro__year=anio, codigo_sensor=4,
                                                                   tipo_sensor=1).aggregate(
                    r=Coalesce(Avg('value'), 0)).get(
                    'r')

                sensor_humedad_ambiente_1_avg = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                                      fecha_registro__year=anio, codigo_sensor=1,
                                                                      tipo_sensor=2).aggregate(
                    r=Coalesce(Avg('value'), 0)).get('r')

                sensor_temperatura_ambiente_1_avg = Sensor.objects.filter(fecha_registro__day=d,
                                                                          fecha_registro__month=mes,
                                                                          fecha_registro__year=anio, codigo_sensor=1,
                                                                          tipo_sensor=3).aggregate(
                    r=Coalesce(Avg('value'), 0)).get('r')

                sensor_humedad_suelo_1_avgs.append(float(sensor_humedad_suelo_1_avg))
                sensor_humedad_suelo_2_avgs.append(float(sensor_humedad_suelo_2_avg))
                sensor_humedad_suelo_3_avgs.append(float(sensor_humedad_suelo_3_avg))
                sensor_humedad_suelo_4_avgs.append(float(sensor_humedad_suelo_4_avg))
                sensor_humedad_ambiente_1_avgs.append(float(sensor_humedad_ambiente_1_avg))
                sensor_temperatura_ambiente_1_avgs.append(float(sensor_temperatura_ambiente_1_avg))

            sensor_avgs = {
                'sensor_humedad_suelo_1_avgs': sensor_humedad_suelo_1_avgs,
                'sensor_humedad_suelo_2_avgs': sensor_humedad_suelo_2_avgs,
                'sensor_humedad_suelo_3_avgs': sensor_humedad_suelo_3_avgs,
                'sensor_humedad_suelo_4_avgs': sensor_humedad_suelo_4_avgs,
                'sensor_humedad_ambiente_1_avgs': sensor_humedad_ambiente_1_avgs,
                'sensor_temperatura_ambiente_1_avgs': sensor_temperatura_ambiente_1_avgs
            }

        except:
            pass
        return sensor_avgs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sensor_avgs = self.get_sensor_avgs(mes=datetime.now().month, anio=datetime.now().year)
        context['title'] = 'Promedio de datos de los Sensores'
        context['entity'] = 'Sensor'
        context['create_url'] = reverse_lazy('gestion_riego:sensor_create')
        context['list_url'] = reverse_lazy('gestion_riego:sensor_list')
        # Tarda mucho en cargar por lo cual se ha comentado
        context['mes'] = datetime.now().strftime('%B')
        context['sensor_humedad_suelo_1_avgs'] = sensor_avgs['sensor_humedad_suelo_1_avgs']
        context['sensor_humedad_suelo_2_avgs'] = sensor_avgs['sensor_humedad_suelo_1_avgs']
        context['sensor_humedad_suelo_3_avgs'] = sensor_avgs['sensor_humedad_suelo_1_avgs']
        context['sensor_humedad_suelo_4_avgs'] = sensor_avgs['sensor_humedad_suelo_1_avgs']
        context['sensor_humedad_ambiente_1_avgs'] = sensor_avgs['sensor_humedad_ambiente_1_avgs']
        context['sensor_temperatura_ambiente_1_avgs'] = sensor_avgs['sensor_temperatura_ambiente_1_avgs']
        return context


# Para el apirest con django-rest
class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()


def lectura(request):
    sensor = Sensor.objects.first()
    print(sensor)
    contexto = {

    }
    return render(request, 'gestion_riego/sensor/dashboard.html', contexto)
