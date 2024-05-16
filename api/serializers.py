from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from account.serializers import UserSerializer

from .models import *

class ChoiceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Choice
        fields = '__all__'

class TopicQuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicQuestionChoice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices =  ChoiceSerializer(read_only=True, many=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    has_multiple_choices = serializers.BooleanField(read_only=True)
    class Meta:
        model = Question
        fields = '__all__'

class TopicQuestionSerializer(serializers.ModelSerializer):
    choices =  TopicQuestionChoiceSerializer(read_only=True, many=True)
    has_multiple_choices = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = TopicQuestion
        fields = '__all__'


class TopicQuestionStudentAnswerSerializer(serializers.ModelSerializer):
    question_detail = TopicQuestionSerializer(source='topic_question', read_only=True)
    class Meta:
        model = TopicQuestionStudentAnswer
        fields = '__all__'
    
    validators = [
        UniqueTogetherValidator(
            queryset=TopicQuestionStudentAnswer.objects.all(),
            fields=('topic_question', 'student'),  # Replace field1 and field2 with your actual field names
            message='The combination of topic_question and student must be unique.'
        )
    ]


class TestSerializer(serializers.ModelSerializer): 
    questions = TopicQuestionSerializer(many=True, source='topicquestion_set', read_only=True)
    class Meta:
        model = Test
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
    # test = TestSerializer(read_only=True)
    class Meta:
        model = Topic
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    learning_center_name = serializers.CharField(source='learning_center.name', read_only=True)
    class Meta:
        model = Subject
        fields = '__all__'

class LearningCenterSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, source='subject_set', read_only=True)

    class Meta:
        model = LearningCenter
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'



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
    all_questions_answered = serializers.BooleanField(read_only=True)
    total_time = serializers.IntegerField(read_only=True)
    class Meta:
        model = Exam
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
    user = UserSerializer(read_only=True)   
    level = LevelSerializer(read_only=True)   
    class Meta:
        model = Student
        fields = '__all__'


class TeacherSchoolSerializer(serializers.ModelSerializer):
    school_detail = SchoolSerializer(source='school', read_only=True)
    teacher_detail = TeacherSerializer(source='teacher', read_only=True)
    class Meta:
        model = TeacherSchool
        fields = '__all__'


class StudentNotesLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    topic_detail = TopicSerializer(source='topic', read_only=True)
    class Meta:
        model = StudentNotesLog
        fields = '__all__'

class NotesSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(source='topic_set', many=True, read_only=True)
    subject_detail = SubjectSerializer(source='teacher_subject.subject', read_only=True)
    teacher_detail = TeacherSerializer(source='teacher_subject.teacher', read_only=True)
    logs = StudentNotesLogSerializer(source='studentnoteslog_set', many=True, read_only=True)
    class Meta:
        model = Notes
        fields = '__all__'

class TeacherSubjectSerializer(serializers.ModelSerializer):
    teacher_detail = TeacherSerializer(source='teacher', read_only=True)
    subject_detail = SubjectSerializer(source='subject', read_only=True)
    notes = NotesSerializer(many=True, source='notes_set', read_only=True)
    class Meta:
        model = TeacherSubject
        fields = '__all__'


        
