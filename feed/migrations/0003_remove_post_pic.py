# Generated by Django 3.2.3 on 2021-06-20 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='pic',
        ),
    ]
