from rest_framework import viewsets
from api.models import StudentAnswer, StudentTopicProgress
from rest_framework import viewsets
from rest_framework.decorators import action
from api.models import  Topic
from api.serializers import StudentAnswerSerializer, StudentTopicProgressSerializer, TeacherSchoolSerializer, TopicSerializer
from rest_framework.response import Response
from rest_framework import status
from ..models import Choice, TeacherSchool, Test
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


class TeacherSchoolViewSet(viewsets.ModelViewSet):
    queryset = TeacherSchool.objects.all()
    serializer_class = TeacherSchoolSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['accepted', 'school', 'teacher']