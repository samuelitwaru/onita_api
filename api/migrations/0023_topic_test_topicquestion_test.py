# Generated by Django 4.2.6 on 2024-05-07 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_remove_question_test_remove_topic_test_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.test'),
        ),
        migrations.AddField(
            model_name='topicquestion',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.test'),
        ),
    ]
