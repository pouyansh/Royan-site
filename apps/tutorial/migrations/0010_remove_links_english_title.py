# Generated by Django 2.1.7 on 2019-09-02 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0009_auto_20190902_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='links',
            name='english_title',
        ),
    ]
