# Generated by Django 4.2.3 on 2023-07-17 13:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Floor",
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
                (
                    "floor_number",
                    models.CharField(
                        max_length=2,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Enter a number from 1 to 99",
                                regex="^[1-9]|[1-9][0-9]$",
                            )
                        ],
                    ),
                ),
            ],
        ),
    ]
