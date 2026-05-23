from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('unit', 'Palliative Unit'),
    )

    role = models.CharField( max_length=10,choices=ROLE_CHOICES,default='user')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    location_name = models.CharField(max_length=255,blank=True,null=True)
    latitude = models.FloatField(blank=True,null=True)
    longitude = models.FloatField(blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username