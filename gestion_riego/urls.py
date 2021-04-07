from django.urls import path
from rest_framework.routers import DefaultRouter

from gestion_riego.views.dashboard.dashboard_view import dashboard
from gestion_riego.views.device.device_views import DeviceCreateView, DeviceUpdateView, DeviceDeleteView, \
    DeviceListView, dashboardView, DeviceViewSet
from gestion_riego.views.historial_riego.historial_riego_view import HistorialRiegoListView, HistorialRiegoViewSet, UsoAguaPorTipoLogicaDifusa
from gestion_riego.views.login.views import LoginFormView, LogoutView
from gestion_riego.views.persona.persona_view import PersonaCreateView, PersonaUpdateView, PersonaDeleteView, \
    PersonaListView
from gestion_riego.views.planta.planta_view import PlantaCreateView, PlantaUpdateView, PlantaDeleteView, PlantaListView
from gestion_riego.views.plataforma.plataforma_view import PlataformaCreateView, PlataformaUpdateView, \
    PlataformaDeleteView, PlataformaListView, PlataformaViewSet
from gestion_riego.views.sensor.sensor_view import SensorCreateView, SensorUpdateView, SensorDeleteView, SensorListView, SensorViewSet
from gestion_riego.views.siembra.siembra_view import SiembraCreateView, SiembraUpdateView, SiembraDeleteView, \
    SiembraListView
from gestion_riego.views.tipo_sensor.tipo_sensor_view import TipoSensorCreateView, TipoSensorUpdateView, \
    TipoSensorDeleteView, TipoSensorListView
from gestion_riego.views.tipo_suelo.tipo_suelo_view import TipoSueloCreateView, TipoSueloUpdateView, \
    TipoSueloDeleteView, TipoSueloListView
from .view import fuzzy, plot, home

from django.conf import settings
from django.conf.urls.static import static

app_name = 'gestion_riego'

router = DefaultRouter()
router.register('srv/sensor', SensorViewSet)
router.register('srv/historial-riego', HistorialRiegoViewSet)
router.register('srv/plataforma', PlataformaViewSet)
router.register('srv/device', DeviceViewSet)

urlpatterns = router.urls

urlpatterns += [
    # Vistas basadas en clases, todo lo que hice en view.py, django ya lo hace automaticamente, cambian algunas reglas.
    #  class_view.py
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('personas/create', PersonaCreateView.as_view(), name='persona_create'),
    path('personas/update/<int:pk>/', PersonaUpdateView.as_view(), name='persona_update'),
    path('personas/delete/<int:pk>/', PersonaDeleteView.as_view(), name='persona_delete'),
    path('personas/', PersonaListView.as_view(), name='persona_list'),

    path('sensores/create', SensorCreateView.as_view(), name='sensor_create'),
    path('sensores/update/<int:pk>/', SensorUpdateView.as_view(), name='sensor_update'),
    path('sensores/delete/<int:pk>/', SensorDeleteView.as_view(), name='sensor_delete'),
    path('sensores/', SensorListView.as_view(), name='sensor_list'),

    path('plataformas/create/', PlataformaCreateView.as_view(), name='plataforma_create'),
    path('plataformas/update/<int:pk>/', PlataformaUpdateView.as_view(), name='plataforma_update'),
    path('plataformas/delete/<int:pk>/', PlataformaDeleteView.as_view(), name='plataforma_delete'),
    path('plataformas/', PlataformaListView.as_view(), name='plataforma_list'),

    path('tipo-sensores/create/', TipoSensorCreateView.as_view(), name='tipo_sensor_create'),
    path('tipo-sensores/update/<int:pk>/', TipoSensorUpdateView.as_view(), name='tipo_sensor_update'),
    path('tipo-sensores/delete/<int:pk>/', TipoSensorDeleteView.as_view(), name='tipo_sensor_delete'),
    path('tipo-sensores/', TipoSensorListView.as_view(), name='tipo_sensor_list'),

    path('tipo-suelos/create/', TipoSueloCreateView.as_view(), name='tipo_suelo_create'),
    path('tipo-suelos/update/<int:pk>/', TipoSueloUpdateView.as_view(), name='tipo_suelo_update'),
    path('tipo-suelos/delete/<int:pk>/', TipoSueloDeleteView.as_view(), name='tipo_suelo_delete'),
    path('tipo-suelos', TipoSueloListView.as_view(), name='tipo_suelo_list'),

    path('plantas/create/', PlantaCreateView.as_view(), name='planta_create'),
    path('plantas/update/<int:pk>/', PlantaUpdateView.as_view(), name='planta_update'),
    path('plantas/delete/<int:pk>/', PlantaDeleteView.as_view(), name='planta_delete'),
    path('plantas', PlantaListView.as_view(), name='planta_list'),

    path('siembras/create/', SiembraCreateView.as_view(), name='siembra_create'),
    path('siembras/update/<int:pk>/', SiembraUpdateView.as_view(), name='siembra_update'),
    path('siembras/delete/<int:pk>/', SiembraDeleteView.as_view(), name='siembra_delete'),
    path('siembras', SiembraListView.as_view(), name='siembra_list'),

    path('devices/create/', DeviceCreateView.as_view(), name='device_create'),
    path('devices/update/<int:pk>/', DeviceUpdateView.as_view(), name='device_update'),
    path('devices/delete/<int:pk>/', DeviceDeleteView.as_view(), name='device_delete'),
    path('devices/list/', DeviceListView.as_view(), name='device_list'),
    path('dashboard/', dashboardView.as_view(), name='dashboard'),

    path('historial_riego/', HistorialRiegoListView.as_view(), name='historial_riego'),
    path('uso_agua/', UsoAguaPorTipoLogicaDifusa.as_view(), name='uso_agua'),

    path('fuzzy/', home, name='fuzzy'),


]

