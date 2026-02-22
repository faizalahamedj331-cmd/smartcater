"""
Models for the Accounts Application.
Handles user profiles and role-based access control.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User Model extending Django's AbstractUser.
    Adds role-based access control for Customer, Caterer, and Admin.
    """
    
    # Role choices for user types
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('caterer', 'Caterer'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.png', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_customer(self):
        """Check if user is a customer."""
        return self.role == 'customer'
    
    def is_caterer(self):
        """Check if user is a caterer."""
        return self.role == 'caterer'
    
    def is_admin_user(self):
        """Check if user is an admin."""
        return self.role == 'admin' or self.is_superuser


class CatererProfile(models.Model):
    """
    Extended profile information for caterers.
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='caterer_profile')
    company_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    service_area = models.CharField(max_length=200, blank=True)
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_bookings = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Caterer Profile'
        verbose_name_plural = 'Caterer Profiles'
    
    def __str__(self):
        return f"{self.company_name} - {self.user.username}"
