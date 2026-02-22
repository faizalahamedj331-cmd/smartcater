"""
Views for the Catering Application.
Handles menu browsing, booking, and catering management views.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count, Sum, Avg
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import date, datetime
from .models import MenuItem, MenuCategory, Booking, BookingItem, Review
from .forms import (
    MenuItemForm, MenuCategoryForm, BookingForm, 
    BookingStatusForm, BookingItemForm, ReviewForm, CatererSearchForm
)
from accounts.models import CatererProfile, User


def home(request):
    """
    Home page view.
    Displays featured caterers and welcome message.
    """
    # Get featured caterers (verified ones with bookings)
    featured_caterers = CatererProfile.objects.filter(
        is_verified=True
    ).order_by('-total_bookings')[:6]
    
    # Get all active menu categories
    categories = MenuCategory.objects.filter(is_active=True)
    
    # Statistics for the dashboard
    total_caterers = CatererProfile.objects.count()
    total_bookings = Booking.objects.count()
    
    context = {
        'featured_caterers': featured_caterers,
        'categories': categories,
        'total_caterers': total_caterers,
        'total_bookings': total_bookings,
    }
    
    return render(request, 'catering/home.html', context)


def caterer_list(request):
    """
    View to list all caterers.
    Allows filtering by search and service area.
    """
    caterers = CatererProfile.objects.filter(
        user__is_active=True
    ).select_related('user')
    
    search_query = request.GET.get('search', '')
    area_query = request.GET.get('area', '')
    
    if search_query:
        caterers = caterers.filter(
            Q(company_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if area_query:
        caterers = caterers.filter(service_area__icontains=area_query)
    
    context = {
        'caterers': caterers,
        'search_query': search_query,
        'area_query': area_query,
    }
    
    return render(request, 'catering/caterer_list.html', context)


def caterer_detail(request, caterer_id):
    """
    View to display caterer details and menu.
    """
    caterer = get_object_or_404(
        CatererProfile.objects.select_related('user'),
        id=caterer_id
    )
    
    # Get menu items grouped by category
    menu_items = MenuItem.objects.filter(
        caterer=caterer,
        is_available=True
    ).select_related('category')
    
    # Group by meal type
    menu_by_meal = {}
    for item in menu_items:
        if item.meal_type not in menu_by_meal:
            menu_by_meal[item.meal_type] = []
        menu_by_meal[item.meal_type].append(item)
    
    # Get reviews
    reviews = Review.objects.filter(caterer=caterer).select_related('customer')[:5]
    
    # Calculate average rating
    avg_rating = Review.objects.filter(caterer=caterer).aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'caterer': caterer,
        'menu_by_meal': menu_by_meal,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    
    return render(request, 'catering/caterer_detail.html', context)


@login_required
def create_booking(request, caterer_id):
    """
    View to create a new booking.
    """
    if not request.user.is_customer:
        messages.error(request, "Only customers can make bookings.")
        return redirect('home')
    
    caterer = get_object_or_404(CatererProfile, id=caterer_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.caterer = caterer
            booking.save()
            
            # Redirect to menu selection
            return redirect('select_menu', booking_id=booking.id)
    else:
        form = BookingForm()
    
    context = {
        'form': form,
        'caterer': caterer,
    }
    
    return render(request, 'catering/create_booking.html', context)


@login_required
def select_menu(request, booking_id):
    """
    View to select menu items for a booking.
    """
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    # Check if booking is still pending
    if booking.status != 'pending':
        messages.error(request, "This booking cannot be modified.")
        return redirect('my_bookings')
    
    # Get caterer's available menu items
    menu_items = MenuItem.objects.filter(
        caterer=booking.caterer,
        is_available=True
    ).select_related('category')
    
    # Get already selected items
    selected_items = BookingItem.objects.filter(booking=booking).select_related('menu_item')
    
    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if menu_item_id:
            menu_item = get_object_or_404(MenuItem, id=menu_item_id, caterer=booking.caterer)
            
            # Check if item already in booking
            existing_item = BookingItem.objects.filter(
                booking=booking,
                menu_item=menu_item
            ).first()
            
            if existing_item:
                existing_item.quantity += quantity
                existing_item.save()
            else:
                BookingItem.objects.create(
                    booking=booking,
                    menu_item=menu_item,
                    quantity=quantity
                )
            
            messages.success(request, f"Added {menu_item.name} to your booking.")
    
    # Calculate total
    total = sum(item.subtotal for item in selected_items)
    booking.total_amount = total
    booking.save()
    
    context = {
        'booking': booking,
        'menu_items': menu_items,
        'selected_items': selected_items,
        'total': total,
    }
    
    return render(request, 'catering/select_menu.html', context)


@login_required
def remove_booking_item(request, item_id):
    """
    View to remove an item from booking.
    """
    item = get_object_or_404(BookingItem, id=item_id)
    booking = item.booking
    
    # Verify ownership
    if booking.customer != request.user:
        messages.error(request, "You don't have permission to remove this item.")
        return redirect('my_bookings')
    
    if booking.status != 'pending':
        messages.error(request, "This booking cannot be modified.")
        return redirect('my_bookings')
    
    item.delete()
    
    # Recalculate total
    total = sum(i.subtotal for i in BookingItem.objects.filter(booking=booking))
    booking.total_amount = total
    booking.save()
    
    messages.success(request, "Item removed from booking.")
    return redirect('select_menu', booking_id=booking.id)


@login_required
def confirm_booking(request, booking_id):
    """
    View to confirm and finalize a booking.
    """
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if booking.status != 'pending':
        messages.error(request, "This booking cannot be confirmed.")
        return redirect('my_bookings')
    
    # Check if at least one item selected
    if not BookingItem.objects.filter(booking=booking).exists():
        messages.error(request, "Please select at least one menu item.")
        return redirect('select_menu', booking_id=booking.id)
    
    # Calculate total based on number of guests
    # This is a simple calculation - can be customized
    total = booking.total_amount * booking.number_of_guests
    booking.total_amount = total
    booking.save()
    
    messages.success(request, "Booking confirmed successfully!")
    return redirect('booking_confirmation', booking_id=booking.id)


@login_required
def booking_confirmation(request, booking_id):
    """
    View to display booking confirmation.
    """
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    items = BookingItem.objects.filter(booking=booking).select_related('menu_item')
    
    context = {
        'booking': booking,
        'items': items,
    }
    
    return render(request, 'catering/booking_confirmation.html', context)


@login_required
def my_bookings(request):
    """
    View to display customer's bookings.
    """
    if not request.user.is_customer:
        messages.error(request, "Access denied.")
        return redirect('home')
    
    bookings = Booking.objects.filter(
        customer=request.user
    ).select_related('caterer').prefetch_related('items')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
    }
    
    return render(request, 'catering/my_bookings.html', context)


# ==================== CATERER VIEWS ====================

@login_required
def caterer_dashboard(request):
    """
    Dashboard view for caterers.
    Displays booking statistics and recent orders.
    """
    if not request.user.is_caterer:
        messages.error(request, "Access denied. Only caterers can access this page.")
        return redirect('home')
    
    try:
        caterer_profile = request.user.caterer_profile
    except CatererProfile.DoesNotExist:
        messages.error(request, "Please complete your caterer profile first.")
        return redirect('caterer_profile_edit')
    
    # Get all bookings for this caterer
    bookings = Booking.objects.filter(
        caterer=caterer_profile
    ).select_related('customer')
    
    # Statistics
    pending_bookings = bookings.filter(status='pending').count()
    confirmed_bookings = bookings.filter(status='confirmed').count()
    completed_bookings = bookings.filter(status='completed').count()
    total_revenue = bookings.filter(status='completed').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Recent bookings
    recent_bookings = bookings.order_by('-created_at')[:10]
    
    context = {
        'caterer_profile': caterer_profile,
        'bookings': bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
    }
    
    return render(request, 'catering/caterer_dashboard.html', context)


@login_required
def caterer_menu(request):
    """
    View to manage menu items for caterers.
    """
    if not request.user.is_caterer:
        messages.error(request, "Access denied.")
        return redirect('home')
    
    try:
        caterer_profile = request.user.caterer_profile
    except CatererProfile.DoesNotExist:
        return redirect('caterer_profile_edit')
    
    menu_items = MenuItem.objects.filter(
        caterer=caterer_profile
    ).select_related('category').order_by('-created_at')
    
    # Filter by availability
    availability_filter = request.GET.get('availability')
    if availability_filter == 'available':
        menu_items = menu_items.filter(is_available=True)
    elif availability_filter == 'unavailable':
        menu_items = menu_items.filter(is_available=False)
    
    context = {
        'menu_items': menu_items,
        'caterer_profile': caterer_profile,
        'availability_filter': availability_filter,
    }
    
    return render(request, 'catering/caterer_menu.html', context)


@login_required
def add_menu_item(request):
    """
    View to add a new menu item.
    """
    if not request.user.is_caterer:
        messages.error(request, "Access denied.")
        return redirect('home')
    
    try:
        caterer_profile = request.user.caterer_profile
    except CatererProfile.DoesNotExist:
        return redirect('caterer_profile_edit')
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.caterer = caterer_profile
            menu_item.save()
            messages.success(request, f"Menu item '{menu_item.name}' added successfully!")
            return redirect('caterer_menu')
    else:
        form = MenuItemForm()
    
    context = {
        'form': form,
        'caterer_profile': caterer_profile,
    }
    
    return render(request, 'catering/add_menu_item.html', context)


@login_required
def edit_menu_item(request, item_id):
    """
    View to edit a menu item.
    """
    if not request.user.is_caterer:
        messages.error(request, "Access denied.")
        return redirect('home')
    
    menu_item = get_object_or_404(MenuItem, id=item_id)
    
    # Verify ownership
    if menu_item.caterer != request.user.caterer_profile:
        messages.error(request, "You don't have permission to edit this item.")
        return redirect('caterer_menu')
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item updated successfully!")
            return redirect('caterer_menu')
    else:
        form = MenuItemForm(instance=menu_item)
    
    context = {
        'form': form,
        'menu_item': menu_item,
    }
    
    return render(request, 'catering/edit_menu_item.html', context)


@login_required
def delete_menu_item(request, item_id):
    """
    View to delete a menu item.
    """
    if not request.user.is_caterer:
        messages.error(request, "Access denied.")
        return redirect('home')
    
    menu_item = get_object_or_404(MenuItem, id=item_id)
    
    # Verify ownership
    if menu_item.caterer != request.user.caterer_profile:
        messages.error(request, "You don't have permission to delete this item.")
        return redirect('caterer_menu')
    
    if request.method == 'POST':
        menu_item.delete()
        messages.success(request, "Menu item deleted successfully!")
        return redirect('caterer_menu')
    
    return render(request, 'catering/delete_menu_item.html', {'menu_item': menu_item})


@login_required
def manage_categories(request):
    """
    View to manage menu categories.
    """
    if not request.user.is_caterer:
        messages.error(request, "Access denied.")
        return redirect('home')
    
    categories = MenuCategory.objects.all()
    
    return render(request, 'catering/manage_categories.html', {'categories': categories})


@login_required
def add_category(request):
    """
    View to add a new category.
    """
    if not request.user.is_caterer:
        messages.error(request, "Access denied.")
        return redirect('home')
    
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('manage_categories')
    else:
        form = MenuCategoryForm()
    
    return render(request, 'catering/add_category.html', {'form': form})


@login_required
def catering_bookings(request):
    """
    View to manage bookings for caterers.
    """
    if not request.user.is_caterer:
        messages.error(request, "Access denied.")
        return redirect('home')
    
    try:
        caterer_profile = request.user.caterer_profile
    except CatererProfile.DoesNotExist:
        return redirect('caterer_profile_edit')
    
    bookings = Booking.objects.filter(
        caterer=caterer_profile
    ).select_related('customer').prefetch_related('items')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
    }
    
    return render(request, 'catering/catering_bookings.html', context)


@login_required
def update_booking_status(request, booking_id):
    """
    View to update booking status.
    """
    if not request.user.is_caterer:
        messages.error(request, "Access denied.")
        return redirect('home')
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Verify ownership
    if booking.caterer != request.user.caterer_profile:
        messages.error(request, "You don't have permission to update this booking.")
        return redirect('catering_bookings')
    
    if request.method == 'POST':
        form = BookingStatusForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save()
            
            # Update caterer total bookings if confirmed or completed
            if booking.status in ['confirmed', 'completed']:
                caterer = request.user.caterer_profile
                caterer.total_bookings = Booking.objects.filter(
                    caterer=caterer,
                    status__in=['confirmed', 'completed']
                ).count()
                caterer.save()
            
            messages.success(request, f"Booking status updated to {booking.get_status_display()}!")
            return redirect('catering_bookings')
    else:
        form = BookingStatusForm(instance=booking)
    
    context = {
        'form': form,
        'booking': booking,
    }
    
    return render(request, 'catering/update_booking_status.html', context)


@login_required
def booking_detail(request, booking_id):
    """
    View to display booking details.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check permission
    if not (
        request.user.is_admin_user or
        (request.user.is_customer and booking.customer == request.user) or
        (request.user.is_caterer and booking.caterer == request.user.caterer_profile)
    ):
        messages.error(request, "You don't have permission to view this booking.")
        return redirect('home')
    
    items = BookingItem.objects.filter(booking=booking).select_related('menu_item')
    
    context = {
        'booking': booking,
        'items': items,
    }
    
    return render(request, 'catering/booking_detail.html', context)


