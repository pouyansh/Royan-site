# Generated by Django 2.1.7 on 2019-05-01 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete='DoNothing', related_name='parent_message', to='message.Message', verbose_name=''),
        ),
    ]
