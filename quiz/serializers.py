from rest_framework import serializers

from .models import *

class ChoiceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices =  ChoiceSerializer(read_only=True, many=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    has_multiple_choices = serializers.BooleanField(read_only=True)
    class Meta:
        model = Question
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer): 
    questions = QuestionSerializer(many=True, source='question_set', read_only=True)
    class Meta:
        model = Test
        fields = '__all__'



class ExamAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    question_mark = serializers.IntegerField(source='question.mark', read_only=True)
    question_time = serializers.IntegerField(source='question.time', read_only=True)
    question_detail = QuestionSerializer(source='question', read_only=True)
    # answer_text = serializers.CharField(source='examanswer.answer')
    class Meta:
        model = ExamAnswer
        fields = '__all__'


class ExamSerializer(serializers.ModelSerializer): 
    questions = ExamAnswerSerializer(many=True, source='examanswer_set', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_learning_center_name = serializers.CharField(source='subject.learning_center.name', read_only=True)
    class Meta:
        model = Exam
        fields = '__all__'


