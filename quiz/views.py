from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from quiz.forms import ChoiceForm, QuestionForm
from .models import Choice, Question, Test


class TestList(ListView):
    model = Test
    context_object_name = 'tests'
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()
    
def get_test(request, id):
    test = Test.objects.get(id=id)
    question_form = QuestionForm()
    context = {'test':test, 'question_form':question_form}
    return render(request, 'quiz/test.html', context)


def get_question(request, id, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question.text = request.POST['text']
            question.save()
            messages.success(request, 'Updated question')
    form = QuestionForm(data={'text':question.text})
    context = {'question':question, 'form': form}
    return render(request, 'quiz/question.html', context)

def get_choice(request, id, question_id, choice_id):
    choice = Choice.objects.get(id=choice_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice.text = request.POST['text']
            choice.save()
            messages.success(request, 'Updated question')
    form = ChoiceForm(data={'text':choice.text, 'is_correct': choice.is_correct})
    context = {'choice':choice, 'form': form}
    return render(request, 'quiz/choice.html', context)