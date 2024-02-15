from account.filters import BaseFilter
from rest_framework import viewsets
from .models import *
from .serializers import *
from account.serializers import SchoolSerializer, TeacherSerializer, StudentSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = []

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = []

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = []

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.order_by('-id').all()
    serializer_class = ExamSerializer
    permission_classes = []

class ExamAnswerViewSet(viewsets.ModelViewSet):
    queryset = ExamAnswer.objects.all()
    serializer_class = ExamAnswerSerializer
    permission_classes = []