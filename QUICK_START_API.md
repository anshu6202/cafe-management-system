# Quick Start Guide - REST API Setup

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Installed packages:**
- `djangorestframework` - Django REST Framework for building APIs
- `djangorestframework-simplejwt` - JWT authentication
- `django-filter` - Advanced filtering support
- `django-cors-headers` - CORS support for frontend

---

## 2. Apply Database Migrations

```bash
python manage.py migrate
```

---

## 3. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

**Example:**
```
Username: admin
Email: admin@example.com
Password: admin123
```

---

## 4. Run Development Server

```bash
python manage.py runserver
```

The API will be available at: **`http://localhost:8000/api/`**

---

## 5. Quick Test Using Python Script

Install requests library (if not already installed):
```bash
pip install requests
```

Run the test script:
```bash
python test_api.py
```

This will automatically test all API endpoints.

---

## 6. Manual Testing with cURL

### Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }'
```

### Login and Get Token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### Get All Menu Items
```bash
curl -X GET http://localhost:8000/api/menu/
```

### Create a Booking (requires token)
```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "date": "2024-04-25",
    "time": "18:30",
    "number_of_people": 4,
    "special_requests": "Window seat"
  }'
```

---

## 7. Using Postman for API Testing

### Import the Collection

1. Open Postman
2. Click **"Import"** button
3. Select **"Upload Files"**
4. Choose `Cafe_Management_API.postman_collection.json`
5. Click **"Import"**

### Set Environment Variables

1. Create new Environment
2. Add variables:
   - `access_token`: Your JWT access token
   - `refresh_token`: Your JWT refresh token
   - `admin_access_token`: Admin JWT token

### Test Steps

1. **Register** → Get user credentials
2. **Login** → Get JWT tokens (save access_token)
3. **Get Menu Items** → View all items
4. **Create Booking** → Create new booking
5. **Get My Bookings** → View your bookings
6. **Update Booking** → Modify booking details
7. **Cancel Booking** → Cancel the booking

---

## 8. API Endpoints Summary

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `GET /api/auth/profile/` - Get user profile
- `PUT/PATCH /api/auth/profile/` - Update profile

### Menu
- `GET /api/menu/` - Get all menu items
- `GET /api/menu/{id}/` - Get single item
- `GET /api/menu/search/?q=coffee` - Search menu
- `GET /api/menu/by_category/?category=coffee` - Filter by category
- `GET /api/menu/available/` - Get available items
- `POST /api/menu/` - Create item (admin only)
- `PUT/PATCH /api/menu/{id}/` - Update item (admin only)
- `DELETE /api/menu/{id}/` - Delete item (admin only)

### Bookings
- `POST /api/bookings/` - Create booking
- `GET /api/bookings/my_bookings/` - Get user's bookings
- `GET /api/bookings/{id}/` - Get single booking
- `PUT/PATCH /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Cancel booking
- `GET /api/bookings/all_bookings/` - Get all bookings (admin)
- `POST /api/bookings/{id}/confirm_booking/` - Confirm (admin)
- `POST /api/bookings/{id}/complete_booking/` - Complete (admin)

### Cafe Timing
- `GET /api/cafe-timing/` - Get cafe timing
- `GET /api/cafe-timing/status/` - Get open/closed status
- `POST /api/cafe-timing/` - Update timing (admin only)

---

## 9. Common Issues & Solutions

### Issue: "No module named 'rest_framework'"
**Solution:** Run `pip install -r requirements.txt`

### Issue: "Unauthorized" error
**Solution:** Make sure you include the JWT token in Authorization header:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Issue: "Page not found" (404)
**Solution:** Make sure server is running and use correct endpoint paths

### Issue: "Booking date and time must be in the future"
**Solution:** Use a future date/time for booking (e.g., 7 days from now)

### Issue: CORS errors from frontend
**Solution:** Already configured in settings.py for localhost. Add your domain if needed.

---

## 10. File Structure

```
cafe_management/
├── API_DOCUMENTATION.md          # Comprehensive API docs
├── QUICK_START_API.md            # This file
├── test_api.py                   # Python test script
├── Cafe_Management_API.postman_collection.json  # Postman collection
├── cafe/
│   ├── api_views.py              # API views/viewsets
│   ├── api_urls.py               # API routes
│   ├── serializers.py            # Serializers for models
│   ├── permissions.py            # Custom permissions
│   ├── models.py                 # Database models
│   └── ...
├── cafe_project/
│   ├── settings.py               # Settings (DRF configured)
│   ├── urls.py                   # Main URLs
│   └── ...
└── ...
```

---

## 11. Next Steps

1. ✅ Install dependencies
2. ✅ Apply migrations
3. ✅ Create superuser
4. ✅ Run server
5. ✅ Test API endpoints
6. 📝 Deploy to production (update ALLOWED_HOSTS, DEBUG=False)
7. 🔒 Secure SECRET_KEY and environment variables
8. 📊 Add monitoring and logging
9. 🚀 Deploy to cloud (AWS, Heroku, etc.)

---

## 12. Production Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Use environment variables for sensitive data
- [ ] Set `SECRET_KEY` to a strong random value
- [ ] Configure proper database (PostgreSQL recommended)
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure CORS for your frontend domain
- [ ] Add logging and error tracking
- [ ] Set up backup strategy
- [ ] Test thoroughly before deployment

---

## Support & Documentation

- **Full API Documentation:** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Django REST Framework:** https://www.django-rest-framework.org/
- **JWT Authentication:** https://django-rest-framework-simplejwt.readthedocs.io/

---

## Success! 🎉

Your REST API is now ready for use. Start building amazing applications with it!
