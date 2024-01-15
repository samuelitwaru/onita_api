from rest_framework import viewsets
from api.models import StudentAnswer, StudentTopicProgress
from rest_framework import viewsets
from rest_framework.decorators import action
from api.models import  Topic
from api.serializers import StudentAnswerSerializer, StudentTopicProgressSerializer, TopicSerializer
from rest_framework.response import Response
from rest_framework import status
from quiz.models import Choice, Test



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
        topic = Topic.objects.get(test=test)
        topic_order = topic.order
        next_topic = Topic.objects.filter(order=topic_order+1).first()
        student_id = answer.student.id
        print(student_id, topic.id)
        student_progress = StudentTopicProgress.objects.filter(
            student_id=student_id,
            topic_id=topic.id
            ).first()

        if next_topic:
            report['next_topic'] = TopicSerializer(next_topic).data
            report['student_progress'] = StudentTopicProgressSerializer(student_progress).data
        return Response(report, status=status.HTTP_200_OK)
        
