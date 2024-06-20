from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget

from api.models import Level, Subject, Subtopic, Topic
from utils.helpers import LEVEL_CHOICES

class SubtopicForm(forms.Form):
    name = forms.CharField()
    content = forms.CharField(widget=CKEditorWidget())

class CreateSubtopicForm(forms.ModelForm):

    class Meta:
        model = Subtopic
        exclude = ('content', 'order')


class TopicForm(forms.ModelForm):
    
    class Meta:
        model = Topic
        exclude = ('order',)


class FilterByLevelForm(forms.Form):
    level = forms.ChoiceField(choices=[(0, 'All Levels')]+LEVEL_CHOICES)



# class TestForm(forms.ModelForm):
#     """Form definition for Test."""

#     class Meta:
#         """Meta definition for Testform."""

#         model = Test
#         fields = ('name',)  


class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Question
        fields = ('text',)  


class ChoiceForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        """Meta definition for Choiceform."""

        model = Choice
        fields = ('text', 'is_correct') 