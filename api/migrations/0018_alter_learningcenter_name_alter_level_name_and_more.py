# Generated by Django 4.2.6 on 2024-01-15 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_choice_text_alter_question_text_and_more'),
        ('api', '0017_alter_subtopic_unique_together_alter_topic_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningcenter',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='level',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='question',
            name='examiner',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='question',
            name='ref',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='subtopic',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='topic',
            name='test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.test'),
        ),
        migrations.AlterUniqueTogether(
            name='subtopic',
            unique_together={('topic', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='topic',
            unique_together={('subject', 'order')},
        ),
    ]
