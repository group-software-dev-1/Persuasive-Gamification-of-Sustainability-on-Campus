# Generated by Django 5.0.2 on 2024-03-15 17:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("poi", "0002_placeofinterest_title_alter_placeofinterest_desc_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="placeofinterest",
            name="title",
            field=models.CharField(max_length=100, verbose_name="Title"),
        ),
    ]