from onita_api import router

from .viewsets import *


router.register(r'learning-centers', LearningCenterViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'activities', ActivityViewSet)

router.register(r'questions', QuestionViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'students', StudentViewSet)
