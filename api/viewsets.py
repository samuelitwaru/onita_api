from account.filters import BaseFilter
from rest_framework import viewsets
from .models import *
from .serializers import *
from account.serializers import SchoolSerializer, TeacherSerializer, StudentSerializer
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status

class LearningCenterViewSet(viewsets.ModelViewSet):
    queryset = LearningCenter.objects.all()
    serializer_class = LearningCenterSerializer
    permission_classes = []


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = []


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = []
    
    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = []


class SubtopicViewSet(viewsets.ModelViewSet):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer
    permission_classes = []

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset


# class ActivityViewSet(viewsets.ModelViewSet):
#     queryset = Activity.objects.all()
#     serializer_class = ActivitySerializer
#     permission_classes = []


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = []


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = []


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = []


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = []

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset

    @action(detail=True, methods=['PUT'], name='update_student', url_path=r'update', serializer_class=UpdateStudentSerializer)
    def update_student(self, request, pk, *args, **kwargs):
        student = Student.objects.get(id=pk)
        serializer = UpdateStudentSerializer(request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user= student.user
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.username = data['email']
            student.full_name = f'{data["first_name"]} {data["last_name"]}'
            user.save()
            student.save()

            return Response({'detail': 'Student updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class StudentAnswerViewSet(viewsets.ModelViewSet):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer
    permission_classes = []

    # def get_queryset(self):
    #     params = self.request.query_params
    #     f = BaseFilter(self.queryset, params)
    #     queryset = f.filter()
    #     return queryset
    
    @action(detail=False, methods=['POST'], name='submit_single_choice_answer', url_path=r'submit_single_choice_answer', serializer_class=StudentAnswerSerializer)
    def submit_single_choice_answer(self, request, *args, **kwargs):
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
    
    @action(detail=False, methods=['DELETE'], name='delete_answers', url_path=r'delete_answers')
    def delete_answers(self, request, *args, **kwargs):
        params = request.query_params
        answers_to_delete = StudentAnswer.objects.filter(**params.dict())
        answers_to_delete.delete()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], name='submit_answers', url_path=r'submit_answers')
    def submit_answers(self, request, *args, **kwargs):
        params = request.query_params
        test_id = params.get('question__test')
        
        answers = StudentAnswer.objects.filter(**params.dict()).all()
        report = {
            'answers':dict(),

        }
        for answer in answers:
            if report.get(answer.question.id):
                report['answers'][answer.question.id]['answers'].append(answer.choice.is_correct)
            else:
                report['answers'][answer.question.id] = dict()
                report['answers'][answer.question.id]['answers'] = [answer.choice.is_correct]
                report['answers'][answer.question.id]['question'] = answer.question.text
        test = Test.objects.get(id=test_id)
        topic_order = Topic.objects.get(test=test).order
        next_topic = Topic.objects.filter(order=topic_order+1).first()
        if next_topic:
            report['next_topic'] = TopicSerializer(next_topic).data
        return Response(report, status=status.HTTP_200_OK)
        

class StudentTopicProgressViewSet(viewsets.ModelViewSet):
    queryset = StudentTopicProgress.objects.all()
    serializer_class = StudentTopicProgressSerializer
    permission_classes = []

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset










