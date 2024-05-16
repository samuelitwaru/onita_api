from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Subject, Subtopic, Topic
from ..forms import CreateSubtopicForm, SubtopicForm, TopicForm


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
    