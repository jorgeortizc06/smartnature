from rest_framework import viewsets
from gestion_riego.models import Plataforma
from .plataforma_serializers import PlataformaSerializer


class PlataformaViewSet(viewsets.ModelViewSet):
    serializer_class = PlataformaSerializer
    queryset = Plataforma.objects.all()
