# Generated by Django 4.2.6 on 2024-02-09 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_transaction'),
        ('quiz', '0004_exam_examanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.student'),
            preserve_default=False,
        ),
    ]
