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

    # Add them here to see them in the admin table view
    list_display = ('username', 'email', 'full_name', 'blood_group', 'role')
    list_filter = ('role', 'blood_group')
    search_fields = ('username', 'email', 'full_name')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'full_name', 'blood_group')}),
        ('Role Info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'full_name', 'blood_group', 'password1', 'password2'),
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