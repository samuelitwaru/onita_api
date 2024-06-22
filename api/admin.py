from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Student)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(StudentNotesProgress)
admin.site.register(TopicQuestion)
admin.site.register(Choice)
admin.site.register(TopicQuestionChoice)
admin.site.register(StudentNotesLog)
admin.site.register(Exam)
admin.site.register(ExamAnswer)
admin.site.register(Teacher)
admin.site.register(School)
admin.site.register(Notes)