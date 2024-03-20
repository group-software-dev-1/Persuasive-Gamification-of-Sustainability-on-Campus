# Generated by Django 5.0.2 on 2024-02-29 07:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_remove_annoucement_priority_annoucement_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='linked_announcement',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.annoucement'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='linked_post',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.suggestion'),
        ),
    ]
