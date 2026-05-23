from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = (

    ('admin', 'Admin'),

    ('user', 'User'),

    ('unit', 'Palliative Unit')

)


class User(AbstractUser):

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    location_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.username