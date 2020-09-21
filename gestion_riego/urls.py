from django.contrib import admin
from django.urls import path
#from gestion_riego.views import list_persona, new_persona, edit_persona, delete_persona
from .persona_view import PersonaCreate, PersonaUpdate, PersonaDelete, PersonaList
from .sensor_view import SensorCreate, SensorUpdate, SensorDelete, SensorList, lectura
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
]
