from onita_api import router, srouter

from .viewsets import *


router.register(r'learning-centers', LearningCenterViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'subtopics', SubtopicViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'students', StudentViewSet)
router.register(r'student-answers', StudentAnswerViewSet)
router.register(r'student-notes-progresses', StudentNotesProgressViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'tests', TestViewSet)
router.register(r'test-questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'exam-answers', ExamAnswerViewSet)
router.register(r'teacher-schools', TeacherSchoolViewSet)
router.register(r'teacher-subjects', TeacherSubjectViewSet)
router.register(r'notes', NotesViewSet)
router.register(r'student-notes-logs', StudentNotesLogViewSet)
router.register(r'topic-questions', TopicQuestionViewSet)
router.register(r'topic-question-choices', TopicQuestionChoiceViewSet)
router.register(r'topic-question-student-answers', TopicQuestionStudentAnswerViewSet)


srouter.register(r'learning-centers/(?P<learning_center_id>[^/.]+)/subjects', LearningCenterSubject)

from django.urls import path
from .views1 import *
from .views import *

urlpatterns = [
    path('notes-editor/<notes_id>', notes_editor),
    # path('', index, name='index'),
    path('subjects/', SubjectList.as_view(), name='subjects'),
    path('subjects/<id>', get_subject, name='get_subject'),
    path('subjects/<id>/topics/create', create_topic, name='create_topic'),
    path('subjects/<id>/topics/<topic_id>/update', update_topic, name='update_topic'),
    path('subjects/<id>/topics/<topic_id>/subtopics/<subtopic_id>', get_subtopic, name='get_subtopic'),
    path('subtopics/create', create_subtopic, name='create_subtopic'),
    path('subtopics/create', create_subtopic, name='create_subtopic'),
    # path('tests/', TestList.as_view(), name='tests'),
    # path('tests/create', create_test, name='create_test'),
    # path('choices/<question_id>/create', create_choice, name='create_choice'),
    # path('tests/<id>', get_test, name='get_test'),
    # path('tests/<id>/questions/create', create_question, name='create_question'),
    # path('tests/<id>/questions/<question_id>', get_question, name='get_question'),
    # path('tests/<id>/questions/<question_id>/choices/<choice_id>', get_choice, name='get_choice'),
]
