# Generated by Django 4.2.6 on 2023-11-09 11:31

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_subtopic_id_alter_subtopic_topic_delete_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtopic',
            name='content2',
            field=ckeditor.fields.RichTextField(default=''),
            preserve_default=False,
        ),
    ]
