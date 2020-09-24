from django.contrib import admin
from django.urls import path
#from gestion_riego.views import list_persona, new_persona, edit_persona, delete_persona
from .persona_view import PersonaCreate, PersonaUpdate, PersonaDelete, PersonaList
from .sensor_view import SensorCreate, SensorUpdate, SensorDelete, SensorList, lectura
from .tipo_sensor_view import TipoSensorCreate, TipoSensorUpdate, TipoSensorDelete, TipoSensorList
from .tipo_suelo_view import TipoSueloCreate, TipoSueloUpdate, TipoSueloDelete, TipoSueloList
from .device_view import DeviceCreate, DeviceUpdate, DeviceDelete, DeviceList
from .planta_view import PlantaCreate, PlantaUpdate, PlantaDelete, PlantaList
from .plataforma_view import PlataformaCreate, PlataformaUpdate, PlataformaDelete, PlataformaList
from .sensor_api import SensorViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('srv/sensor/list', SensorViewSet)

urlpatterns = router.urls

urlpatterns += [
    #Vistas basadas en clases, todo lo que hice en view.py, django ya lo hace automaticamente, cambian algunas reglas. class_view.py
    path('persona_create/', PersonaCreate.as_view(), name='persona_create'),
    path('persona_update/<int:pk>/', PersonaUpdate.as_view(), name='persona_update'),
    path('persona_delete/<int:pk>/', PersonaDelete.as_view(), name='persona_delete'),
    path('persona_list/', PersonaList.as_view(), name='persona_list'),

    path('sensor_create/', SensorCreate.as_view(), name='sensor_create'),
    path('sensor_update/<int:pk>/', SensorUpdate.as_view(), name='sensor_update'),
    path('sensor_delete/<int:pk>/', SensorDelete.as_view(), name='sensor_delete'),
    path('sensor_list/', SensorList.as_view(), name='sensor_list'),
    path('dashboard/', lectura, name='dashboard'),

    path('plataforma_create/', PlataformaCreate.as_view(), name='plataforma_create'),
    path('plataforma_update/<int:pk>/', PlataformaUpdate.as_view(), name='plataforma_update'),
    path('plataforma_delete/<int:pk>/', PlataformaDelete.as_view(), name='plataforma_delete'),
    path('plataforma_list/', PlataformaList.as_view(), name='plataforma_list'),

    path('tipo_sensor_create/', TipoSensorCreate.as_view(), name='tipo_sensor_create'),
    path('tipo_sensor_update/<int:pk>/', TipoSensorUpdate.as_view(), name='tipo_sensor_update'),
    path('tipo_sensor_delete/<int:pk>/', TipoSensorDelete.as_view(), name='tipo_sensor_delete'),
    path('tipo_sensor_list/', TipoSensorList.as_view(), name='tipo_sensor_list'),

    path('tipo_suelo_create/', TipoSueloCreate.as_view(), name='tipo_suelo_create'),
    path('tipo_suelo_update/<int:pk>/', TipoSueloUpdate.as_view(), name='tipo_suelo_update'),
    path('tipo_suelo_delete/<int:pk>/', TipoSueloDelete.as_view(), name='tipo_suelo_delete'),
    path('tipo_suelo_list/', TipoSueloList.as_view(), name='tipo_suelo_list'),

    path('planta_create/', PlantaCreate.as_view(), name='planta_create'),
    path('planta_update/<int:pk>/', PlantaUpdate.as_view(), name='planta_update'),
    path('planta_delete/<int:pk>/', PlantaDelete.as_view(), name='planta_delete'),
    path('planta_list/', PlantaList.as_view(), name='planta_list'),

    path('device_create/', DeviceCreate.as_view(), name='device_create'),
    path('device_update/<int:pk>/', DeviceUpdate.as_view(), name='device_update'),
    path('device_delete/<int:pk>/', DeviceDelete.as_view(), name='device_delete'),
    path('device_list/', DeviceList.as_view(), name='device_list'),
]
