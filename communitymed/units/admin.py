from django.contrib import admin
from users.models import MedicineRequest
from units.models import PalliativeUnit


# Register your models here.
admin.site.register(MedicineRequest)
admin.site.register(PalliativeUnit)
