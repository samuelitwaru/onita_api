from onita_api import router

from .viewsets import *


router.register(r'learning-centers', LearningCenterViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'subtopics', SubtopicViewSet)
# router.register(r'activities', ActivityViewSet)

router.register(r'questions', QuestionViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'students', StudentViewSet)
router.register(r'student-answers', StudentAnswerViewSet)
router.register(r'student-topic-progresses', StudentTopicProgressViewSet)
router.register(r'transactions', TransactionViewSet)


from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('subjects/', SubjectList.as_view(), name='subjects'),
    path('subjects/<id>', get_subject, name='get_subject'),
    path('subjects/<id>/topics/create', create_topic, name='create_topic'),
    path('subjects/<id>/topics/<topic_id>/update', update_topic, name='update_topic'),
    path('subjects/<id>/topics/<topic_id>/subtopics/<subtopic_id>', get_subtopic, name='get_subtopic'),
    path('subtopics/create', create_subtopic, name='create_subtopic'),
    path('subtopics/create', create_subtopic, name='create_subtopic'),
]
