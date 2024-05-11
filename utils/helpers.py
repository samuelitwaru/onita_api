from api.models import Student, StudentTopicProgress, Level
from django.db.utils import OperationalError, ProgrammingError

def get_level_choices():
    try:
        return [(level.id, level.name) for level in Level.objects.all()]
    except (OperationalError,ProgrammingError):
        return []

LEVEL_CHOICES = get_level_choices()



def set_student_topic_progresses(student):
    subjects = student.level.learning_center.subject_set.all()
    for subject in subjects:
        topic = subject.topics.filter(order=1).first()
        print(subject.id, subject, topic)
        if topic:
            res = StudentTopicProgress.objects.get_or_create(**{
                "student_id": student.id,
                "subject_id": subject.id,
                "topic_id": topic.id,
            })

