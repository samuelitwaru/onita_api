# Generated by Django 4.2.6 on 2023-11-09 17:14

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_subtopic_content2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtopic',
            name='content2',
        ),
        migrations.AlterField(
            model_name='subtopic',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
