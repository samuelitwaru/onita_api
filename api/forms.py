from ckeditor.widgets import CKEditorWidget
from django import forms

from api.models import Level, Subject, Subtopic, Topic

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
    level = forms.ChoiceField(choices=[(level.id, level.name) for level in Level.objects.all()])