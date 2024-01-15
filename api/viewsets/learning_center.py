from rest_framework import viewsets
from api.models import LearningCenter
from api.serializers import LearningCenterSerializer


class LearningCenterViewSet(viewsets.ModelViewSet):
    queryset = LearningCenter.objects.all()
    serializer_class = LearningCenterSerializer
    permission_classes = []