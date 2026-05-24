from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import MedicineDonation, MedicineRequest, User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role')



class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm

    list_display = ('username', 'email', 'role')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Role Info', {'fields': ('role',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )



admin.site.register(User, CustomUserAdmin)

@admin.register(MedicineDonation)
class MedicineDonationAdmin(admin.ModelAdmin):
    list_display = (
        'medicine_name',
        'donor',
        'unit',
        'quantity',
        'expiry_date',
        'status',
        'created_at',
    )
    list_filter = ('status', 'expiry_date', 'created_at')
    search_fields = ('medicine_name', 'donor__username', 'donor__email')


@admin.register(MedicineRequest)
class MedicineRequestAdmin(admin.ModelAdmin):
    list_display = (
        'donation',
        'requester',
        'unit',
        'status',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'donation__medicine_name',
        'requester__username',
        'unit__name',
    )