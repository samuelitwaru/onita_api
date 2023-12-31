# Generated by Django 4.2.6 on 2023-11-19 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_studenttopicprogress'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='order',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterUniqueTogether(
            name='studenttopicprogress',
            unique_together={('student', 'subject')},
        ),
    ]