@login_required
def cancel_booking(request, booking_id):
    """
    View to cancel a booking.
    """
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if booking.status != 'pending':
        messages.error(request, "Only pending bookings can be cancelled.")
        return redirect('my_bookings')
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Booking cancelled successfully!")
        return redirect('my_bookings')
    
    return render(request, 'catering/cancel_booking.html', {'booking': booking})


@login_required
def submit_review(request, booking_id):
    """
    View to submit a review for a completed booking.
    """
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    # Only allow reviews for completed bookings
    if booking.status != 'completed':
        messages.error(request, "You can only review completed bookings.")
        return redirect('my_bookings')
    
    # Check if already reviewed
    if hasattr(booking, 'review'):
        messages.error(request, "You have already reviewed this booking.")
        return redirect('my_bookings')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.customer = request.user
            review.caterer = booking.caterer
            review.save()
            
            # Update caterer rating
            avg_rating = Review.objects.filter(
                caterer=booking.caterer
            ).aggregate(Avg('rating'))['rating__avg']
            booking.caterer.rating = avg_rating or 0
            booking.caterer.save()
            
            messages.success(request, "Thank you for your review!")
            return redirect('my_bookings')
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'booking': booking,
    }
    
    return render(request, 'catering/submit_review.html', context)


# ==================== ADMIN VIEWS ====================

@login_required
def admin_dashboard(request):
    """
    Admin dashboard with statistics.
    """
    if not request.user.is_admin_user:
        messages.error(request, "Access denied.")
        return redirect('home')
    
    # Statistics
    total_users = User.objects.count()
    total_customers = User.objects.filter(role='customer').count()
    total_caterers = CatererProfile.objects.count()
    total_bookings = Booking.objects.count()
    
    # Revenue from completed bookings
    total_revenue = Booking.objects.filter(
        status='completed'
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Recent bookings
    recent_bookings = Booking.objects.order_by('-created_at')[:10]
    
    # Bookings by status
    bookings_by_status = Booking.objects.values('status').annotate(count=Count('id'))
    
    context = {
        'total_users': total_users,
        'total_customers': total_customers,
        'total_caterers': total_caterers,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'bookings_by_status': bookings_by_status,
    }
    
    return render(request, 'catering/admin_dashboard.html', context)


def about(request):
    """About page view."""
    return render(request, 'catering/about.html')


def contact(request):
    """Contact page view."""
    return render(request, 'catering/contact.html')
