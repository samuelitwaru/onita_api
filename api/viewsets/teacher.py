from rest_framework import viewsets
from account.serializers import TeacherSerializer
from api.models import Teacher

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = []