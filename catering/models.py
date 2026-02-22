"""
Models for the Catering Application.
Handles menu categories, menu items, and booking management.
"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User, CatererProfile


class MenuCategory(models.Model):
    """
    Menu Categories for organizing menu items.
    Examples: Appetizers, Main Course, Desserts, Beverages
    """
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Menu Category'
        verbose_name_plural = 'Menu Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    Individual menu items that caterers offer.
    """
    
    # Meal type choices
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snacks', 'Snacks'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
    ]
    
    caterer = models.ForeignKey(
        CatererProfile, 
        on_delete=models.CASCADE, 
        related_name='menu_items'
    )
    category = models.ForeignKey(
        MenuCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='items'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, default='lunch')
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    preparation_time = models.IntegerField(
        default=30,
        help_text="Preparation time in minutes"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.caterer.company_name}"


class Booking(models.Model):
    """
    Customer booking for catering services.
    """
    
    # Booking status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    caterer = models.ForeignKey(
        CatererProfile, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    event_name = models.CharField(max_length=200)
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.TextField()
    number_of_guests = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)]
    )
    special_requests = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    total_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking #{self.id} - {self.customer.username} - {self.caterer.company_name}"
    
    def get_status_class(self):
        """Returns Bootstrap color class for status."""
        status_classes = {
            'pending': 'warning',
            'confirmed': 'success',
            'completed': 'info',
            'cancelled': 'danger',
        }
        return status_classes.get(self.status, 'secondary')


class BookingItem(models.Model):
    """
    Items selected in a booking.
    """
    
    booking = models.ForeignKey(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    menu_item = models.ForeignKey(
        MenuItem, 
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = 'Booking Item'
        verbose_name_plural = 'Booking Items'
    
    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Calculate subtotal before saving."""
        self.unit_price = self.menu_item.price
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class Review(models.Model):
    """
    Customer reviews for caterers.
    """
    
    booking = models.OneToOneField(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='review'
    )
    customer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    caterer = models.ForeignKey(
        CatererProfile, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review by {self.customer.username} for {self.caterer.company_name}"
