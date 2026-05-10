from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class MedicineDonation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('collected', 'Collected')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    expiry_date = models.DateField()
    image = models.ImageField(upload_to='medicine_images/')
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.medicine_name
    
class UnitInventory(models.Model):
    unit = models.ForeignKey(User, on_delete=models.CASCADE)  # role = unit
    donation = models.ForeignKey(MedicineDonation, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=50)
    expiry_date = models.DateField()
    added_at = models.DateTimeField(auto_now_add=True)