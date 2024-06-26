from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Question(models.Model):
    subject = models.ForeignKey('api.Subject', on_delete=models.CASCADE)
    text = RichTextField()
    # test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
    mark = models.IntegerField(default=1)
    time = models.IntegerField(default=120)
    is_multiple_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
    @property
    def has_multiple_choices(self):
        return self.choices.filter(is_correct=True).count() > 1
    
class Exam(TimestampedModel):
    subject = models.ForeignKey('api.Subject', on_delete=models.CASCADE)
    student = models.ForeignKey('api.Student', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    submitted = models.BooleanField(default=False)
    time_taken = models.IntegerField(default=0)

    @property
    def all_questions_answered(self):
        for exam_answer in self.examanswer_set.all():
            if bool(exam_answer.answer) == False:
                return False
        return True
    
    @property
    def total_time(self):
        total = 8*3600
        # for exam_answer in self.examanswer_set.all():
        #     total += exam_answer.question.time
        # print(total)
        return total

class ExamAnswer(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

class LearningCenter(models.Model):
    name = models.CharField(unique=True, max_length=128)  # Field name made lowercase.

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=128)  # Field name made lowercase.
    learning_center = models.ForeignKey(LearningCenter, models.DO_NOTHING)  # Field name made lowercase.

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=128)  # Field name made lowercase.
    learning_center = models.ForeignKey(LearningCenter, models.DO_NOTHING)  # Field name made lowercase.
    code = models.CharField(max_length=128)  # Field name made lowercase.
    image = models.ImageField(upload_to='subjects/', null=True, blank=True)
    def __str__(self):
        return f'{self.code} {self.name}'
    
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class School(TimeStampedModel):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=256)
    telephone = models.CharField(max_length=16, null=True, blank=True)
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Teacher(TimeStampedModel):
    full_name = models.CharField(max_length=128)
    telephone = models.CharField(max_length=16, null=True, blank=True)
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name
    

class TeacherSchool(TimestampedModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = (('teacher','school'))


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject.name


class Notes(models.Model):
    title = models.CharField(max_length=128)
    teacher_subject = models.ForeignKey(TeacherSubject, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, null=True, blank=True, on_delete=models.SET_NULL)
    introduction = RichTextField(default='')
    is_published = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Student(TimeStampedModel):
    full_name = models.CharField(max_length=128)
    telephone = models.CharField(max_length=16, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name
    
class StudentSchool(TimestampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = (('student','school'))


class Test(models.Model):
    name = models.CharField(max_length=128)



class Topic(models.Model):
    name = models.CharField(max_length=128)  # Field name made lowercase.
    introduction = RichTextField(default='')
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE, null=True, blank=True)
    level = models.ForeignKey(Level, models.SET_NULL, null=True, blank=True)  # Field name made lowercase.
    test = models.ForeignKey(Test, models.SET_NULL, null=True, blank=True)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    

class Subtopic(models.Model):
    name = models.CharField(max_length=128)  # Field name made lowercase.
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Field name made lowercase. The composite primary key (TopicId, SubTopicId) found, that is not supported. The first column is selected.
    content = RichTextField(default='')
    order = models.IntegerField(default=1)

    class Meta:
        unique_together = (('topic','order'))
    
    def __str__(self):
        return self.name


class StudentNotesProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=64, null=True, blank=True)
    title = models.CharField(max_length=64, default='')
    content = RichTextField(default='')
    category = models.CharField(max_length=64, null=True, blank=True)
    order = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('student', 'notes', 'topic', 'subtopic', 'status')


class TopicQuestion(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, blank=True)
    text = RichTextField()
    mark = models.IntegerField(default=1)
    time = models.IntegerField(default=120)
    is_multiple_choice = models.BooleanField(default=False)

    @property
    def has_multiple_choices(self):
        return self.choices.filter(is_correct=True).count() > 1


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True, related_name='choices')
    text = RichTextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class TopicQuestionChoice(models.Model):
    topic_question = models.ForeignKey(TopicQuestion, on_delete=models.SET_NULL, null=True, blank=True, related_name='choices')
    text = RichTextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class StudentAnswer(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'student', 'choice')

class TopicQuestionStudentAnswer(models.Model):
    topic_question = models.ForeignKey(TopicQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('topic_question', 'student')


class StudentNotesLog(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.CharField(max_length=128)
    
    class Meta:
        unique_together = ('topic', 'student', 'note')


class Transaction(models.Model):
    TYPE_CHOICES = [('C', 'CREDIT'), ('D', 'DEBIT')]
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    description = models.TextField()


@receiver(post_save, sender=Topic)
def set_topic_order(sender, instance, created, **kwargs):
    if not created: return 
    last_topic = Topic.objects.filter(notes=instance.notes).order_by('order').last()
    if last_topic:
        instance.order = last_topic.order + 1
    else:
        instance.order = 1

@receiver(post_save, sender=Subtopic)
def set_next_subtopic_order(sender, instance, created, **kwargs):
    if created:
        topic_id = instance.topic.id
        last_subtopic = Subtopic.objects.filter(topic_id=topic_id).order_by('order').last()
        if last_subtopic:
            instance.order = (last_subtopic.order or 0) + 1
        else:
            instance.order = 1
        instance.save()


@receiver(post_save, sender=Exam)
def set_exam_questions(sender, instance, created, **kwargs):
    if created:
        no_questions = 10
        questions = Question.objects.filter(subject=instance.subject).order_by('?').all()
        if len(questions) > no_questions:
            questions = questions[:no_questions]
        time = 0
        for question in questions:
            answer = ExamAnswer(exam=instance, question=question)
            answer.save()
            time += question.time
        instance.time = time
        instance.save()
