# QUICK START GUIDE - CAFE MANAGEMENT SYSTEM ☕

Get your Cafe Management System up and running in 5 minutes!

---

## STEP 1: Activate Virtual Environment

### Windows (PowerShell):
```bash
.\venv\Scripts\Activate.ps1
```

### Windows (Command Prompt):
```bash
venv\Scripts\activate.bat
```

### macOS/Linux:
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal.

---

## STEP 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## STEP 3: Setup Database

```bash
python manage.py migrate
```

---

## STEP 4: Create Admin Account

```bash
python manage.py createsuperuser
```

Enter:
- Username: `admin` (or any username)
- Email: `admin@cafemate.com` (or any email)
- Password: (choose a secure password)

---

## STEP 5: Load Sample Data (Optional)

```bash
python manage.py shell < sample_data.py
```

This adds 18 sample menu items automatically.

---

## STEP 6: Run the Server

```bash
python manage.py runserver
```

---

## STEP 7: Access the Application

Open your browser and visit:

- **Home**: http://127.0.0.1:8000/
- **Menu**: http://127.0.0.1:8000/menu/
- **Book Table**: http://127.0.0.1:8000/book-table/
- **Admin**: http://127.0.0.1:8000/admin/

---

## Admin Login

Go to http://127.0.0.1:8000/admin/ and use the credentials you created in Step 4.

In the admin panel, you can:
- ✅ Add/Edit/Delete Menu Items
- ✅ View Table Bookings
- ✅ Set Cafe Hours
- ✅ Manage Users

---

## Keyboard Shortcuts

- **H** = Go to Home
- **M** = Go to Menu  
- **B** = Book Table

---

## Add More Menu Items Manually

1. Go to http://127.0.0.1:8000/admin/
2. Click "Menu Items"
3. Click "Add Menu Item"
4. Fill in the details
5. Click Save

---

## Troubleshooting

**Server won't start?**
```bash
python manage.py runserver 8001  # Use different port
```

**Static files not loading?**
```bash
python manage.py collectstatic --noinput
```

**Database errors?**
```bash
python manage.py migrate
```

---

## Next Steps

1. Customize cafe hours in admin panel
2. Add your menu items
3. Test the booking system
4. Customize colors in `cafe/static/css/style.css`
5. Deploy to production (see README.md)

---

## File Locations

- **Templates**: `cafe/templates/*.html`
- **Styles**: `cafe/static/css/style.css`
- **JavaScript**: `cafe/static/js/main.js`
- **Database Models**: `cafe/models.py`
- **Settings**: `cafe_project/settings.py`

---

## Need Help?

See **README.md** for detailed setup and customization instructions.

---

**Happy Coding! ☕**

When done, press `CTRL+C` to stop the server.
