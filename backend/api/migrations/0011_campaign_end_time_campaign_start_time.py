# Generated by Django 5.0.6 on 2025-01-14 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0010_remove_keyword_keyword_keyword_file_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaign",
            name="end_time",
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name="campaign",
            name="start_time",
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
