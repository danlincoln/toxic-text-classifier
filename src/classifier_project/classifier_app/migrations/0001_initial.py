# Generated by Django 5.0.3 on 2024-03-18 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HumanRating",
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
                ("rating", models.BooleanField()),
                ("raw_rating", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Text",
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
                ("unprocessed", models.TextField()),
                ("processed", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="HumanRatingClass",
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
                ("severe_toxicity", models.FloatField()),
                ("obscene", models.FloatField()),
                ("threat", models.FloatField()),
                ("insult", models.FloatField()),
                ("identity_attack", models.FloatField()),
                ("sexual_explicit", models.FloatField()),
                (
                    "human_rating",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classifier_app.humanrating",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MachineRating",
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
                ("rating", models.BooleanField()),
                (
                    "text",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="classifier_app.text",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="humanrating",
            name="text",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="classifier_app.text"
            ),
        ),
    ]
