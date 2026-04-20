# Cafe Management System - REST API Documentation

## Overview
This document provides comprehensive documentation for the Cafe Management System REST API built with Django REST Framework.

---

## Table of Contents
1. [Setup Instructions](#setup-instructions)
2. [API Base URL](#api-base-url)
3. [Authentication](#authentication)
4. [API Endpoints](#api-endpoints)
5. [Postman Collection](#postman-collection)
6. [Response Formats](#response-formats)
7. [Error Handling](#error-handling)

---

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

---

## API Base URL
```
http://localhost:8000/api/
```

---

## Authentication

### JWT Token-Based Authentication

The API uses JWT (JSON Web Token) for authentication.

#### Step 1: Obtain JWT Token
**Endpoint:** `POST /api/token/`

**Request:**
```json
{
    "username": "testuser",
    "password": "testpass123"
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Step 2: Use JWT Token in Requests
Add the token to the Authorization header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

#### Step 3: Refresh Token
**Endpoint:** `POST /api/token/refresh/`

**Request:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## API Endpoints

### 1. Authentication Endpoints

#### 1.1 User Registration
**Endpoint:** `POST /api/auth/register/`

**Permission:** Public (AllowAny)

**Request:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

**Error Response (400 Bad Request):**
```json
{
    "username": ["Username already exists."],
    "email": ["Email already registered."],
    "password": ["Passwords don't match."]
}
```

---

#### 1.2 User Login
**Endpoint:** `POST /api/auth/login/`

**Permission:** Public (AllowAny)

**Request:**
```json
{
    "username": "john_doe",
    "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
    "message": "Login successful",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_staff": false,
        "is_superuser": false,
        "date_joined": "2024-04-19T10:30:00Z"
    }
}
```

---

#### 1.3 User Logout
**Endpoint:** `POST /api/auth/logout/`

**Permission:** IsAuthenticated

**Request:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
    "message": "Logout successful"
}
```

---

#### 1.4 Get User Profile
**Endpoint:** `GET /api/auth/profile/`

**Permission:** IsAuthenticated

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_staff": false,
    "is_superuser": false,
    "date_joined": "2024-04-19T10:30:00Z"
}
```

---

#### 1.5 Update User Profile
**Endpoint:** `PUT /api/auth/profile/` or `PATCH /api/auth/profile/`

**Permission:** IsAuthenticated

**Request (PATCH):**
```json
{
    "first_name": "Johnny",
    "email": "newemail@example.com"
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "newemail@example.com",
    "first_name": "Johnny",
    "last_name": "Doe",
    "is_staff": false,
    "is_superuser": false,
    "date_joined": "2024-04-19T10:30:00Z"
}
```

---

### 2. Menu Endpoints

#### 2.1 Get All Menu Items
**Endpoint:** `GET /api/menu/`

**Permission:** Public (AllowAny)

**Query Parameters:**
- `page`: Page number (default: 1)
- `category`: Filter by category (coffee, tea, snacks, desserts, beverages, breakfast)
- `is_available`: Filter by availability (true/false)
- `search`: Search by name or description
- `ordering`: Order by field (name, price, created_at)

**Example Request:**
```
GET /api/menu/?page=1&category=coffee&search=latte&ordering=-price
```

**Response (200 OK):**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/menu/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Espresso",
            "category": "coffee",
            "category_display": "Coffee",
            "price": "3.50",
            "description": "Strong black coffee",
            "image": "http://localhost:8000/media/menu_items/espresso.jpg",
            "is_available": true,
            "created_at": "2024-04-19T10:00:00Z",
            "updated_at": "2024-04-19T10:00:00Z"
        },
        {
            "id": 2,
            "name": "Cappuccino",
            "category": "coffee",
            "category_display": "Coffee",
            "price": "4.50",
            "description": "Coffee with steamed milk",
            "image": "http://localhost:8000/media/menu_items/cappuccino.jpg",
            "is_available": true,
            "created_at": "2024-04-19T10:05:00Z",
            "updated_at": "2024-04-19T10:05:00Z"
        }
    ]
}
```

---

#### 2.2 Get Single Menu Item
**Endpoint:** `GET /api/menu/{id}/`

**Permission:** Public (AllowAny)

**Example Request:**
```
GET /api/menu/1/
```

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "Espresso",
    "category": "coffee",
    "category_display": "Coffee",
    "price": "3.50",
    "description": "Strong black coffee",
    "image": "http://localhost:8000/media/menu_items/espresso.jpg",
    "is_available": true,
    "created_at": "2024-04-19T10:00:00Z",
    "updated_at": "2024-04-19T10:00:00Z"
}
```

---

#### 2.3 Search Menu Items
**Endpoint:** `GET /api/menu/search/?q=coffee`

**Permission:** Public (AllowAny)

**Query Parameters:**
- `q`: Search query (minimum 2 characters)

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "name": "Espresso",
        "category": "coffee",
        "category_display": "Coffee",
        "price": "3.50",
        "description": "Strong black coffee",
        "image": "http://localhost:8000/media/menu_items/espresso.jpg",
        "is_available": true,
        "created_at": "2024-04-19T10:00:00Z",
        "updated_at": "2024-04-19T10:00:00Z"
    }
]
```

---

#### 2.4 Get Menu by Category
**Endpoint:** `GET /api/menu/by_category/?category=coffee`

**Permission:** Public (AllowAny)

**Query Parameters:**
- `category`: Category name (required)

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "name": "Espresso",
        "category": "coffee",
        "category_display": "Coffee",
        "price": "3.50",
        "description": "Strong black coffee",
        "image": "http://localhost:8000/media/menu_items/espresso.jpg",
        "is_available": true,
        "created_at": "2024-04-19T10:00:00Z",
        "updated_at": "2024-04-19T10:00:00Z"
    }
]
```

---

#### 2.5 Get Available Menu Items
**Endpoint:** `GET /api/menu/available/`

**Permission:** Public (AllowAny)

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "name": "Espresso",
        "category": "coffee",
        "category_display": "Coffee",
        "price": "3.50",
        "description": "Strong black coffee",
        "image": "http://localhost:8000/media/menu_items/espresso.jpg",
        "is_available": true,
        "created_at": "2024-04-19T10:00:00Z",
        "updated_at": "2024-04-19T10:00:00Z"
    }
]
```

---

#### 2.6 Create Menu Item (Admin Only)
**Endpoint:** `POST /api/menu/`

**Permission:** IsAdminOrReadOnly (Admin required for POST)

**Headers:**
```
Authorization: Bearer {admin_access_token}
Content-Type: multipart/form-data
```

**Request:**
```json
{
    "name": "Latte",
    "category": "coffee",
    "price": "4.75",
    "description": "Espresso with lots of steamed milk",
    "is_available": true,
    "image": <file>
}
```

**Response (201 Created):**
```json
{
    "id": 3,
    "name": "Latte",
    "category": "coffee",
    "category_display": "Coffee",
    "price": "4.75",
    "description": "Espresso with lots of steamed milk",
    "image": "http://localhost:8000/media/menu_items/latte.jpg",
    "is_available": true,
    "created_at": "2024-04-19T12:00:00Z",
    "updated_at": "2024-04-19T12:00:00Z"
}
```

---

#### 2.7 Update Menu Item (Admin Only)
**Endpoint:** `PUT /api/menu/{id}/` or `PATCH /api/menu/{id}/`

**Permission:** IsAdminOrReadOnly (Admin required)

**Headers:**
```
Authorization: Bearer {admin_access_token}
Content-Type: application/json
```

**Request (PATCH):**
```json
{
    "price": "5.00",
    "is_available": false
}
```

**Response (200 OK):**
```json
{
    "id": 3,
    "name": "Latte",
    "category": "coffee",
    "category_display": "Coffee",
    "price": "5.00",
    "description": "Espresso with lots of steamed milk",
    "image": "http://localhost:8000/media/menu_items/latte.jpg",
    "is_available": false,
    "created_at": "2024-04-19T12:00:00Z",
    "updated_at": "2024-04-19T12:30:00Z"
}
```

---

#### 2.8 Delete Menu Item (Admin Only)
**Endpoint:** `DELETE /api/menu/{id}/`

**Permission:** IsAdminOrReadOnly (Admin required)

**Headers:**
```
Authorization: Bearer {admin_access_token}
```

**Response (204 No Content):**
```
(Empty response)
```

---

### 3. Booking Endpoints

#### 3.1 Create Table Booking
**Endpoint:** `POST /api/bookings/`

**Permission:** IsAuthenticated

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "date": "2024-04-25",
    "time": "18:30",
    "number_of_people": 4,
    "special_requests": "Window seat if possible"
}
```

**Response (201 Created):**
```json
{
    "message": "Booking created successfully",
    "booking": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "123-456-7890",
        "date": "2024-04-25",
        "time": "18:30:00",
        "number_of_people": 4,
        "special_requests": "Window seat if possible",
        "status": "pending",
        "status_display": "Pending",
        "user_detail": {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe"
        },
        "booking_date_time": "2024-04-25T18:30:00",
        "created_at": "2024-04-19T14:00:00Z",
        "updated_at": "2024-04-19T14:00:00Z"
    }
}
```

**Error Response (400 Bad Request):**
```json
{
    "date": ["Booking date and time must be in the future."],
    "number_of_people": ["Maximum 20 people per booking."]
}
```

---

#### 3.2 Get User's Bookings
**Endpoint:** `GET /api/bookings/my_bookings/`

**Permission:** IsAuthenticated

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `page`: Page number
- `status`: Filter by status (pending, confirmed, completed, cancelled)
- `date`: Filter by date

**Example Request:**
```
GET /api/bookings/my_bookings/?status=confirmed
```

**Response (200 OK):**
```json
{
    "count": 2,
    "results": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "date": "2024-04-25",
            "time": "18:30:00",
            "number_of_people": 4,
            "status": "confirmed",
            "status_display": "Confirmed",
            "created_at": "2024-04-19T14:00:00Z"
        }
    ]
}
```

---

#### 3.3 Get Single Booking
**Endpoint:** `GET /api/bookings/{id}/`

**Permission:** IsAuthenticated (User can view their own, Admin can view all)

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "date": "2024-04-25",
    "time": "18:30:00",
    "number_of_people": 4,
    "special_requests": "Window seat if possible",
    "status": "pending",
    "status_display": "Pending",
    "user_detail": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "booking_date_time": "2024-04-25T18:30:00",
    "created_at": "2024-04-19T14:00:00Z",
    "updated_at": "2024-04-19T14:00:00Z"
}
```

