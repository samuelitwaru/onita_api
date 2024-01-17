from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView
from ..models import Subject
from ..forms import FilterByLevelForm, TopicForm


class SubjectList(ListView):
    model = Subject
    context_object_name = 'subjects'
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        # Implement filtering logic if needed
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset


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
