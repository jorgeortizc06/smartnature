from rest_framework import serializers
from gestion_riego.models import HistorialRiego


class HistorialRiegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialRiego
        fields = '__all__'  # Para especificar['marca', 'alcohol']
