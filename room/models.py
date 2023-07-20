from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from floor.models import Floor


class Room(models.Model):
    room_number = models.CharField(
        max_length=2,
        null=False,
        blank=False,
        validators=[
            RegexValidator(
                regex=r"^[1-9]|[1-9][0-9]$", message="Enter a number from 1 to 99"
            )
        ],
    )
    capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, blank=False
    )
    price = models.IntegerField(null=False, blank=False)
    floor = models.ForeignKey(
        Floor, on_delete=models.CASCADE, null=False, related_name="rooms"
    )
