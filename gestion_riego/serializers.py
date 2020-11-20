from rest_framework import serializers

from gestion_riego.models import Sensor, Plataforma, HistorialRiego

class PlataformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plataforma
        fields = '__all__'  # Para especificar['marca', 'alcohol']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'  # Para especificar['marca', 'alcohol']

class HistorialRiegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialRiego
        fields = '__all__'  # Para especificar['marca', 'alcohol']