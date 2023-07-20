from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator
from room.models import Room


class CustomUser(AbstractUser):
    mobile_number = models.CharField(
        unique=True,
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$", message="Enter a valid mobile number."
            ),
            MinLengthValidator(10),
        ],
    )
    address = models.CharField(max_length=255, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="users")

    # method overidden
    def save(self, *args, **kwargs):
        self.mobile_number = self.mobile_number.replace(" ", "").replace("-", "")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
