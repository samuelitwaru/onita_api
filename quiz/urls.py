from onita_api import router

from .viewsets import *


router.register(r'tests', TestViewSet)
router.register(r'test-questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)

from django.urls import path
from .views import *

urlpatterns = [
    path('tests/', TestList.as_view(), name='tests'),
    path('tests/<id>', get_test, name='get_test'),
    path('tests/<id>/questions/<question_id>', get_question, name='get_question'),
    path('tests/<id>/questions/<question_id>/choices/<choice_id>', get_choice, name='get_choice'),

]
