# Generated by Django 4.2.6 on 2024-03-30 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_teacherschool'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='teacherschool',
            unique_together={('teacher', 'school')},
        ),
    ]
