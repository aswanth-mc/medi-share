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


    def __str__(self):
        return self.username


class MedicineDonation(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending Unit Review'),
        ('accepted', 'Accepted by Unit'),
        ('collected', 'Collected'),
        ('removed', 'Removed by Admin'),
    )

    donor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='medicine_donations'
    )
    unit = models.ForeignKey(
        'unit.PalliativeUnit',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medicine_donations'
    )
    medicine_name = models.CharField(max_length=255)
    medicine_image = models.ImageField(upload_to='medicine_images/')
    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField()
    pickup_location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.medicine_name} donated by {self.donor.username}'
