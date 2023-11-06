from onita_api import router

from .viewsets import *


router.register(r'tests', TestViewSet)
router.register(r'test-questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)