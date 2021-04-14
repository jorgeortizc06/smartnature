from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, FormView, TemplateView
from django.http import JsonResponse
from rest_framework import viewsets

from gestion_riego.forms import DeviceForm, DashboardForm
from gestion_riego.models import Device, HistorialRiego
from datetime import datetime
import itertools
# Vistas basadas en clases
# Recomendable y haca a la aplicacion facilmente escalable
from gestion_riego.serializers import DeviceSerializer


class DeviceCreateView(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'gestion_riego/device/device_create.html'
    success_url = reverse_lazy('gestion_riego:device_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save() #el metodo sobrescrito en forms:DeviceForm.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo dispositivo'
        context['entity'] = 'Device'
        context['list_url'] = reverse_lazy('gestion_riego:device_list')
        context['action'] = 'add'
        # context['object_list'] = Device.objects.all()
        return context

class DeviceUpdateView(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'gestion_riego/device/device_create.html'
    success_url = reverse_lazy('gestion_riego:device_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object() #hago referencia al objeto que recupero para actualizar
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
        self.object = self.get_object() #cuando inicie el objeto recupero la instancia
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
        context['title'] = 'Eliminación de un Dispositivo'
        context['entity'] = 'Device'
        context['list_url'] = reverse_lazy('gestion_riego:device_list')
        return context


class DeviceListView(TemplateView):
    template_name = 'gestion_riego/device/device_list.html'

    ####Sobreescribir metodos####
    # Metodos para devolver algo especifico
    def get_queryset(self):
        return Device.objects.all()

    @method_decorator(csrf_exempt)  # Al hacer post, va a salir forbideen 404, desabilito aunque no es recomendable
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #Listar con ajax
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Device.objects.all():
                    data.append(i.toJSON())
            elif action == 'add': #Esta seccion es para trabajar con los modals
                cli = Device()
                cli.nombre = request.POST['nombre']
                cli.descripcion = request.POST['descripcion']
                cli.ip = request.POST['ip']
                cli.topic = request.POST['topic']
                cli.puerto = request.POST['puerto']
                cli.save()
            elif action == 'edit': #Esta seccion es para trabajar con los modals
                cli = Device.objects.get(pk=request.POST['id'])
                cli.nombre = request.POST['nombre']
                cli.descripcion = request.POST['descripcion']
                cli.ip = request.POST['ip']
                cli.topic = request.POST['topic']
                cli.puerto = request.POST['puerto']
                cli.save()
            elif action == 'delete': #Esta seccion es para trabajar con los modals
                cli = Device.objects.get(pk=request.POST['id'])
                cli.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) #como uso coleccion de satos agrego safe=False

    # Metodo para modificar el context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de dispositivos'
        context['entity'] = 'Device'
        context['create_url'] = reverse_lazy('gestion_riego:device_create')
        context['list_url'] = reverse_lazy('gestion_riego:device_list')
        context['form'] = DeviceForm() #Para trabajar con los modals.
        # context['object_list'] = Device.objects.all()
        return context

class DashboardView(TemplateView):
    model = Device
    template_name = 'gestion_riego/dashboard/dashboard.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # el ajax envia el parametro de search_historial_riego_day para la etiqueta input dateDia
            if action == 'search_historial_riego_day':
                fecha_ajax = request.POST['fecha']
                fecha = datetime.strptime(fecha_ajax, '%Y-%m-%d') #convierto a fecha para que python lo entienda
                formateo_fecha = datetime.strftime(fecha, '%d-%m-%Y')
                dia = fecha.day
                mes = fecha.month
                anio = fecha.year
                data_historial_riego_day = self.get_graph_historial_riego_day(dia, mes, anio)
                data = []
                data = {'historial_riego_day_1': data_historial_riego_day['data_historial_riego_sensor_1'],
                        'historial_riego_day_2': data_historial_riego_day['data_historial_riego_sensor_2'],
                        'historial_riego_day_3': data_historial_riego_day['data_historial_riego_sensor_3'],
                        'historial_riego_day_4': data_historial_riego_day['data_historial_riego_sensor_4'],
                        'historial_riego_day_5': data_historial_riego_day['data_historial_riego_sensor_5'],
                        'dia_riego':  formateo_fecha}
            #el ajax envia el parametro de search_historial_riego_mont para la etiqueta input dateMes
            elif action == 'search_historial_riego_month':
                fecha_ajax = request.POST['fecha']
                fecha = datetime.strptime(fecha_ajax, '%Y-%m-%d') #convierto a fecha para que python lo entienda
                formateo_fecha = datetime.strftime(fecha, '%B') #ne sirve para visualizarlo en el chart
                dia = fecha.day
                mes = fecha.month
                anio = fecha.year
                v3_data_historial_riego_month = self.get_graph_v3_historial_riego_month(mes, anio)
                v1_data_historial_riego_month = self.get_graph_v1_historial_riego_month(mes, anio)
                v4_data_historial_riego_month = self.get_graph_v4_historial_riego_month(mes, anio)
                data = []
                data = {'historial_riego_month_1': v3_data_historial_riego_month['data_historial_riego_sensor_1'],
                        'historial_riego_month_2': v3_data_historial_riego_month['data_historial_riego_sensor_2'],
                        'historial_riego_month_3': v3_data_historial_riego_month['data_historial_riego_sensor_3'],
                        'historial_riego_month_4': v3_data_historial_riego_month['data_historial_riego_sensor_4'],
                        'historial_riego_month_5': v3_data_historial_riego_month['data_historial_riego_sensor_5'],

                        'v1_historial_riego_month_1': v1_data_historial_riego_month['data_historial_riego_sensor_1'],
                        'v1_historial_riego_month_2': v1_data_historial_riego_month['data_historial_riego_sensor_2'],
                        'v1_historial_riego_month_3': v1_data_historial_riego_month['data_historial_riego_sensor_3'],
                        'v1_historial_riego_month_4': v1_data_historial_riego_month['data_historial_riego_sensor_4'],
                        'v1_historial_riego_month_5': v1_data_historial_riego_month['data_historial_riego_sensor_5'],

                        'v4_historial_riego_month_1': v4_data_historial_riego_month['data_historial_riego_sensor_1'],
                        'v4_historial_riego_month_2': v4_data_historial_riego_month['data_historial_riego_sensor_2'],
                        'v4_historial_riego_month_3': v4_data_historial_riego_month['data_historial_riego_sensor_3'],
                        'v4_historial_riego_month_4': v4_data_historial_riego_month['data_historial_riego_sensor_4'],
                        'v4_historial_riego_month_5': v4_data_historial_riego_month['data_historial_riego_sensor_5'],

                        'dia_riego':  formateo_fecha}

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error']= str(e)
        return JsonResponse(data, safe=False)
    #==========Funciones para obtener historial de riego de un dia determinado para desglosarlo en 24 horas=============
    def get_graph_historial_riego_day(self, day, mes, anio):
        data_historial_riego_sensor_1 = []
        data_historial_riego_sensor_2 = []
        data_historial_riego_sensor_3 = []
        data_historial_riego_sensor_4 = []
        data_historial_riego_sensor_5 = []
        data = {}
        try:
            for h in range(1,25):
                sum_riego_sensor_1 = HistorialRiego.objects.filter(fecha_riego__day=day, fecha_riego__month=mes,
                                                                   fecha_riego__year=anio, fecha_riego__hour=h,
                                                                   codigo_sensor=1).aggregate(
                    r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                sum_riego_sensor_2 = HistorialRiego.objects.filter(fecha_riego__day=day, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, fecha_riego__hour=h,
                                                           codigo_sensor=2).aggregate(
                    r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                sum_riego_sensor_3 = HistorialRiego.objects.filter(fecha_riego__day=day, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, fecha_riego__hour=h,
                                                           codigo_sensor=3).aggregate(
                    r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                sum_riego_sensor_4 = HistorialRiego.objects.filter(fecha_riego__day=day, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, fecha_riego__hour=h,
                                                           codigo_sensor=4).aggregate(
                    r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                sum_riego_sensor_5 = HistorialRiego.objects.filter(fecha_riego__day=day, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, fecha_riego__hour=h,
                                                           codigo_sensor=5).aggregate(
                    r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                data_historial_riego_sensor_1.append(float(sum_riego_sensor_1))
                data_historial_riego_sensor_2.append(float(sum_riego_sensor_2))
                data_historial_riego_sensor_3.append(float(sum_riego_sensor_3))
                data_historial_riego_sensor_4.append(float(sum_riego_sensor_4))
                data_historial_riego_sensor_5.append(float(sum_riego_sensor_5))
            data = {
                'data_historial_riego_sensor_1': data_historial_riego_sensor_1,
                'data_historial_riego_sensor_2': data_historial_riego_sensor_2,
                'data_historial_riego_sensor_3': data_historial_riego_sensor_3,
                'data_historial_riego_sensor_4': data_historial_riego_sensor_4,
                'data_historial_riego_sensor_5': data_historial_riego_sensor_5,
            }
        except:
            pass
        return data

    # ==========Funciones para obtener historial de riego de un mes determinado para desglosarlo en días por cada tipo de logica difusa=============
    def get_graph_v3_historial_riego_month(self, mes, anio):
        data_historial_riego_sensor_1 = []
        data_historial_riego_sensor_2 = []
        data_historial_riego_sensor_3 = []
        data_historial_riego_sensor_4 = []
        data_historial_riego_sensor_5 = []
        data = {}
        try:
            for d in range(1,32):
                sum_riego_sensor_1 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                                   fecha_riego__year=anio, codigo_sensor=1).aggregate(
                    r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                sum_riego_sensor_2 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, codigo_sensor=2).aggregate(
                    r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                sum_riego_sensor_3 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, codigo_sensor=3).aggregate(
                    r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                sum_riego_sensor_4 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, codigo_sensor=4).aggregate(
                    r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                sum_riego_sensor_5 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                          fecha_riego__year=anio, codigo_sensor=5).aggregate(
                    r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                data_historial_riego_sensor_1.append(float(sum_riego_sensor_1))
                data_historial_riego_sensor_2.append(float(sum_riego_sensor_2))
                data_historial_riego_sensor_3.append(float(sum_riego_sensor_3))
                data_historial_riego_sensor_4.append(float(sum_riego_sensor_4))
                data_historial_riego_sensor_5.append(float(sum_riego_sensor_5))
            data = {
                'data_historial_riego_sensor_1': data_historial_riego_sensor_1,
                'data_historial_riego_sensor_2': data_historial_riego_sensor_2,
                'data_historial_riego_sensor_3': data_historial_riego_sensor_3,
                'data_historial_riego_sensor_4': data_historial_riego_sensor_4,
                'data_historial_riego_sensor_5': data_historial_riego_sensor_5,
            }
        except:
            pass
        return data

    def get_graph_v1_historial_riego_month(self, mes, anio):
        data_historial_riego_sensor_1 = []
        data_historial_riego_sensor_2 = []
        data_historial_riego_sensor_3 = []
        data_historial_riego_sensor_4 = []
        data_historial_riego_sensor_5 = []
        data = {}
        try:
            for d in range(1,32):
                sum_riego_sensor_1 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                                   fecha_riego__year=anio, codigo_sensor=1).aggregate(
                    r=Coalesce(Sum('tiempo_riego_1_variable'), 0)).get('r')
                sum_riego_sensor_2 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, codigo_sensor=2).aggregate(
                    r=Coalesce(Sum('tiempo_riego_1_variable'), 0)).get('r')
                sum_riego_sensor_3 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, codigo_sensor=3).aggregate(
                    r=Coalesce(Sum('tiempo_riego_1_variable'), 0)).get('r')
                sum_riego_sensor_4 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, codigo_sensor=4).aggregate(
                    r=Coalesce(Sum('tiempo_riego_1_variable'), 0)).get('r')
                sum_riego_sensor_5 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                          fecha_riego__year=anio, codigo_sensor=5).aggregate(
                    r=Coalesce(Sum('tiempo_riego_1_variable'), 0)).get('r')
                data_historial_riego_sensor_1.append(float(sum_riego_sensor_1))
                data_historial_riego_sensor_2.append(float(sum_riego_sensor_2))
                data_historial_riego_sensor_3.append(float(sum_riego_sensor_3))
                data_historial_riego_sensor_4.append(float(sum_riego_sensor_4))
                data_historial_riego_sensor_5.append(float(sum_riego_sensor_5))
            data = {
                'data_historial_riego_sensor_1': data_historial_riego_sensor_1,
                'data_historial_riego_sensor_2': data_historial_riego_sensor_2,
                'data_historial_riego_sensor_3': data_historial_riego_sensor_3,
                'data_historial_riego_sensor_4': data_historial_riego_sensor_4,
                'data_historial_riego_sensor_5': data_historial_riego_sensor_5,
            }
        except:
            pass
        return data

    def get_graph_v4_historial_riego_month(self, mes, anio):
        data_historial_riego_sensor_1 = []
        data_historial_riego_sensor_2 = []
        data_historial_riego_sensor_3 = []
        data_historial_riego_sensor_4 = []
        data_historial_riego_sensor_5 = []
        data = {}
        try:
            for d in range(1,32):
                sum_riego_sensor_1 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                                   fecha_riego__year=anio, codigo_sensor=1).aggregate(
                    r=Coalesce(Sum('tiempo_riego_4_variable'), 0)).get('r')
                sum_riego_sensor_2 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, codigo_sensor=2).aggregate(
                    r=Coalesce(Sum('tiempo_riego_4_variable'), 0)).get('r')
                sum_riego_sensor_3 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, codigo_sensor=3).aggregate(
                    r=Coalesce(Sum('tiempo_riego_4_variable'), 0)).get('r')
                sum_riego_sensor_4 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                           fecha_riego__year=anio, codigo_sensor=4).aggregate(
                    r=Coalesce(Sum('tiempo_riego_4_variable'), 0)).get('r')
                sum_riego_sensor_5 = HistorialRiego.objects.filter(fecha_riego__day=d, fecha_riego__month=mes,
                                                          fecha_riego__year=anio, codigo_sensor=5).aggregate(
                    r=Coalesce(Sum('tiempo_riego_4_variable'), 0)).get('r')
                data_historial_riego_sensor_1.append(float(sum_riego_sensor_1))
                data_historial_riego_sensor_2.append(float(sum_riego_sensor_2))
                data_historial_riego_sensor_3.append(float(sum_riego_sensor_3))
                data_historial_riego_sensor_4.append(float(sum_riego_sensor_4))
                data_historial_riego_sensor_5.append(float(sum_riego_sensor_5))
            data = {
                'data_historial_riego_sensor_1': data_historial_riego_sensor_1,
                'data_historial_riego_sensor_2': data_historial_riego_sensor_2,
                'data_historial_riego_sensor_3': data_historial_riego_sensor_3,
                'data_historial_riego_sensor_4': data_historial_riego_sensor_4,
                'data_historial_riego_sensor_5': data_historial_riego_sensor_5,
            }
        except:
            pass
        return data
    # Metodo para modificar el context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_historial_riego_month = self.get_graph_v3_historial_riego_month(mes = datetime.now().month, anio = datetime.now().year)
        data_historial_riego_day = self.get_graph_historial_riego_day(day = datetime.now().day, mes = datetime.now().month, anio = datetime.now().year)
        context['title'] = 'Dashboard'
        context['entity'] = 'Device'
        context['object_list'] = Device.objects.all()
        context['form'] = DashboardForm()
        context['mes'] = datetime.now().strftime('%B')
        context['dia'] = datetime.now().strftime('%D')
        context['historial_riego_day_1'] = data_historial_riego_day['data_historial_riego_sensor_1']
        context['historial_riego_day_2'] = data_historial_riego_day['data_historial_riego_sensor_2']
        context['historial_riego_day_3'] = data_historial_riego_day['data_historial_riego_sensor_3']
        context['historial_riego_day_4'] = data_historial_riego_day['data_historial_riego_sensor_4']
        context['historial_riego_day_5'] = data_historial_riego_day['data_historial_riego_sensor_5']
        context['historial_riego_1'] = data_historial_riego_month['data_historial_riego_sensor_1']
        context['historial_riego_2'] = data_historial_riego_month['data_historial_riego_sensor_2']
        context['historial_riego_3'] = data_historial_riego_month['data_historial_riego_sensor_3']
        context['historial_riego_4'] = data_historial_riego_month['data_historial_riego_sensor_4']
        context['historial_riego_5'] = data_historial_riego_month['data_historial_riego_sensor_5']
        #Tipo de logica difusa de 1 variable
        data_historial_riego_month_1_variable = self.get_graph_v1_historial_riego_month(
            mes=datetime.now().month,
            anio=datetime.now().year)
        context['v1_historial_riego_1'] = data_historial_riego_month_1_variable['data_historial_riego_sensor_1']
        context['v1_historial_riego_2'] = data_historial_riego_month_1_variable['data_historial_riego_sensor_2']
        context['v1_historial_riego_3'] = data_historial_riego_month_1_variable['data_historial_riego_sensor_3']
        context['v1_historial_riego_4'] = data_historial_riego_month_1_variable['data_historial_riego_sensor_4']
        context['v1_historial_riego_5'] = data_historial_riego_month_1_variable['data_historial_riego_sensor_5']
        #Tipo de logica difusa de 4 variables
        data_historial_riego_month_4_variable = self.get_graph_v4_historial_riego_month(
            mes=datetime.now().month,
            anio=datetime.now().year)
        context['v4_historial_riego_1'] = data_historial_riego_month_4_variable['data_historial_riego_sensor_1']
        context['v4_historial_riego_2'] = data_historial_riego_month_4_variable['data_historial_riego_sensor_2']
        context['v4_historial_riego_3'] = data_historial_riego_month_4_variable['data_historial_riego_sensor_3']
        context['v4_historial_riego_4'] = data_historial_riego_month_4_variable['data_historial_riego_sensor_4']
        context['v4_historial_riego_5'] = data_historial_riego_month_4_variable['data_historial_riego_sensor_5']
        return context


class DeviceFormView(FormView):
    form_class = DeviceForm
    template_name = 'gestion_riego/device/device_create.html'
    success_url = reverse_lazy('erp:device_list')

class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()