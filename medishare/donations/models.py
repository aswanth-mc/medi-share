from django.db import models
from django.conf import settings
from unit.models import PalliativeUnit
# Create your models here.



class Donation(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('pickup_pending', 'Pickup Pending'),
        ('collected', 'Collected'),
        ('received', 'Received'),
        ('rejected', 'Rejected'),
    )

    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    unit = models.ForeignKey(
        PalliativeUnit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    medicine_name = models.CharField(max_length=255)

    quantity = models.PositiveIntegerField()

    expiry_date = models.DateField()

    medicine_image = models.ImageField(
        upload_to='donations/'
    )

    description = models.TextField(blank=True)

    pickup_location = models.CharField(max_length=255)

    latitude = models.FloatField()

    longitude = models.FloatField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.medicine_name