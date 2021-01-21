from django.urls import path
from rest_framework.routers import DefaultRouter

from gestion_riego.views.dashboard.dashboard_view import dashboard
from gestion_riego.views.device.device_views import DeviceCreateView, DeviceUpdateView, DeviceDeleteView, \
    DeviceListView, dashboardView, DeviceViewSet
from gestion_riego.views.historial_riego.historial_riego_view import HistorialRiegoListView, HistorialRiegoViewSet
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
router.register('srv/historial_riego', HistorialRiegoViewSet)
router.register('srv/plataforma', PlataformaViewSet)
router.register('srv/device', DeviceViewSet)

urlpatterns = router.urls

urlpatterns += [
    # Vistas basadas en clases, todo lo que hice en view.py, django ya lo hace automaticamente, cambian algunas reglas.
    #  class_view.py
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('persona_create/', PersonaCreateView.as_view(), name='persona_create'),
    path('persona_update/<int:pk>/', PersonaUpdateView.as_view(), name='persona_update'),
    path('persona_delete/<int:pk>/', PersonaDeleteView.as_view(), name='persona_delete'),
    path('persona_list/', PersonaListView.as_view(), name='persona_list'),

    path('sensor_create/', SensorCreateView.as_view(), name='sensor_create'),
    path('sensor_update/<int:pk>/', SensorUpdateView.as_view(), name='sensor_update'),
    path('sensor_delete/<int:pk>/', SensorDeleteView.as_view(), name='sensor_delete'),
    path('sensor_list/', SensorListView.as_view(), name='sensor_list'),

    path('plataforma_create/', PlataformaCreateView.as_view(), name='plataforma_create'),
    path('plataforma_update/<int:pk>/', PlataformaUpdateView.as_view(), name='plataforma_update'),
    path('plataforma_delete/<int:pk>/', PlataformaDeleteView.as_view(), name='plataforma_delete'),
    path('plataforma_list/', PlataformaListView.as_view(), name='plataforma_list'),

    path('tipo_sensor_create/', TipoSensorCreateView.as_view(), name='tipo_sensor_create'),
    path('tipo_sensor_update/<int:pk>/', TipoSensorUpdateView.as_view(), name='tipo_sensor_update'),
    path('tipo_sensor_delete/<int:pk>/', TipoSensorDeleteView.as_view(), name='tipo_sensor_delete'),
    path('tipo_sensor_list/', TipoSensorListView.as_view(), name='tipo_sensor_list'),

    path('tipo_suelo_create/', TipoSueloCreateView.as_view(), name='tipo_suelo_create'),
    path('tipo_suelo_update/<int:pk>/', TipoSueloUpdateView.as_view(), name='tipo_suelo_update'),
    path('tipo_suelo_delete/<int:pk>/', TipoSueloDeleteView.as_view(), name='tipo_suelo_delete'),
    path('tipo_suelo_list/', TipoSueloListView.as_view(), name='tipo_suelo_list'),

    path('planta_create/', PlantaCreateView.as_view(), name='planta_create'),
    path('planta_update/<int:pk>/', PlantaUpdateView.as_view(), name='planta_update'),
    path('planta_delete/<int:pk>/', PlantaDeleteView.as_view(), name='planta_delete'),
    path('planta_list/', PlantaListView.as_view(), name='planta_list'),

    path('siembra_create/', SiembraCreateView.as_view(), name='siembra_create'),
    path('siembra_update/<int:pk>/', SiembraUpdateView.as_view(), name='siembra_update'),
    path('siembra_delete/<int:pk>/', SiembraDeleteView.as_view(), name='siembra_delete'),
    path('siembra_list/', SiembraListView.as_view(), name='siembra_list'),

    path('device_create/', DeviceCreateView.as_view(), name='device_create'),
    path('device_update/<int:pk>/', DeviceUpdateView.as_view(), name='device_update'),
    path('device_delete/<int:pk>/', DeviceDeleteView.as_view(), name='device_delete'),
    path('device_list/', DeviceListView.as_view(), name='device_list'),
    path('dashboard/', dashboardView.as_view(), name='dashboard'),

    path('historial_riego/', HistorialRiegoListView.as_view(), name='historial_riego'),

    path('fuzzy/', home, name='fuzzy'),


]

