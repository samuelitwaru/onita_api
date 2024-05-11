from account.filters import BaseFilter
from rest_framework import viewsets
from ..models import *
from ..serializers import *
from ..serializers import SchoolSerializer, TeacherSerializer, StudentSerializer
from django_filters.rest_framework import DjangoFilterBackend


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = []

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = []

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = []

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.order_by('-id').all()
    serializer_class = ExamSerializer
    permission_classes = []

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset

class ExamAnswerViewSet(viewsets.ModelViewSet):
    queryset = ExamAnswer.objects.all()
    serializer_class = ExamAnswerSerializer
    permission_classes = []


class TopicQuestionViewSet(viewsets.ModelViewSet):
    queryset = TopicQuestion.objects.all()
    serializer_class = TopicQuestionSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['topic']

class TopicQuestionStudentAnswerViewSet(viewsets.ModelViewSet):
    queryset = TopicQuestionStudentAnswer.objects.all()
    serializer_class = TopicQuestionStudentAnswerSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['topic_question', 'student', 'topic_question__topic']

class TopicQuestionChoiceViewSet(viewsets.ModelViewSet):
    queryset = TopicQuestionChoice.objects.all()
    serializer_class = TopicQuestionChoiceSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['topic_question']