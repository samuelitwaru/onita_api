from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Level, Subject, Subtopic, Topic
from .forms import CreateSubtopicForm, FilterByLevelForm, SubtopicForm, TopicForm


class SubjectList(ListView):
    model = Subject
    context_object_name = 'subjects'
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()


def get_subject(request, id):
    level = request.GET.get('level')
    subject = Subject.objects.get(id=id)
    topic_query = subject.topics
    if level and level!='0':
        topic_query = topic_query.filter(level=level)
    
    create_topic_form = TopicForm()
    filter_by_level_form = FilterByLevelForm(initial={'level':level})
    context = {'subject':subject, 'topics':topic_query.all(), 'create_topic_form': create_topic_form, 'filter_by_level_form': filter_by_level_form}
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

def create_topic(request, id):
    subject = get_object_or_404(Subject, id=id)
    create_topic_form = TopicForm()
    print(dir(create_topic_form.fields['subject']))
    print((create_topic_form.fields['subject'].initial))
    create_topic_form.fields['subject'].initial = subject.id
    create_topic_form.fields['test'].required = False
    if request.method == 'POST':
        data = request.POST
        create_topic_form = TopicForm(request.POST)
        if create_topic_form.is_valid():
            topic = Topic.objects.create(**create_topic_form.cleaned_data)
            topic.subject = subject
            topic.save()
            messages.success(request, 'Topic created')
        else:
            messages.error(request, f'{create_topic_form.errors}')
        return redirect(request.META.get('HTTP_REFERER'))
    context = {
        'subject': subject,
        'create_topic_form': create_topic_form
    }
    return render(request, 'api/create-topic-form.html', context)


def update_topic(request, id, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    update_topic_form = TopicForm(initial={
        'name': topic.name,
        'subject':topic.subject,
        'level': topic.level
    })
    if request.method == 'POST':
        data = request.POST
        update_topic_form = TopicForm(request.POST)
        if update_topic_form.is_valid():
            topic.name = data['name']
            topic.subject_id = data['subject']
            topic.level_id = data['level']
            topic.save()
            messages.success(request, 'Topic updated')
        else:
            messages.error(request, f'{update_topic_form.errors}', tags="danger")
        return redirect(request.META.get('HTTP_REFERER'))
    context = {'topic':topic, 'update_topic_form':update_topic_form}
    return render(request, 'api/update_topic.html', context)



def create_subtopic(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        create_subtopic_form = CreateSubtopicForm(request.POST)
        if create_subtopic_form.is_valid():
            Subtopic.objects.create(**create_subtopic_form.cleaned_data)
            messages.success(request, 'Subtopic created')
        else:
            messages.error(request, f'{create_subtopic_form.errors}')
        return redirect(request.META.get('HTTP_REFERER'))
    