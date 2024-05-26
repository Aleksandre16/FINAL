from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Define a custom UserAdmin
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'full_name', 'personal_number', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_user', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'personal_number', 'date_of_birth', 'password1', 'password2'),
        }),
    )
    list_display = (
    'username', 'email', 'full_name', 'personal_number', 'date_of_birth', 'is_staff', 'is_superuser', 'is_user')
    search_fields = ('username', 'email', 'full_name', 'personal_number')
    ordering = ('username',)


# Register the User model with the custom admin
admin.site.register(User, CustomUserAdmin)