---

#### 3.4 Update Booking
**Endpoint:** `PUT /api/bookings/{id}/` or `PATCH /api/bookings/{id}/`

**Permission:** IsAuthenticated (User can update their own, Admin can update all)

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request (PATCH):**
```json
{
    "time": "19:00",
    "number_of_people": 5
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "date": "2024-04-25",
    "time": "19:00:00",
    "number_of_people": 5,
    "special_requests": "Window seat if possible",
    "status": "pending",
    "status_display": "Pending",
    "user_detail": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "booking_date_time": "2024-04-25T19:00:00",
    "created_at": "2024-04-19T14:00:00Z",
    "updated_at": "2024-04-19T14:30:00Z"
}
```

---

#### 3.5 Cancel Booking
**Endpoint:** `DELETE /api/bookings/{id}/`

**Permission:** IsAuthenticated (User can cancel their own, Admin can cancel all)

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (204 No Content):**
```
(Empty response with message)
```

---

#### 3.6 Get All Bookings (Admin Only)
**Endpoint:** `GET /api/bookings/all_bookings/`

**Permission:** IsAdminUser

**Headers:**
```
Authorization: Bearer {admin_access_token}
```

**Query Parameters:**
- `status`: Filter by status
- `date`: Filter by date

**Response (200 OK):**
```json
{
    "count": 5,
    "results": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "123-456-7890",
            "date": "2024-04-25",
            "time": "18:30:00",
            "number_of_people": 4,
            "special_requests": "Window seat if possible",
            "status": "pending",
            "status_display": "Pending",
            "user_detail": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe"
            },
            "booking_date_time": "2024-04-25T18:30:00",
            "created_at": "2024-04-19T14:00:00Z",
            "updated_at": "2024-04-19T14:00:00Z"
        }
    ]
}
```

