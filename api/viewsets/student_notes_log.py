from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from account.filters import BaseFilter
from api.models import StudentNotesLog
from api.serializers import StudentNotesLogSerializer
from utils.helpers import set_student_topic_progresses


class StudentNotesLogViewSet(viewsets.ModelViewSet):
    queryset = StudentNotesLog.objects.all()
    serializer_class = StudentNotesLogSerializer
    permission_classes = []

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset