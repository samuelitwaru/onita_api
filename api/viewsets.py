from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import action
from rest_framework.response import Response
from django.urls import reverse
from rest_framework import viewsets
from account.filters import BaseFilter
from api.models import StudentNotesLog
from api.serializers import StudentNotesLogSerializer
from utils.helpers import set_student_topic_progresses
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.authtoken.models import Token
from utils.templating import render_template
from api.models import *
from api.serializers import *


class LearningCenterViewSet(viewsets.ModelViewSet):
    queryset = LearningCenter.objects.all()
    serializer_class = LearningCenterSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['learning_center']

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    @action(detail=True, methods=['GET'], name='redoreder_subtopics', url_path=r'redoreder-subtopics')
    def redoreder_subtopics(self, request, pk, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=pk)
        subtopics = topic.subtopic_set.order_by('order')
        order = 1
        for topic in subtopics:
            topic.order = order
            topic.save()
            order += 1 
        data = TopicSerializer(topic).data
        return self.retrieve(request, pk=pk)
    
    @action(detail=True, methods=['GET'], name='get_next', url_path=r'get-next')
    def get_next(self, request, pk, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=pk)
        print(topic.order+1)
        next_topic = get_object_or_404(Topic, notes=topic.notes, order=topic.order+1)
        data = TopicSerializer(next_topic).data
        return Response(data, status=200)
    
    @action(detail=True, methods=['GET'], name='get_prev', url_path=r'get-prev')
    def get_prev(self, request, pk, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=pk)
        prev_topic = get_object_or_404(Topic, notes=topic.notes, order=topic.order+1)
        data = TopicSerializer(prev_topic).data
        return Response(data, status=200)

    @action(detail=True, methods=['GET'], name='set_topic_order_up', url_path=r'set-topic-order-up')
    def set_topic_order_up(self, request, pk, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=pk)
        prev_topic = Topic.objects.filter(subject=topic.subject, order=topic.order-1).first()
        if prev_topic:
            topic.order = 999
            topic.save()
            prev_topic.order = prev_topic.order + 1
            prev_topic.save()
            topic.order = prev_topic.order - 1
            topic.save()
            topics = Topic.objects.filter(subject=topic.subject).all()
            template = render_template('ajax/topic/topic_list.html', {'topics':topics})
            return Response({'template': template}, status=status.HTTP_200_OK)
        return Response({'message': 'Cannot cannot find previous topic'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], name='set_topic_order_down', url_path=r'set-topic-order-down')
    def set_topic_order_down(self, request, pk, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=pk)
        next_topic = Topic.objects.filter(subject=topic.subject, order=topic.order+1).first()
        if next_topic:
            topic.order = 999
            topic.save()
            next_topic.order = next_topic.order - 1
            next_topic.save()
            topic.order = next_topic.order + 1
            topic.save()
            topics = Topic.objects.filter(subject=topic.subject).all()
            template = render_template('ajax/topic/topic_list.html', {'topics':topics})
            return Response({'template': template}, status=status.HTTP_200_OK)
        return Response({'message': 'Cannot find next topic'}, status=status.HTTP_400_BAD_REQUEST)
        
class SubtopicViewSet(viewsets.ModelViewSet):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset
    
    @action(detail=True, methods=['GET'], name='get_next', url_path=r'get-next')
    def get_next(self, request, pk, *args, **kwargs):
        subtopic = get_object_or_404(Subtopic, pk=pk)
        next_subtopic = get_object_or_404(Subtopic, topic=subtopic.topic, order=subtopic.order+1)
        return self.retrieve(request, pk=next_subtopic.id)

    @action(detail=True, methods=['GET'], name='get_prev', url_path=r'get-prev')
    def get_prev(self, request, pk, *args, **kwargs):
        subtopic = get_object_or_404(Subtopic, pk=pk)
        prev_subtopic = get_object_or_404(Subtopic, topic=subtopic.topic, order=subtopic.order+1)
        return self.retrieve(request, pk=prev_subtopic.id)
    
    @action(detail=True, methods=['GET'], name='set_subtopic_order_up', url_path=r'set-subtopic-order-up')
    def set_subtopic_order_up(self, request, pk, *args, **kwargs):
        subtopic = get_object_or_404(Subtopic, pk=pk)
        prev_subtopic = Subtopic.objects.filter(topic=subtopic.topic, order=subtopic.order-1).first()
        if prev_subtopic:
            subtopic.order = 999
            subtopic.save()
            prev_subtopic.order = prev_subtopic.order + 1
            prev_subtopic.save()
            subtopic.order = prev_subtopic.order - 1
            subtopic.save()
            subtopics = Subtopic.objects.filter(topic=subtopic.topic).all()
            template = render_template('ajax/subtopic/subtopic_list.html', {'subtopics':subtopics})
            return Response({'template': template}, status=status.HTTP_200_OK)
        return Response({'message': 'Cannot cannot find previous subtopic'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], name='set_subtopic_order_down', url_path=r'set-subtopic-order-down')
    def set_subtopic_order_down(self, request, pk, *args, **kwargs):
        subtopic = get_object_or_404(Subtopic, pk=pk)
        next_subtopic = Subtopic.objects.filter(topic=subtopic.topic, order=subtopic.order+1).first()
        if next_subtopic:
            subtopic.order = 999
            subtopic.save()
            next_subtopic.order = next_subtopic.order - 1
            next_subtopic.save()
            subtopic.order = next_subtopic.order + 1
            subtopic.save()
            subtopics = Subtopic.objects.filter(topic=subtopic.topic).all()
            template = render_template('ajax/subtopic/subtopic_list.html', {'subtopics':subtopics})
            return Response({'template': template}, status=status.HTTP_200_OK)
        return Response({'message': 'Cannot find next subtopic'}, status=status.HTTP_400_BAD_REQUEST)
 
