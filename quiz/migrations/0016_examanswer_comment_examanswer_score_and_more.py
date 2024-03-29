# Generated by Django 4.2.6 on 2024-02-24 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0015_question_is_multiple_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='examanswer',
            name='comment',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='examanswer',
            name='score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='is_multiple_choice',
            field=models.BooleanField(default=False),
        ),
    ]
