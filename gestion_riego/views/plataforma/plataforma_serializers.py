from rest_framework import serializers
from gestion_riego.models import Plataforma


class PlataformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plataforma
        fields = '__all__'  # Para especificar['marca', 'alcohol']
