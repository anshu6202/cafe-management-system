# CAFE MANAGEMENT SYSTEM - SETUP INSTRUCTIONS

## Project Overview
A full-stack Cafe Management System built with Django (backend) and HTML, CSS, JavaScript (frontend).

### Features Included:
✅ User Authentication (Signup/Login/Logout)
✅ Home Page with Cafe Info
✅ Dynamic Menu with Filtering & Search
✅ Table Booking System
✅ Booking History for Logged-in Users
✅ Admin Panel for Management
✅ Cafe Timing/Hours Management
✅ Responsive Design (Mobile & Desktop)
✅ Beautiful UI with Modern Styling

---

## PREREQUISITES

Before you start, make sure you have:
- Python 3.8 or higher installed
- pip (Python package manager)
- Git (optional, for version control)

### Check Python Installation:
```bash
python --version
pip --version
```

---

## STEP 1: INITIAL SETUP

### 1.1 Navigate to Project Directory
```bash
cd c:\Users\dell\PROJECT\cafe_management
```

### 1.2 Create Virtual Environment
Create a Python virtual environment to isolate project dependencies:

**On Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal when activated.

### 1.3 Upgrade pip
```bash
python -m pip install --upgrade pip
```

---

## STEP 2: INSTALL DEPENDENCIES

Install all required packages from requirements.txt:

```bash
pip install -r requirements.txt
```

This will install:
- Django 4.2.0 (Web Framework)
- Pillow 10.0.0 (Image Processing)
- python-dateutil 2.8.2 (Date Utilities)

---

## STEP 3: DATABASE SETUP

### 3.1 Create Migrations
Run the following command to create database migration files:

```bash
python manage.py makemigrations
```

### 3.2 Apply Migrations
Migrate the database to create all necessary tables:

```bash
python manage.py migrate
```

This creates a SQLite database (db.sqlite3) with all required tables.

---

## STEP 4: CREATE SUPERUSER (ADMIN)

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts:
- Username: (choose a username, e.g., "admin")
- Email: (enter your email)
- Password: (enter a password)
- Password (again): (confirm password)

**Example:**
```
Username: admin
Email: admin@cafemate.com
Password: ••••••••
Password (again): ••••••••
```

---

## STEP 5: COLLECT STATIC FILES (Optional but Recommended)

```bash
python manage.py collectstatic --noinput
```

This gathers all CSS, JS, and image files into one location.

---

## STEP 6: RUN THE DEVELOPMENT SERVER

Start the Django development server:

