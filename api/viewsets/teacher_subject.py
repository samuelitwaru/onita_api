from rest_framework import viewsets
from api.models import StudentAnswer, StudentTopicProgress
from rest_framework import viewsets
from rest_framework.decorators import action
from api.models import  Topic
from api.serializers import TeacherSubjectSerializer
from rest_framework.response import Response
from rest_framework import status
from ..models import Choice, TeacherSubject, Test
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


class TeacherSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject', 'teacher']