---

#### 3.7 Confirm Booking (Admin Only)
**Endpoint:** `POST /api/bookings/{id}/confirm_booking/`

**Permission:** IsAdminUser

**Headers:**
```
Authorization: Bearer {admin_access_token}
```

**Response (200 OK):**
```json
{
    "message": "Booking confirmed",
    "booking": {
        "id": 1,
        "status": "confirmed",
        "status_display": "Confirmed",
        "...": "..."
    }
}
```

---

#### 3.8 Complete Booking (Admin Only)
**Endpoint:** `POST /api/bookings/{id}/complete_booking/`

**Permission:** IsAdminUser

**Headers:**
```
Authorization: Bearer {admin_access_token}
```

**Response (200 OK):**
```json
{
    "message": "Booking marked as completed",
    "booking": {
        "id": 1,
        "status": "completed",
        "status_display": "Completed",
        "...": "..."
    }
}
```

---

### 4. Cafe Timing Endpoints

#### 4.1 Get Cafe Timing
**Endpoint:** `GET /api/cafe-timing/`

**Permission:** Public (AllowAny)

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "Our Cafe",
    "opening_time": "08:00:00",
    "closing_time": "22:00:00",
    "created_at": "2024-04-19T10:00:00Z",
    "updated_at": "2024-04-19T10:00:00Z"
}
```

---

#### 4.2 Get Cafe Status (Open/Closed)
**Endpoint:** `GET /api/cafe-timing/status/`

**Permission:** Public (AllowAny)

**Response (200 OK):**
```json
{
    "name": "Our Cafe",
    "is_open": true,
    "status": "OPEN",
    "opening_time": "08:00:00",
    "closing_time": "22:00:00",
    "current_time": "15:30:45"
}
```

---

#### 4.3 Update Cafe Timing (Admin Only)
**Endpoint:** `POST /api/cafe-timing/`

**Permission:** IsAdminOrReadOnly (Admin required)

**Headers:**
```
Authorization: Bearer {admin_access_token}
Content-Type: application/json
```

**Request:**
```json
{
    "name": "Our Cafe",
    "opening_time": "07:00",
    "closing_time": "23:00"
}
```

**Response (200 OK):**
```json
{
    "message": "Cafe timing updated successfully",
    "data": {
        "id": 1,
        "name": "Our Cafe",
        "opening_time": "07:00:00",
        "closing_time": "23:00:00",
        "created_at": "2024-04-19T10:00:00Z",
        "updated_at": "2024-04-19T15:30:00Z"
    }
}
```

---

## Postman Collection

### Import the Collection

You can use Postman to test the API. Here's a template for common requests:

### 1. Register User
```
POST /api/auth/register/
Body (raw JSON):
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
}
```

### 2. Login User
```
POST /api/auth/login/
Body (raw JSON):
{
    "username": "testuser",
    "password": "testpass123"
}
```

### 3. Get Menu Items
```
GET /api/menu/
Headers:
(No auth required for public endpoints)
```

### 4. Create Booking
```
POST /api/bookings/
Headers:
Authorization: Bearer {access_token}
Content-Type: application/json

