"""
URL Configuration for Catering Application.
Maps all catering-related URLs to views.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Caterer URLs
    path('caterers/', views.caterer_list, name='caterer_list'),
    path('caterer/<int:caterer_id>/', views.caterer_detail, name='caterer_detail'),
    
    # Booking URLs (Customer)
    path('booking/create/<int:caterer_id>/', views.create_booking, name='create_booking'),
    path('booking/<int:booking_id>/select-menu/', views.select_menu, name='select_menu'),
    path('booking/item/<int:item_id>/remove/', views.remove_booking_item, name='remove_booking_item'),
    path('booking/<int:booking_id>/confirm/', views.confirm_booking, name='confirm_booking'),
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('booking/<int:booking_id>/review/', views.submit_review, name='submit_review'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    
    # Caterer Dashboard URLs
    path('caterer/dashboard/', views.caterer_dashboard, name='caterer_dashboard'),
    path('caterer/menu/', views.caterer_menu, name='caterer_menu'),
    path('caterer/menu/add/', views.add_menu_item, name='add_menu_item'),
    path('caterer/menu/<int:item_id>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('caterer/menu/<int:item_id>/delete/', views.delete_menu_item, name='delete_menu_item'),
    path('caterer/categories/', views.manage_categories, name='manage_categories'),
    path('caterer/category/add/', views.add_category, name='add_category'),
    path('caterer/bookings/', views.catering_bookings, name='catering_bookings'),
    path('caterer/booking/<int:booking_id>/status/', views.update_booking_status, name='update_booking_status'),
    
    # Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
