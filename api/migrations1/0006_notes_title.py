# Generated by Django 4.2.6 on 2024-04-05 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_notes_teacher_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='title',
            field=models.CharField(default='My Notes', max_length=128),
            preserve_default=False,
        ),
    ]
