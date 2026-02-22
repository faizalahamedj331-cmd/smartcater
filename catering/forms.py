"""
Forms for the Catering Application.
Handles menu item creation, booking, and review forms.
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import MenuItem, MenuCategory, Booking, BookingItem, Review
from accounts.models import CatererProfile


class MenuCategoryForm(forms.ModelForm):
    """
    Form for creating/editing menu categories.
    """
    
    class Meta:
        model = MenuCategory
        fields = ('name', 'description', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MenuItemForm(forms.ModelForm):
    """
    Form for creating/editing menu items.
    """
    
    class Meta:
        model = MenuItem
        fields = (
            'category', 'name', 'description', 'price', 'meal_type',
            'image', 'is_available', 'is_vegetarian', 'is_vegan',
            'is_gluten_free', 'preparation_time'
        )
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_vegetarian': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_vegan': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_gluten_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'preparation_time': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active categories
        self.fields['category'].queryset = MenuCategory.objects.filter(is_active=True)


class BookingForm(forms.ModelForm):
    """
    Form for creating bookings.
    """
    
    class Meta:
        model = Booking
        fields = (
            'event_name', 'event_date', 'event_time', 'location',
            'number_of_guests', 'special_requests'
        )
        widgets = {
            'event_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event name'
            }),
            'event_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'event_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'location': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter event location'
            }),
            'number_of_guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Number of guests'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requests or dietary requirements'
            }),
        }
    
    def clean_event_date(self):
        """Validate that event date is in the future."""
        event_date = self.cleaned_data.get('event_date')
        from datetime import date
        if event_date and event_date < date.today():
            raise ValidationError("Event date cannot be in the past.")
        return event_date


class BookingStatusForm(forms.ModelForm):
    """
    Form for updating booking status (for caterers).
    """
    
    class Meta:
        model = Booking
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class BookingItemForm(forms.ModelForm):
    """
    Form for adding items to a booking.
    """
    
    class Meta:
        model = BookingItem
        fields = ('menu_item', 'quantity')
        widgets = {
            'menu_item': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }


class ReviewForm(forms.ModelForm):
    """
    Form for submitting reviews.
    """
    
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience...'
            }),
        }
    
    def clean_rating(self):
        """Validate rating is between 1 and 5."""
        rating = self.cleaned_data.get('rating')
        if rating and (rating < 1 or rating > 5):
            raise ValidationError("Rating must be between 1 and 5.")
        return rating


class CatererSearchForm(forms.Form):
    """
    Form for searching caterers.
    """
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search caterers...'
        })
    )
    
    service_area = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by location'
        })
    )
