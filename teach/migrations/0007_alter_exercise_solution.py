# Generated by Django 5.1 on 2024-08-28 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teach", "0006_rename_level_exercise_difficulty_category_grade_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exercise",
            name="solution",
            field=models.TextField(default="", null=True),
        ),
    ]
