# Generated by Django 4.2.6 on 2024-02-09 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_transaction'),
        ('quiz', '0005_exam_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.subject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.subject'),
            preserve_default=False,
        ),
    ]
