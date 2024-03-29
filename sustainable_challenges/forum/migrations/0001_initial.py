# Generated by Django 5.0.1 on 2024-03-21 10:34

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
                ('post_name', models.CharField(max_length=100, verbose_name='Post Name')),
                ('post_text', models.CharField(max_length=400, verbose_name='Post Text')),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Posted')),
                ('active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('poster', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Poster')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_name', models.CharField(max_length=100, verbose_name='Post Name')),
                ('post_text', models.CharField(max_length=400, verbose_name='Post Text')),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Posted')),
                ('poster', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Poster')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=400, verbose_name='Comment Text')),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Posted')),
                ('linked_announcement', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.annoucement', verbose_name='Announcement')),
                ('poster', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Poster')),
                ('linked_post', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.suggestion', verbose_name='Suggestion')),
            ],
        ),
    ]
