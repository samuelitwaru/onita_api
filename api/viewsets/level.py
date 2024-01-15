from rest_framework import viewsets
from api.models import Level
from api.serializers import LevelSerializer



class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = []