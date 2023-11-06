from rest_framework import serializers

from .models import *


class TestSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Test
        fields = '__all__'



class ChoiceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices =  ChoiceSerializer(read_only=True, many=True)
    class Meta:
        model = Question
        fields = '__all__'