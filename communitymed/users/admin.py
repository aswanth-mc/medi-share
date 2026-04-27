from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import User



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