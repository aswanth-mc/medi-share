from django.db import models
from django.conf import settings
# Create your models here.

class PalliativeUnit(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    location=models.CharField(max_length=255)
    license_number = models.CharField(max_length=100)
    license_file = models.FileField(upload_to='licenses/')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)