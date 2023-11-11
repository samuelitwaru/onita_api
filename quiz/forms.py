from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget


class TestForm(forms.ModelForm):
    """Form definition for Test."""

    class Meta:
        """Meta definition for Testform."""

        model = Test
        fields = ('name',)  


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
