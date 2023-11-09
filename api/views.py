from django.shortcuts import render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Subject, Subtopic
from .forms import SubtopicForm


class SubjectList(ListView):
    model = Subject
    context_object_name = 'subjects'

def get_subject(request, id):
    subject = Subject.objects.get(id=id)
    context = {'subject':subject}
    return render(request, 'api/subject.html', context)

def get_subtopic(request, id, topic_id, subtopic_id):
    subtopic = Subtopic.objects.get(id=subtopic_id)
    if request.method == 'POST':
        form = SubtopicForm(request.POST)
        if form.is_valid():
            subtopic.name = request.POST['name']
            subtopic.content = request.POST['content']
            subtopic.save()
            messages.success(request, 'Updated subtopic')
    form = SubtopicForm(data={'name':subtopic.name, 'content':subtopic.content})
    context = {'subtopic':subtopic, 'form': form}
    return render(request, 'api/subtopic.html', context)