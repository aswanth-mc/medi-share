from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('palliative_care', 'Palliative Care'),
        ('user', 'User')
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')