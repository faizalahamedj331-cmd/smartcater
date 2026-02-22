"""
Admin Configuration for Catering Application.
Registers models to Django admin panel.
"""

from django.contrib import admin
from .models import MenuCategory, MenuItem, Booking, BookingItem, Review


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    """
    Menu Category Admin.
    """
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('is_active',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    Menu Item Admin.
    """
    list_display = ('name', 'caterer', 'category', 'price', 'meal_type', 'is_available')
    list_filter = ('is_available', 'meal_type', 'category', 'is_vegetarian', 'is_vegan', 'is_gluten_free')
    search_fields = ('name', 'description', 'caterer__company_name')
    list_editable = ('is_available',)
    raw_id_fields = ('caterer',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Booking Admin.
    """
    list_display = ('id', 'customer', 'caterer', 'event_name', 'event_date', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'event_date', 'created_at')
    search_fields = ('event_name', 'customer__username', 'caterer__company_name')
    list_editable = ('status',)
    raw_id_fields = ('customer', 'caterer')
    date_hierarchy = 'event_date'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BookingItem)
class BookingItemAdmin(admin.ModelAdmin):
    """
    Booking Item Admin.
    """
    list_display = ('booking', 'menu_item', 'quantity', 'unit_price', 'subtotal')
    search_fields = ('booking__id', 'menu_item__name')
    raw_id_fields = ('booking', 'menu_item')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Review Admin.
    """
    list_display = ('customer', 'caterer', 'rating', 'booking', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('customer__username', 'caterer__company_name', 'comment')
    raw_id_fields = ('booking', 'customer', 'caterer')
