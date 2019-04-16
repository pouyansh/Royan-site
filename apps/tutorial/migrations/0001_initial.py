# Generated by Django 2.1.7 on 2019-04-16 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='')),
                ('summary', models.TextField(max_length=1000, verbose_name='')),
                ('paper', models.FileField(upload_to='', verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='نام توتوریال')),
                ('description', models.TextField(max_length=1000, verbose_name='توضیحات')),
            ],
        ),
        migrations.AddField(
            model_name='paper',
            name='tutorial',
            field=models.ForeignKey(on_delete='Restrict', to='tutorial.Tutorial', verbose_name=''),
        ),
    ]