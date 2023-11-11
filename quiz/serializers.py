from rest_framework import serializers

from .models import *

class ChoiceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices =  ChoiceSerializer(read_only=True, many=True)
    is_multiple_choice = serializers.BooleanField()
    class Meta:
        model = Question
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer): 
    questions = QuestionSerializer(many=True, source='question_set', read_only=True)
    class Meta:
        model = Test
        fields = '__all__'


