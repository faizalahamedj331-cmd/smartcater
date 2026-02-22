"""
Views for the Accounts Application.
Handles user authentication, registration, and profile management.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, CatererProfileForm
from .models import User, CatererProfile
from catering.models import Booking


def user_login(request):
    """
    User login view.
    Authenticates user and redirects based on role.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                
                # Redirect based on user role
                if user.is_caterer():
                    return redirect('caterer_dashboard')
                elif user.is_admin_user():
                    return redirect('admin:index')
                else:
                    return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def user_register(request):
    """
    User registration view.
    Creates new user with selected role.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to SmartCater!")
            
            if user.role == 'caterer':
                return redirect('caterer_profile_edit')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_logout(request):
    """
    User logout view.
    Logs out user and redirects to home.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def profile_view(request):
    """
    User profile view.
    Displays user information and booking history for customers.
    """
    user = request.user
    bookings = []
    
    if user.is_customer():
        bookings = Booking.objects.filter(customer=user).order_by('-created_at')
    elif user.is_caterer():
        try:
            caterer_profile = user.caterer_profile
        except CatererProfile.DoesNotExist:
            caterer_profile = None
    
    context = {
        'user': user,
        'bookings': bookings,
    }
    
    if user.is_caterer():
        context['caterer_profile'] = caterer_profile
    
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit(request):
    """
    User profile edit view.
    Allows users to update their profile information.
    """
    user = request.user
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def caterer_profile_edit(request):
    """
    Caterer profile edit view.
    Allows caterers to update their business information.
    """
    if not request.user.is_caterer():
        messages.error(request, "Access denied. Only caterers can access this page.")
        return redirect('home')
    
    try:
        caterer_profile = request.user.caterer_profile
    except CatererProfile.DoesNotExist:
        caterer_profile = CatererProfile.objects.create(
            user=request.user,
            company_name=f"{request.user.username}'s Catering"
        )
    
    if request.method == 'POST':
        form = CatererProfileForm(request.POST, instance=caterer_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Caterer profile updated successfully!")
            return redirect('caterer_dashboard')
    else:
        form = CatererProfileForm(instance=caterer_profile)
    
    return render(request, 'accounts/caterer_profile_edit.html', {'form': form})
