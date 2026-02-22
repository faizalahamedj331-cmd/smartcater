"""
Forms for the Accounts Application.
Handles user registration, login, and profile editing.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import User, CatererProfile


class UserRegistrationForm(UserCreationForm):
    """
    User Registration Form with role selection.
    """
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )
    
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'role', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})
    
    def clean_email(self):
        """Validate email uniqueness."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists!")
        return email
    
    def save(self, commit=True):
        """Save user with hashed password."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.phone = self.cleaned_data.get('phone', '')
        
        if commit:
            user.save()
            
            # Create caterer profile if role is caterer
            if user.role == 'caterer':
                CatererProfile.objects.create(
                    user=user,
                    company_name=f"{user.username}'s Catering"
                )
        
        return user


class UserLoginForm(AuthenticationForm):
    """
    User Login Form with styling.
    """
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile.
    """
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'profile_image')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CatererProfileForm(forms.ModelForm):
    """
    Form for editing caterer profile.
    """
    
    class Meta:
        model = CatererProfile
        fields = ('company_name', 'description', 'license_number', 'service_area')
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'service_area': forms.TextInput(attrs={'class': 'form-control'}),
        }
