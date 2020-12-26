from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
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


class SensorListView(ListView):
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
                for i in Sensor.objects.all()[0:300]:
                    data.append(i.toJSON())
            elif action == 'search_historial_sensores_month':
                fecha_ajax = request.POST['fecha']

                fecha = datetime.strptime(fecha_ajax, '%Y-%m-%d') #convierto a fecha para que python lo entienda
                formateo_fecha = datetime.strftime(fecha, '%B') #ne sirve para visualizarlo en el chart
                dia = fecha.day
                mes = fecha.month
                anio = fecha.year
                data = []
                data = {'historial_sensor_humedad_suelo_month_1': self.get_graph_sensor_humedad_suelo_month_1(mes, anio),
                        'historial_sensor_humedad_suelo_month_2': self.get_graph_sensor_humedad_suelo_month_2(mes, anio),
                        'historial_sensor_humedad_suelo_month_3': self.get_graph_sensor_humedad_suelo_month_3(mes, anio),
                        'historial_sensor_humedad_suelo_month_4': self.get_graph_sensor_humedad_suelo_month_4(mes, anio),
                        'historial_sensor_humedad_ambiente_month_1' : self.get_graph_sensor_humedad_ambiente_month_1(mes, anio),
                        'historial_sensor_temperatura_ambiente_month_1' : self.get_graph_sensor_temperatura_ambiente_month_1(mes, anio),
                        'mes':  formateo_fecha}
                print(data)

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    #def get_queryset(self):
    #    return self.model.objects.all()[:10]  # Trae solo dos objetos

    def get_graph_sensor_humedad_suelo_month_1(self, mes, anio):
        data = []
        try:

            for d in range(1, 31):
                avg_sensor_humedad = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                           fecha_registro__year=anio, codigo_sensor=1,
                                                           tipo_sensor=1).aggregate(r=Coalesce(Avg('value'), 0)).get(
                    'r')
                data.append(float(avg_sensor_humedad))
        except:
            pass
        return data

    def get_graph_sensor_humedad_suelo_month_2(self, mes, anio):
        data = []
        try:

            for d in range(1, 31):
                avg_sensor_humedad = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                           fecha_registro__year=anio, codigo_sensor=2,
                                                           tipo_sensor=1).aggregate(r=Coalesce(Avg('value'), 0)).get(
                    'r')
                data.append(float(avg_sensor_humedad))
        except:
            pass
        return data

    def get_graph_sensor_humedad_suelo_month_3(self, mes, anio):
        data = []
        try:

            for d in range(1, 31):
                avg_sensor_humedad = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                           fecha_registro__year=anio, codigo_sensor=3,
                                                           tipo_sensor=1).aggregate(r=Coalesce(Avg('value'), 0)).get(
                    'r')
                data.append(float(avg_sensor_humedad))
        except:
            pass
        return data

    def get_graph_sensor_humedad_suelo_month_4(self, mes, anio):
        data = []
        try:

            for d in range(1, 31):
                avg_sensor_humedad = Sensor.objects.filter(fecha_registro__day=d, fecha_registro__month=mes,
                                                           fecha_registro__year=anio, codigo_sensor=4,
                                                           tipo_sensor=1).aggregate(r=Coalesce(Avg('value'), 0)).get(
                    'r')
                data.append(float(avg_sensor_humedad))
        except:
            pass
        return data

    def get_graph_sensor_humedad_ambiente_month_1(self, mes, anio):
        data = []
        try:

            for d in range(1,31):
                avg_sensor_hum_ambiente = Sensor.objects.filter(fecha_registro__day = d, fecha_registro__month = mes, fecha_registro__year = anio, codigo_sensor = 1, tipo_sensor = 2).aggregate(r=Coalesce(Avg('value'), 0)).get('r')
                data.append(float(avg_sensor_hum_ambiente))
        except:
            pass
        return data

    def get_graph_sensor_temperatura_ambiente_month_1(self, mes, anio):
        data = []
        try:
            for d in range(1,31):
                avg_sensor_temp_ambiente = Sensor.objects.filter(fecha_registro__day = d, fecha_registro__month = mes, fecha_registro__year = anio, codigo_sensor = 1, tipo_sensor = 3).aggregate(r=Coalesce(Avg('value'), 0)).get('r')
                data.append(float(avg_sensor_temp_ambiente))
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Sensores'
        context['entity'] = 'Sensor'
        context['create_url'] = reverse_lazy('gestion_riego:sensor_create')
        context['list_url'] = reverse_lazy('gestion_riego:sensor_list')
        context['mes'] = datetime.now().strftime('%B')
        context['sensor_humedad_suelo_1'] = self.get_graph_sensor_humedad_suelo_month_1(mes = datetime.now().month, anio = datetime.now().year)
        context['sensor_humedad_suelo_2'] = self.get_graph_sensor_humedad_suelo_month_2(mes = datetime.now().month, anio = datetime.now().year)
        context['sensor_humedad_suelo_3'] = self.get_graph_sensor_humedad_suelo_month_3(mes = datetime.now().month, anio = datetime.now().year)
        context['sensor_humedad_suelo_4'] = self.get_graph_sensor_humedad_suelo_month_4(mes = datetime.now().month, anio = datetime.now().year)
        context['sensor_humedad_ambiente_1'] = self.get_graph_sensor_humedad_ambiente_month_1(mes = datetime.now().month, anio = datetime.now().year)
        context['sensor_temperatura_ambiente_1'] = self.get_graph_sensor_temperatura_ambiente_month_1(mes = datetime.now().month, anio = datetime.now().year)
        return context


#Para el apirest con django-rest
class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()


def lectura(request):
    sensor = Sensor.objects.first()
    print(sensor)
    contexto = {

    }
    return render(request, 'gestion_riego/sensor/dashboard.html', contexto)