class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name']
    ordering_fields = ['name', 'id']
    ordering = ['id']

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset

    @action(detail=True, methods=['PUT'], name='update_student', url_path=r'update', serializer_class=UpdateStudentSerializer)
    def update_student(self, request, pk, *args, **kwargs):
        student = Student.objects.get(id=pk)
        serializer = UpdateStudentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = student.user
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.username = data['email']
            student.full_name = f'{data["first_name"]} {data["last_name"]}'
            student.telephone = data["telephone"]
            user.save()
            student.save()
            student = StudentSerializer(student).data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'student':student}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], name='notes-progresses', url_path=r'notes-progresses')
    def notes_progresses(self, request, pk, *args, **kwargs):
        student = get_object_or_404(Student, id=pk)
        notes = Notes.objects.filter(level=student.level)
        data = dict()
        for note in notes:
            total = StudentNotesProgress.objects.filter(student=student, notes=note).count()
            complete = StudentNotesProgress.objects.filter(student=student, notes=note, status='COMPLETE').count()
            progress = round(complete/total * 100)
            data[note.id] = progress
        return Response(data, status=status.HTTP_200_OK)
    

class StudentAnswerViewSet(viewsets.ModelViewSet):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer
    permission_classes = []
    
    @action(detail=False, methods=['POST','GET'], name='submit_single_choice_answer', url_path=r'submit_single_choice_answer', serializer_class=StudentAnswerSerializer)
    def submit_single_choice_answer(self, request, *args, **kwargs):
        if request.method == 'GET': return Response({})
        serializer = StudentAnswerSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            student_id = data['student']
            choice_id = data['choice']
            question_id = data['question']
            choice = Choice.objects.get(id=choice_id)
            answer = StudentAnswer.objects.filter(question_id=question_id, student_id=student_id).first()
            if answer:
                answer.choice = choice
            else:
                answer = StudentAnswer.objects.create(**{
                    'student_id': data['student'],
                    'choice_id': data['choice'],
                    'question_id': data['question'],
                })
            answer.save()
            answer_serilizer = StudentAnswerSerializer(answer)
            return Response(answer_serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['DELETE','GET'], name='delete_answers', url_path=r'delete_answers')
    def delete_answers(self, request, *args, **kwargs):
        if request.method == 'GET': return Response({})
        params = request.query_params
        answers_to_delete = StudentAnswer.objects.filter(**params.dict())
        answers_to_delete.delete()
        return Response(status=status.HTTP_200_OK)
    
class StudentNotesProgressViewSet(viewsets.ModelViewSet):
    queryset = StudentNotesProgress.objects.order_by('id')
    serializer_class = StudentNotesProgressSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
        
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.order_by('-id').all()
    serializer_class = ExamSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

class ExamAnswerViewSet(viewsets.ModelViewSet):
    queryset = ExamAnswer.objects.all()
    serializer_class = ExamAnswerSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

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

class TeacherSchoolViewSet(viewsets.ModelViewSet):
    queryset = TeacherSchool.objects.all()
    serializer_class = TeacherSchoolSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['accepted', 'school', 'teacher']

class TeacherSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject', 'teacher']

class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['teacher_subject', 'teacher_subject__teacher', 'level', 'is_published']

    @action(detail=True, methods=['GET'], name='redorder_topics', url_path=r'reorder-topics')
    def redoreder_topics(self, request, pk, *args, **kwargs):
        notes = get_object_or_404(Notes, pk=pk)
        topics = notes.topic_set.order_by('order')
        order = 1
        for topic in topics:
            topic.order = order
            topic.save()
            order += 1
        data = NotesSerializer(notes).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST', 'GET'], name='enroll_student', url_path=r'enroll-student', serializer_class=EnrollStudentSerializer)
    def enroll_student(self, request, pk, *args, **kwargs):
        if request.method == 'POST':
            student = request.data['student']
            notes = get_object_or_404(Notes, pk=pk)
            topics = notes.topic_set.order_by('order')
            _status = 'STARTED'
            order = 1
            for topic in topics:
                StudentNotesProgress.objects.create(notes_id=notes.id, student_id=student, topic_id=topic.id, content=topic.introduction, category='topic', title=topic.name, status=_status, order=order)
                order +=1
                _status = None
                for subtopic in Subtopic.objects.filter(topic=topic):
                    StudentNotesProgress.objects.create(notes_id=notes.id, student_id=student, topic_id=topic.id, subtopic_id=subtopic.id, content=subtopic.content, category='subtopic', title=subtopic.name, order=order)
                    order += 1
                if topic.test:
                    StudentNotesProgress.objects.create(notes_id=notes.id, student_id=student, topic_id=topic.id, test_id=topic.test.id, category='test', title='Test', order=order)
                    order += 1
            progresses = StudentNotesProgress.objects.all()
            data = StudentNotesProgressSerializer(progresses, many=True).data
            
        else:
            data = []
        return Response(data, status=status.HTTP_200_OK)
    

class StudentNotesLogViewSet(viewsets.ModelViewSet):
    queryset = StudentNotesLog.objects.all()
    serializer_class = StudentNotesLogSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


class LearningCenterSubject(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = []
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = '__all__'

    def get_queryset(self):
        return self.queryset.filter(learning_center_id=self.kwargs["learning_center_id"])

    def perform_create(self, serializer):
        print(serializer)
        serializer.save(learning_center_id=self.kwargs["learning_center_id"])
