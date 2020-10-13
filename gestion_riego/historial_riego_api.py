from rest_framework import viewsets
from .models import HistorialRiego
from .historial_riego_serializers import HistorialRiegoSerializer

class HistorialRiegoViewSet(viewsets.ModelViewSet):
    serializer_class = HistorialRiegoSerializer
    queryset = HistorialRiego.objects.all()