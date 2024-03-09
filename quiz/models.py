from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Test(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    subject = models.ForeignKey('api.Subject', on_delete=models.CASCADE)
    text = RichTextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    mark = models.IntegerField(default=1)
    time = models.IntegerField(default=120)
    is_multiple_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
    @property
    def has_multiple_choices(self):
        return self.choices.filter(is_correct=True).count() > 1

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = RichTextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    

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
        total = 0
        for exam_answer in self.examanswer_set.all():
            total += exam_answer.question.time
        print(total)
        return total
    
    


class ExamAnswer(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True)
    comment = models.TextField(null=True)


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

    
    