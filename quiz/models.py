from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    text = RichTextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
    @property
    def is_multiple_choice(self):
        return self.choices.filter(is_correct=True).count() > 1

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = RichTextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text