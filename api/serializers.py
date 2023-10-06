from rest_framework import serializers
from .models import *


class LearningCenterSerializer(serializers.ModelSerializer):    
    class Meta:
        model = LearningCenter
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'
    

class SubjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subject
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Topic
        fields = '__all__'

class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtopic
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activity
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class SchoolSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = School
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Student
        fields = '__all__'