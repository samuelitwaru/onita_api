# Generated by Django 4.2.6 on 2024-05-04 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_studenttopicprogress_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studentnoteslog',
            unique_together={('topic', 'student')},
        ),
    ]
