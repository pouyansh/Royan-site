# Generated by Django 2.1.7 on 2019-04-30 23:59

from django.conf import settings
from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('text', models.TextField(max_length=2000, verbose_name='متن')),
                ('date', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ')),
                ('is_opened', models.BooleanField(default=False, verbose_name='وضعیت مشاهده')),
                ('Receiver', models.ForeignKey(on_delete='Cascade', related_name='receiver', to=settings.AUTH_USER_MODEL, verbose_name='گیرنده')),
                ('Sender', models.ForeignKey(on_delete='Cascade', related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='فرستنده')),
            ],
        ),
    ]
