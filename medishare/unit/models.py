from django.db import models
from django.conf import settings
# Create your models here.

class PalliativeUnit(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location_name = models.CharField(max_length=255)
    latitude = models.FloatField(
        null=True,
        blank=True
    )
    longitude = models.FloatField(
        null=True,
        blank=True
    )
    license_number = models.CharField(max_length=100)
    license_file = models.FileField(
        upload_to='licenses/'
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name