# Generated by Django 4.2.6 on 2024-05-10 07:27

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_topic_test_topicquestion_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.level'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='introduction',
            field=ckeditor.fields.RichTextField(default=''),
        ),
    ]
