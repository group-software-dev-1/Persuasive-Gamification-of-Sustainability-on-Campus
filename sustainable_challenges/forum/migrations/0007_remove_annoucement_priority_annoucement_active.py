# Generated by Django 5.0.2 on 2024-02-29 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_comment_post_date_comment_poster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annoucement',
            name='priority',
        ),
        migrations.AddField(
            model_name='annoucement',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]