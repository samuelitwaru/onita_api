from api.models import Student, StudentTopicProgress


def set_student_topic_progresses(student):
    subjects = student.level.learning_center.subject_set.all()
    print(subjects)
    for subject in subjects:
        topic = subject.topics.filter(order=1).first()
        print(subject.id, subject, topic)
        if topic:
            res = StudentTopicProgress.objects.get_or_create(**{
                "student_id": student.id,
                "subject_id": subject.id,
                "topic_id": topic.id,
            })
