# Generated by Django 5.1 on 2024-08-28 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teach", "0004_rename_excercise_exercise_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name="exercise",
            name="level",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="exercise",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="teach.category"
            ),
        ),
    ]
