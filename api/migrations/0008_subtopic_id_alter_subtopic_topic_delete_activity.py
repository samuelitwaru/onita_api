# Generated by Django 4.2.6 on 2023-11-09 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_topic_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtopic',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subtopic',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.topic'),
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
    ]
