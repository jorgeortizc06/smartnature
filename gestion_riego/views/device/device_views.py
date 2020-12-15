from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, FormView
from django.http import JsonResponse
from gestion_riego.forms import DeviceForm, DashboardForm
from gestion_riego.models import Device, HistorialRiego
from datetime import datetime
import itertools
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


class DeviceListView(ListView):
    model = Device
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

class dashboardView(ListView):
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
            if action == 'search_historial_riego_day':
                dia = request.POST['id']
                data = []
                data = {'historial_riego_day_1': self.get_graph_day_1(dia),
                        'historial_riego_day_2': self.get_graph_day_2(dia),
                        'historial_riego_day_3': self.get_graph_day_3(dia),
                        'historial_riego_day_4': self.get_graph_day_4(dia),
                        'historial_riego_day_5': self.get_graph_day_5(dia)}
                #data = self.get_graph_day_1(dia)

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error']= str(e)
        return JsonResponse(data, safe=False)

    def get_graph_day_1(self, day):
        data = []
        try:

            for h in range(1,25):
                totalRiego = HistorialRiego.objects.filter(fecha_riego__day = day, fecha_riego__hour= h, codigo_sensor = 1).aggregate(r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                data.append(float(totalRiego))

        except:
            pass
        return data

    def get_graph_day_2(self, day):
        data = []
        try:

            for h in range(1,25):
                totalRiego = HistorialRiego.objects.filter(fecha_riego__day = day, fecha_riego__hour= h, codigo_sensor = 2).aggregate(r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                data.append(float(totalRiego))

        except:
            pass
        return data

    def get_graph_day_3(self, day):
        data = []
        try:
            for h in range(1,25):
                totalRiego = HistorialRiego.objects.filter(fecha_riego__day = day, fecha_riego__hour= h, codigo_sensor = 3).aggregate(r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                data.append(float(totalRiego))

        except:
            pass
        return data

    def get_graph_day_4(self, day):
        data = []
        try:
            for h in range(1,25):
                totalRiego = HistorialRiego.objects.filter(fecha_riego__day = day, fecha_riego__hour= h, codigo_sensor = 4).aggregate(r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                data.append(float(totalRiego))

        except:
            pass
        return data
    def get_graph_day_5(self, day):
        data = []
        try:
            for h in range(1,25):
                totalRiego = HistorialRiego.objects.filter(fecha_riego__day = day, fecha_riego__hour= h, codigo_sensor = 5).aggregate(r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                data.append(float(totalRiego))

        except:
            pass
        return data

    def get_graph_month_1(self):
        data = []
        try:
            month = datetime.now().month
            for d in range(1,31):
                totalRiego = HistorialRiego.objects.filter(fecha_riego__month = month, fecha_riego__day = d, codigo_sensor = 1).aggregate(r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                data.append(float(totalRiego))

        except:
            pass
        return data

    def get_graph_month_2(self):
        data = []
        try:
            month = datetime.now().month
            for d in range(1,31):
                totalRiego = HistorialRiego.objects.filter(fecha_riego__month = month, fecha_riego__day = d, codigo_sensor = 2).aggregate(r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                data.append(float(totalRiego))

        except:
            pass
        return data

    def get_graph_month_3(self):
        data = []
        try:
            month = datetime.now().month
            for d in range(1,31):
                totalRiego = HistorialRiego.objects.filter(fecha_riego__month = month, fecha_riego__day = d, codigo_sensor = 3).aggregate(r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                data.append(float(totalRiego))

        except:
            pass
        return data

    def get_graph_month_4(self):
        data = []
        try:
            month = datetime.now().month
            for d in range(1,31):
                totalRiego = HistorialRiego.objects.filter(fecha_riego__month = month, fecha_riego__day = d, codigo_sensor = 4).aggregate(r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                data.append(float(totalRiego))

        except:
            pass
        return data

    def get_graph_month_5(self):
        data = []
        try:
            month = datetime.now().month
            for d in range(1,31):
                totalRiego = HistorialRiego.objects.filter(fecha_riego__month = month, fecha_riego__day = d, codigo_sensor = 5).aggregate(r=Coalesce(Sum('tiempo_riego'), 0)).get('r')
                data.append(float(totalRiego))
        except:
            pass
        return data
    # Metodo para modificar el context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['entity'] = 'Device'
        context['object_list'] = Device.objects.all()
        context['form'] = DashboardForm()
        context['mes'] = datetime.now().strftime('%B')
        context['dia'] = datetime.now().strftime('%D')
        context['historial_riego_day_1'] = self.get_graph_day_1(day = datetime.now().day)
        context['historial_riego_day_2'] = self.get_graph_day_2(day = datetime.now().day)
        context['historial_riego_day_3'] = self.get_graph_day_3(day = datetime.now().day)
        context['historial_riego_day_4'] = self.get_graph_day_4(day = datetime.now().day)
        context['historial_riego_day_5'] = self.get_graph_day_5(day = datetime.now().day)
        context['historial_riego_1'] = self.get_graph_month_1()
        context['historial_riego_2'] = self.get_graph_month_2()
        context['historial_riego_3'] = self.get_graph_month_3()
        context['historial_riego_4'] = self.get_graph_month_4()
        context['historial_riego_5'] = self.get_graph_month_5()
        return context


class DeviceFormView(FormView):
    form_class = DeviceForm
    template_name = 'gestion_riego/device/device_create.html'
    success_url = reverse_lazy('erp:device_list')