from django.db import models
from quiz.models import Test



class LearningCenter(models.Model):
    name = models.CharField(unique=True, max_length=20)  # Field name made lowercase.

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=20)  # Field name made lowercase.
    learning_center = models.ForeignKey(LearningCenter, models.DO_NOTHING)  # Field name made lowercase.

    def __str__(self):
        return self.name
    

class Subject(models.Model):
    name = models.CharField(max_length=20)  # Field name made lowercase.
    learning_center = models.ForeignKey(LearningCenter, models.DO_NOTHING)  # Field name made lowercase.
    code = models.CharField(max_length=20)  # Field name made lowercase.
    
    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=128)  # Field name made lowercase.
    subject = models.ForeignKey(Subject, models.DO_NOTHING, related_name='topics')  # Field name made lowercase.
    level = models.ForeignKey(Level, models.DO_NOTHING)  # Field name made lowercase.
    test = models.ForeignKey(Test, models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    

class Subtopic(models.Model):
    from ckeditor.fields import RichTextField
    name = models.CharField(max_length=20)  # Field name made lowercase.
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Field name made lowercase. The composite primary key (TopicId, SubTopicId) found, that is not supported. The first column is selected.
    content = models.TextField()
    content2 = RichTextField()
    
    def __str__(self):
        return self.name
    

# class Activity(models.Model):
#     name = models.CharField(max_length=128)  # Field name made lowercase.
#     date_from = models.DateField()  # Field name made lowercase.
#     date_to = models.DateField()  # Field name made lowercase.
#     topic = models.OneToOneField(Subtopic, on_delete=models.CASCADE)  # Field name made lowercase. The composite primary key (TopicId, SubTopicId, ActivityId) found, that is not supported. The first column is selected.
#     subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, related_name='topicsubtopicactivity_subtopicid_set')  # Field name made lowercase.

#     class Meta:
#         unique_together = (('topic', 'subtopic'),)

#     def __str__(self):
#         return self.name
    

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Question(TimeStampedModel):
    ref = models.CharField(max_length=32)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    certificate = models.CharField(max_length=32) # UCE, UACE, PLE
    examiner = models.CharField(max_length=32) # UNEB
    mark = models.IntegerField()
    number = models.IntegerField()
    paper_code = models.CharField(max_length=16)
    paper_name = models.CharField(max_length=16)
    paper_type = models.CharField(max_length=16)

    section = models.CharField(max_length=1)
    year = models.IntegerField()

    term = models.IntegerField()
    time = models.IntegerField()
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.ref


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
    # schools =
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    # classes = 

    def __str__(self):
        return self.full_name

class Student(TimeStampedModel):
    full_name = models.CharField(max_length=128)
    telephone = models.CharField(max_length=16, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField("auth.User", on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name
