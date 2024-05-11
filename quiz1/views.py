from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseNotFound
from .forms import ChoiceForm, QuestionForm, TestForm
from .models import Choice, Question, Test


class TestList(ListView):
    model = Test
    context_object_name = 'tests'
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TestForm()
        context['form'] = form
        return context

def create_test(request):
    if request.method == 'POST':
        form = TestForm(data=request.POST)
        if form.is_valid():
            # CREATE TEST
            test = Test.objects.create(**form.cleaned_data)
            messages.success(request, 'Test Created')
            return redirect('get_test', id=test.id)
        context = {'form':form}
        return render(request, 'quiz/create_test.html', context)
    return HttpResponseNotFound("The requested resource was not found.")

def create_question(request, id):
    test = get_object_or_404(Test, id=id)
    if request.method == 'POST':
        create_question_form = QuestionForm(request.POST)
        if create_question_form.is_valid():
            Question.objects.create(**create_question_form.cleaned_data | {'test_id':test.id})
            messages.success(request, 'Question created')
        else:
            messages.error(request, f'{create_question_form.errors}')
        return redirect(request.META.get('HTTP_REFERER'))
    form = QuestionForm()
    context = {'form': form, 'test':test}
    return render(request, 'quiz/create_question.html', context)


def create_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = ChoiceForm(data=request.POST)
        if form.is_valid():
            # CREATE TEST
            print(form.cleaned_data)
            messages.success(request, 'Test Created')
            choice = Choice(**form.cleaned_data)
            choice.question = question
            choice.save()
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('get_test', id=question.test.id)

    return HttpResponseNotFound("The requested resource was not found.")
    
def get_test(request, id):
    test = Test.objects.get(id=id)
    question_form = QuestionForm()
    choice_form = ChoiceForm()
    context = {'test':test, 'question_form':question_form, 'choice_form':choice_form}
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