from django.contrib import admin
from .models import MedicineDonation, UnitInventory

# Register your models here.
admin.site.register(MedicineDonation)
admin.site.register(UnitInventory)