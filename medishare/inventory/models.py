from django.db import models
from unit.models import PalliativeUnit
# Create your models here.




class Inventory(models.Model):

    unit = models.ForeignKey(
        PalliativeUnit,
        on_delete=models.CASCADE
    )

    medicine_name = models.CharField(max_length=255)

    quantity = models.PositiveIntegerField()

    expiry_date = models.DateField()

    medicine_image = models.ImageField(
        upload_to='inventory/'
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.medicine_name