from django.db import models
from django.core.validators import RegexValidator


class Floor(models.Model):
    floor_number = models.CharField(
        max_length=2,
        validators=[
            RegexValidator(
                regex=r"^[1-9]|[1-9][0-9]$", message="Enter a number from 1 to 99"
            )
        ],
    )