Body (raw JSON):
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "date": "2024-04-25",
    "time": "18:30",
    "number_of_people": 4,
    "special_requests": "Window seat"
}
```

---

## Response Formats

### Success Response (200 OK)
```json
{
    "id": 1,
    "name": "Espresso",
    "price": "3.50",
    "...": "..."
}
```

### List Response (200 OK with Pagination)
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/menu/?page=2",
    "previous": null,
    "results": [...]
}
```

### Created Response (201 Created)
```json
{
    "message": "Resource created successfully",
    "data": {...}
}
```

---

## Error Handling

### 400 Bad Request
```json
{
    "field_name": ["Error message"],
    "another_field": ["Another error"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Server Error
```json
{
    "detail": "Internal server error"
}
```

---

## Common Query Parameters

### Pagination
- `page`: Page number (default: 1)
- Example: `/api/menu/?page=2`

### Filtering
- `category`: Filter by category
- `status`: Filter by status
- `is_available`: Filter by availability
- Example: `/api/menu/?category=coffee&is_available=true`

### Searching
- `search`: Search by name or description
- Example: `/api/menu/?search=espresso`

### Ordering
- `ordering`: Order by field
- Use `-` prefix for descending order
- Example: `/api/menu/?ordering=-price`

---

## Running the Development Server

```bash
# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`

---

## Additional Notes

- **JWT Token Lifetime**: 60 minutes (access token), 1 day (refresh token)
- **Rate Limiting**: 100/hour for anonymous users, 1000/hour for authenticated users
- **CORS**: Configured for localhost development
- **Admin Panel**: Available at `/admin/`

---

## Support

For issues or questions, please contact the development team or refer to the Django REST Framework documentation.
