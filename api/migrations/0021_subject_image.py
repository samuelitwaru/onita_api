# Generated by Django 4.2.6 on 2024-03-18 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_delete_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='image',
            field=models.ImageField(null=True, upload_to='C:\\Users\\samuelitwaru\\Desktop\\CODE\\ONITA\\media'),
        ),
    ]
