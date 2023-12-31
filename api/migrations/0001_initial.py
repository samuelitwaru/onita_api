# Generated by Django 4.2.6 on 2023-10-06 03:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('learning_center', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.learningcenter')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=128)),
                ('location', models.CharField(max_length=256)),
                ('telephone', models.CharField(blank=True, max_length=16, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=20)),
                ('learning_center', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.learningcenter')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.level')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Subtopic',
            fields=[
                ('name', models.CharField(max_length=20)),
                ('topic', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.topic')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('full_name', models.CharField(max_length=128)),
                ('telephone', models.CharField(blank=True, max_length=16, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('full_name', models.CharField(max_length=128)),
                ('telephone', models.CharField(blank=True, max_length=16, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.school')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('ref', models.CharField(max_length=32)),
                ('certificate', models.CharField(max_length=32)),
                ('examiner', models.CharField(max_length=32)),
                ('mark', models.IntegerField()),
                ('number', models.IntegerField()),
                ('paper_code', models.CharField(max_length=16)),
                ('paper_name', models.CharField(max_length=16)),
                ('paper_type', models.CharField(max_length=16)),
                ('section', models.CharField(max_length=1)),
                ('year', models.IntegerField()),
                ('term', models.IntegerField()),
                ('time', models.IntegerField()),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.level')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('name', models.CharField(db_column='ActivityName', max_length=40)),
                ('date_from', models.DateField(db_column='ActivityDateFrom')),
                ('date_to', models.DateField(db_column='ActivityDateTo')),
                ('topic', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.subtopic')),
                ('subtopic', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='topicsubtopicactivity_subtopicid_set', to='api.subtopic')),
            ],
            options={
                'unique_together': {('topic', 'subtopic')},
            },
        ),
    ]
