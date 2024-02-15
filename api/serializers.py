from rest_framework import serializers

from quiz.serializers import TestSerializer

from .models import *


class LearningCenterSerializer(serializers.ModelSerializer):    
    class Meta:
        model = LearningCenter
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'
    

class SubtopicSerializer(serializers.ModelSerializer):
    # topic = serializers.ChoiceField(choices=[(topic.id, topic.name) for topic in Topic.objects.all()])
    topic_name = serializers.CharField(source='topic.name', read_only=True)
    class Meta:
        model = Subtopic
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    subtopics = SubtopicSerializer(many=True, source='subtopic_set', read_only=True)
    test = TestSerializer(read_only=True)
    class Meta:
        model = Topic
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    learning_center_name = serializers.CharField(source='learning_center.name')
    class Meta:
        model = Subject
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'




# class ActivitySerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Activity
#         fields = '__all__'


# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = '__all__'


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = '__all__'


class StudentTopicProgressSerializer(serializers.ModelSerializer):
    topic_detail = TopicSerializer(source='topic',read_only=True)
    subject_detail = SubjectSerializer(source='subject',read_only=True)
    class Meta:
        model = StudentTopicProgress
        fields = '__all__'

class UpdateStudentSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    telephone = serializers.IntegerField()
    email = serializers.EmailField()

