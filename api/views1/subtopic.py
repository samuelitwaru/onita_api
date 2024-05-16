from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Subtopic
from ..forms import CreateSubtopicForm, SubtopicForm

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
    