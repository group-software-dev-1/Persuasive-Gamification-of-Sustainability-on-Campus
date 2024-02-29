# Generated by Django 5.0.2 on 2024-02-29 00:17

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Annoucement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_name', models.CharField(max_length=100)),
                ('post_text', models.CharField(max_length=200)),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('priority', models.BooleanField(default=False)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Suggestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_name', models.CharField(max_length=100)),
                ('post_text', models.CharField(max_length=200)),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('endorsements', models.IntegerField(default=0)),
                ('linked_announced', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='forum.annoucement')),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=400)),
                ('endorsements', models.IntegerField(default=0)),
                ('linked_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.suggestions')),
            ],
        ),
    ]
