# Generated by Django 4.2.6 on 2023-11-06 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
        ('api', '0004_alter_student_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.test'),
        ),
    ]
