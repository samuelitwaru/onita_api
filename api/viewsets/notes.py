# notes/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Notes
from ..serializers import NotesSerializer
from django_filters.rest_framework import DjangoFilterBackend


class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['teacher_subject', 'teacher_subject__teacher']