from rest_framework import viewsets
from api.models import Subject
from api.serializers import SubjectSerializer
from account.filters import BaseFilter


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = []
    
    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset