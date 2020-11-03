from rest_framework import serializers
from gestion_riego.models import Sensor

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'  #Para especificar['marca', 'alcohol']