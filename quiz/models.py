from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=64)

class Question(models.Model):
    text = models.CharField(max_length=200)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text