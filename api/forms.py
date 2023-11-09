from ckeditor.widgets import CKEditorWidget
from django import forms

class SubtopicForm(forms.Form):
    name = forms.CharField()
    content = forms.CharField(widget=CKEditorWidget())