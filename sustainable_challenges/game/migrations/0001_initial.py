# Generated by Django 5.0.2 on 2024-02-29 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, unique=True)),
                ('points', models.IntegerField(default='0')),
                ('description', models.CharField(max_length=240)),
            ],
        ),
    ]
