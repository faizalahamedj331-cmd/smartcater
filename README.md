# SmartCater - Catering Management System

A full-featured catering management system built with Django, Bootstrap 5, and MySQL.

## Features

### Customer Features
- User Registration and Login
- Browse Available Caterers
- View Caterer Profiles and Menus
- Create Bookings with Event Details
- Select Menu Items
- Track Booking Status
- View Booking History

### Caterer Features
- Business Profile Management
- Menu Item Management (CRUD)
- View Incoming Bookings
- Update Booking Status (Pending/Confirmed/Completed/Cancelled)
- Dashboard with Statistics

### Admin Features
- Django Admin Panel
- User Management
- Caterer Management
- Monitor All Bookings
- Analytics Dashboard

## Tech Stack

- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Backend**: Python, Django Framework
- **Database**: MySQL
- **Authentication**: Django Built-in Auth System

## Project Structure

```
smartcater/
├── manage.py
├── smartcater/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/accounts/
├── catering/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/catering/
├── templates/
│   ├── base.html
│   └── home.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
└── requirements.txt
```

## Database Configuration

The project is configured to use MySQL with the following credentials:

- **Database Name**: smartcater
- **Username**: root
- **Password**: 123456
- **Host**: 127.0.0.1
- **Port**: 3306

## Setup Instructions

### Step 1: Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

### Step 2: Create Virtual Environment

```
bash
# Navigate to project directory
cd smartcater

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```
bash
pip install -r requirements.txt
```

### Step 4: Create MySQL Database

Open MySQL and create the database:

```
sql
CREATE DATABASE smartcater CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 5: Run Migrations

```
bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser

```
bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### Step 7: Run Development Server

```
bash
python manage.py runserver
```

### Step 8: Access the Application

Open your browser and navigate to:
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## User Roles

1. **Customer**: Can browse caterers, view menus, and create bookings
2. **Caterer**: Can manage menu items and respond to bookings
3. **Admin**: Full access to Django admin panel for system management

## Booking Status Flow

```
Pending → Confirmed → Completed
    ↓
  Cancelled
```

## Models Overview

### User (Extended Django User)
- role (customer/caterer/admin)
- phone
- address
- profile_image
- created_at

### CatererProfile
- user (OneToOne)
- company_name
- description
- license_number
- service_area
- is_verified

### MenuCategory
- name
- description

### MenuItem
- caterer (ForeignKey)
- category (ForeignKey)
- name
- description
- price
- meal_type
- is_vegetarian
- is_vegan
- is_available

### Booking
- customer (ForeignKey)
- caterer (ForeignKey)
- event_name
- event_date
- event_time
- location
- number_of_guests
- total_amount
- status
- special_requests

### BookingItem
- booking (ForeignKey)
- menu_item (ForeignKey)
- quantity
- unit_price
- subtotal

## Security Features

- CSRF Protection
- Password Hashing (Django built-in)
- Role-based Access Control
- Login Required Decorators
- Session Management

## License

This project is for educational purposes.

## Author

SmartCater Development Team
