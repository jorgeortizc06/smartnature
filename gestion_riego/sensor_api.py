from rest_framework import viewsets
from .models import Sensor
from .sensor_serializers import SensorSerializer

class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()