```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## STEP 7: ACCESS THE APPLICATION

### Application URLs:
- **Home Page**: http://127.0.0.1:8000/
- **Menu**: http://127.0.0.1:8000/menu/
- **Book Table**: http://127.0.0.1:8000/book-table/
- **Signup**: http://127.0.0.1:8000/signup/
- **Login**: http://127.0.0.1:8000/login/
- **Admin Panel**: http://127.0.0.1:8000/admin/

### Login to Admin Panel:
1. Go to http://127.0.0.1:8000/admin/
2. Enter the superuser credentials created in Step 4
3. You can now:
   - Add/Edit/Delete Menu Items
   - View and Manage Table Bookings
   - Set Cafe Opening & Closing Times
   - Manage Users

---

## STEP 8: ADD SAMPLE DATA (OPTIONAL)

### 8.1 Add Cafe Timing
1. Go to Admin Panel: http://127.0.0.1:8000/admin/
2. Click on "Cafe Timings"
3. Click "Add Cafe Timing"
4. Set:
   - Name: "Our Cafe"
   - Opening Time: 08:00
   - Closing Time: 22:00
5. Click Save

### 8.2 Add Menu Items
1. Go to Admin Panel
2. Click on "Menu Items"
3. Click "Add Menu Item"
4. Fill in:
   - Name: (e.g., "Cappuccino")
   - Category: (choose from dropdown)
   - Price: (e.g., 3.50)
   - Description: (brief description)
   - Image: (optional, upload an image)
5. Check "Is Available"
6. Click Save

Add multiple items across different categories:
- Coffee
- Tea
- Snacks
- Desserts
- Beverages
- Breakfast

---

## KEYBOARD SHORTCUTS

While using the application:
- **H**: Go to Home
- **M**: Go to Menu
- **B**: Book a Table

---

## PROJECT STRUCTURE

```
cafe_management/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # SQLite database (created after migration)
├── cafe_project/                      # Project configuration
│   ├── __init__.py
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Main URL routing
│   └── wsgi.py                        # WSGI configuration
├── cafe/                              # Main Django app
│   ├── migrations/                    # Database migrations
│   ├── templates/                     # HTML templates
│   │   ├── base.html                  # Base template
│   │   ├── home.html                  # Home page
│   │   ├── menu.html                  # Menu page
│   │   ├── menu_detail.html           # Menu item details
│   │   ├── book_table.html            # Booking form
│   │   ├── booking_success.html       # Success page
│   │   ├── booking_history.html       # User bookings
│   │   ├── signup.html                # Signup page
│   │   └── login.html                 # Login page
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css              # Main stylesheet
│   │   ├── js/
│   │   │   └── main.js                # JavaScript functionality
│   │   └── images/                    # Image files
│   ├── models.py                      # Database models
│   ├── views.py                       # View functions
│   ├── forms.py                       # Django forms
│   ├── urls.py                        # App URL routing
│   ├── admin.py                       # Admin configuration
│   ├── apps.py                        # App configuration
│   └── __init__.py
```

---

## COMMON COMMANDS

### Start Server
```bash
python manage.py runserver
```

### Create New Superuser
```bash
python manage.py createsuperuser
```

### Make Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Access Django Shell
```bash
python manage.py shell
```

### Clear Database (CAUTION!)
```bash
python manage.py flush
```

---

## TROUBLESHOOTING

### Problem: Virtual environment not activating
**Solution**: Make sure you're in the correct directory and use the correct activation script.

### Problem: "Module not found" errors
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Problem: Database errors
**Solution**: Reset the database:
```bash
python manage.py migrate
```

### Problem: Port 8000 already in use
**Solution**: Run on a different port:
```bash
python manage.py runserver 8001
```

### Problem: Static files not loading
**Solution**: Collect static files:
```bash
python manage.py collectstatic --noinput
```

### Problem: Permission denied errors
**Solution**: Check file permissions and try running as administrator.

---

## FEATURES WALKTHROUGH

### 1. Home Page
- Welcome message
- Featured menu items
- Cafe info cards
- Call-to-action buttons

### 2. Menu Page
- Browse all menu items
- Filter by category
- Search functionality
- View item details

### 3. Booking System
- Book table with date/time selection
- Automatic date validation (no past dates)
- Email confirmation
- Special requests field

### 4. User Accounts
- Create new account
- Login/Logout
- View booking history
- Profile management

### 5. Admin Panel
- Manage menu items (Add/Edit/Delete)
- View all bookings
- Update booking status
- Set cafe hours
- User management

---

## CUSTOMIZATION

### Change Cafe Name
Edit `cafe_project/settings.py`:
```python
# Change to your cafe name in templates
# Templates use "CafeMate" - search and replace with your name
```

### Modify Colors
Edit `cafe/static/css/style.css`:
```css
:root {
    --primary-color: #8B4513;      /* Change primary color */
    --secondary-color: #D2B48C;    /* Change secondary color */
    --accent-color: #FF6B6B;       /* Change accent color */
}
```

### Add More Menu Categories
Edit `cafe/models.py`:
```python
CATEGORY_CHOICES = [
    ('coffee', 'Coffee'),
    ('tea', 'Tea'),
    ('your_category', 'Your Category'),  # Add here
]
```

---

## DEPLOYMENT PREPARATION

### Before deploying to production:
1. Set DEBUG = False in settings.py
2. Update ALLOWED_HOSTS with your domain
3. Change SECRET_KEY to a random value
4. Use a production database (PostgreSQL recommended)
5. Set up proper static file serving
6. Enable HTTPS/SSL
7. Set up error logging
8. Configure email for notifications

---

## PERFORMANCE TIPS

1. **Use Database Indexing**: Already done for common fields
2. **Enable Caching**: Add caching middleware for static files
3. **Optimize Images**: Compress images before uploading
4. **Use CDN**: Serve static files from CDN in production
5. **Database Optimization**: Regular cleanup of old bookings

---

## SECURITY NOTES

- CSRF protection is enabled
- SQL injection is prevented by Django ORM
- Password hashing uses Django's default hasher
- Cross-origin requests are restricted
- Session security is configured

---

## SUPPORT & ADDITIONAL RESOURCES

- Django Documentation: https://docs.djangoproject.com/
- Python Documentation: https://docs.python.org/
- Get help in Django Community Forum

---

## License

This project is open source and free to use and modify.

---

## PROJECT COMPLETED! 🎉

Your Cafe Management System is now ready to use!

For questions or issues, refer to the troubleshooting section above.

Happy Coding! ☕
#   c a f e - m a n a g e m e n t - s y s t e m  
 