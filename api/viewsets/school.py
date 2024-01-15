from rest_framework import viewsets
from account.serializers import SchoolSerializer
from api.models import School

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = []