# Generated by Django 5.0.6 on 2025-01-14 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0012_proximity_proximity_store_weather_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="campaign",
            name="target_demographics",
        ),
        migrations.RemoveField(
            model_name="campaign",
            name="topics",
        ),
        migrations.AddField(
            model_name="campaign",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
