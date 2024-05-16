from django.shortcuts import redirect
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseNotFound
from api.models import Choice, Question, Test

def notes_editor(request, notes_id):
    context = {'notes_id': notes_id}
    return render(request, 'notes-editor.html', context)