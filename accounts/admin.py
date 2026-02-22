"""
Admin Configuration for Accounts Application.
Registers models to Django admin panel.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CatererProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom User Admin with role-based fields.
    """
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'address', 'profile_image')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone')}),
    )


@admin.register(CatererProfile)
class CatererProfileAdmin(admin.ModelAdmin):
    """
    Caterer Profile Admin.
    """
    list_display = ('company_name', 'user', 'is_verified', 'rating', 'total_bookings')
    list_filter = ('is_verified',)
    search_fields = ('company_name', 'user__username', 'license_number')
    list_editable = ('is_verified',)
    raw_id_fields = ('user',)
