from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from account.filters import BaseFilter
from api.models import Student, StudentTopicProgress
from api.serializers import StudentTopicProgressSerializer
from utils.helpers import set_student_topic_progresses


class StudentTopicProgressViewSet(viewsets.ModelViewSet):
    queryset = StudentTopicProgress.objects.all()
    serializer_class = StudentTopicProgressSerializer
    permission_classes = []

    def get_queryset(self):
        params = self.request.query_params

        if 'student' in params:
            student_id = params.get('student')
            print(student_id)
            student = get_object_or_404(Student, pk=student_id)
            set_student_topic_progresses(student)

        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset