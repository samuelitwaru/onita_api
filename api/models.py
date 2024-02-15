from django.db import models
from quiz.models import Choice, Test, Question as QuizQuestion
from django.dispatch import receiver
import os
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete




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
    
    def __str__(self):
        return f'{self.code} {self.name}'

class Topic(models.Model):

    def get_next_topic_order():
        last_topic = Topic.objects.order_by('order').last()
        if last_topic:
            return last_topic.order + 1
        return 1
    
    name = models.CharField(max_length=128)  # Field name made lowercase.
    subject = models.ForeignKey(Subject, models.DO_NOTHING, related_name='topics')  # Field name made lowercase.
    level = models.ForeignKey(Level, models.DO_NOTHING)  # Field name made lowercase.
    test = models.ForeignKey(Test, models.SET_NULL, null=True, blank=True)
    order = models.IntegerField(default=get_next_topic_order)

    class Meta:
        unique_together = (('subject','order'))

    def __str__(self):
        return self.name
    

class Subtopic(models.Model):
    from ckeditor.fields import RichTextField
    name = models.CharField(max_length=128)  # Field name made lowercase.
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Field name made lowercase. The composite primary key (TopicId, SubTopicId) found, that is not supported. The first column is selected.
    content = RichTextField()
    order = models.IntegerField(null=True)

    class Meta:
        unique_together = (('topic','order'))
    
    def __str__(self):
        return self.name
    

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


# class Question(TimeStampedModel):
#     ref = models.CharField(max_length=128)
#     level = models.ForeignKey(Level, on_delete=models.CASCADE)
#     certificate = models.CharField(max_length=32) # UCE, UACE, PLE
#     examiner = models.CharField(max_length=128) # UNEB
#     mark = models.IntegerField()
#     number = models.IntegerField()
#     paper_code = models.CharField(max_length=16)
#     paper_name = models.CharField(max_length=16)
#     paper_type = models.CharField(max_length=16)

#     section = models.CharField(max_length=1)
#     year = models.IntegerField()

#     term = models.IntegerField()
#     time = models.IntegerField()
#     question = models.TextField()
#     answer = models.TextField()

#     def __str__(self):
#         return self.ref


class School(TimeStampedModel):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=256)
    telephone = models.CharField(max_length=16, null=True, blank=True)
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    

class Teacher(TimeStampedModel):
    full_name = models.CharField(max_length=128)
    telephone = models.CharField(max_length=16, null=True, blank=True)
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.full_name

class Student(TimeStampedModel):
    full_name = models.CharField(max_length=128)
    telephone = models.CharField(max_length=16, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name
    
class StudentAnswer(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'student', 'choice')


class StudentTopicProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'subject')


class Transaction(models.Model):
    TYPE_CHOICES = [('C', 'CREDIT'), ('D', 'DEBIT')]
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    description = models.TextField()


@receiver(post_save, sender=Student)
def set_student_topic_progresses(sender, instance, created, **kwargs):
    if created:
        subjects = instance.level.learning_center.subject_set.all()
        print(subjects)
        for subject in subjects:
            topic = subject.topics.filter(order=1).first()
            if topic:
                StudentTopicProgress.objects.get_or_create(**{
                    "student_id": instance.id,
                    "subject_id": subject.id,
                    "topic_id": topic.id,
                })

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