from django.contrib.auth.decorators import login_required
from django.db.models import Avg
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
        data_sensores_datatable = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # Obtengo datos del mes actual
                sensores = Sensor.objects.filter(fecha_registro__month=datetime.now().month,
                                                 fecha_registro__year=datetime.now().year)
                for i in sensores:
                    data.append(i.toJSON())
            elif action == 'search_historial_sensores_month':
                fecha_ajax = request.POST['fecha']

                fecha = datetime.strptime(fecha_ajax, '%Y-%m-%d')  # convierto a fecha para que python lo entienda
                formateo_fecha = datetime.strftime(fecha, '%B')  # ne sirve para visualizarlo en el chart
                dia = fecha.day
                mes = fecha.month
                anio = fecha.year
                data = []
                data_sensores = self.get_data_sensores(mes, anio)
                #sensores: Para mi datatable
                sensores_datatable = Sensor.objects.filter(fecha_registro__month=mes,
                                                 fecha_registro__year=anio)
                data_sensores_datatable = []
                for sensor in sensores_datatable:
                    data_sensores_datatable.append(sensor.toJSON())

                print(sensores_datatable)
                data = {'historial_sensor_humedad_suelo_month_1': data_sensores['data_humedad_1'],
                        'historial_sensor_humedad_suelo_month_2': data_sensores['data_humedad_2'],
                        'historial_sensor_humedad_suelo_month_3': data_sensores['data_humedad_3'],
                        'historial_sensor_humedad_suelo_month_4': data_sensores['data_humedad_4'],
                        'historial_sensor_humedad_ambiente_month_1': data_sensores['data_humedad_ambiente_1'],
                        'historial_sensor_temperatura_ambiente_month_1': data_sensores['data_temperatura_ambiente_1'],
                        'data_sensores_datatable': data_sensores_datatable,
                        'mes': formateo_fecha}
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # def get_queryset(self):
    #    return self.model.objects.all()[:10]  # Trae solo dos objetos

    def get_data_sensores(self, mes, anio):
        data_humedad_1 = []
        data_humedad_2 = []
        data_humedad_3 = []
        data_humedad_4 = []
        data_humedad_ambiente_1 = []
        data_temperatura_ambiente_1 = []
        data = {}
        try:

            for d in range(1, 32):
                avg_sensor_humedad_1 = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                             fecha_registro__year=anio, codigo_sensor=1,
                                                             tipo_sensor=1).aggregate(r=Coalesce(Avg('value'), 0)).get(
                    'r')
                avg_sensor_humedad_2 = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                             fecha_registro__year=anio, codigo_sensor=2,
                                                             tipo_sensor=1).aggregate(r=Coalesce(Avg('value'), 0)).get(
                    'r')

                avg_sensor_humedad_3 = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                             fecha_registro__year=anio, codigo_sensor=3,
                                                             tipo_sensor=1).aggregate(r=Coalesce(Avg('value'), 0)).get(
                    'r')
                avg_sensor_humedad_4 = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                             fecha_registro__year=anio, codigo_sensor=4,
                                                             tipo_sensor=1).aggregate(r=Coalesce(Avg('value'), 0)).get(
                    'r')

                avg_sensor_hum_ambiente = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                                fecha_registro__year=anio, codigo_sensor=1,
                                                                tipo_sensor=2).aggregate(
                    r=Coalesce(Avg('value'), 0)).get('r')

                avg_sensor_temp_ambiente = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                                 fecha_registro__year=anio, codigo_sensor=1,
                                                                 tipo_sensor=3).aggregate(
                    r=Coalesce(Avg('value'), 0)).get('r')

                data_humedad_1.append(float(avg_sensor_humedad_1))
                data_humedad_2.append(float(avg_sensor_humedad_2))
                data_humedad_3.append(float(avg_sensor_humedad_3))
                data_humedad_4.append(float(avg_sensor_humedad_4))
                data_humedad_ambiente_1.append(float(avg_sensor_hum_ambiente))
                data_temperatura_ambiente_1.append(float(avg_sensor_temp_ambiente))

            data = {'data_humedad_1': data_humedad_1,
                    'data_humedad_2': data_humedad_2,
                    'data_humedad_3': data_humedad_3,
                    'data_humedad_4': data_humedad_4,
                    'data_humedad_ambiente_1': data_humedad_ambiente_1,
                    'data_temperatura_ambiente_1': data_temperatura_ambiente_1}

        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_sensores = self.get_data_sensores(mes=datetime.now().month, anio=datetime.now().year)
        context['title'] = 'Lista de Sensores'
        context['entity'] = 'Sensor'
        context['create_url'] = reverse_lazy('gestion_riego:sensor_create')
        context['list_url'] = reverse_lazy('gestion_riego:sensor_list')
        # Tarda mucho en cargar por lo cual se ha comentado
        context['mes'] = datetime.now().strftime('%B')
        context['sensor_humedad_suelo_1'] = data_sensores['data_humedad_1']
        context['sensor_humedad_suelo_2'] = data_sensores['data_humedad_2']
        context['sensor_humedad_suelo_3'] = data_sensores['data_humedad_3']
        context['sensor_humedad_suelo_4'] = data_sensores['data_humedad_4']
        context['sensor_humedad_ambiente_1'] = data_sensores['data_humedad_ambiente_1']
        context['sensor_temperatura_ambiente_1'] = data_sensores['data_temperatura_ambiente_1']
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
