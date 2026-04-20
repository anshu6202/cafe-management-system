"""
Sample data initialization script for Cafe Management System
Run this after migrations: python manage.py shell < sample_data.py
"""

from cafe.models import MenuItem, CafeTiming, TableBooking
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create Cafe Timing if it doesn't exist
cafe_timing, created = CafeTiming.objects.get_or_create(
    name="Our Cafe",
    defaults={
        'opening_time': '08:00',
        'closing_time': '22:00',
    }
)
print(f"Cafe Timing: {'Created' if created else 'Already exists'}")

# Menu items data
menu_data = [
    {
        'name': 'Espresso',
        'category': 'coffee',
        'price': 2.50,
        'description': 'Strong and bold espresso shot, perfect for coffee lovers.',
    },
    {
        'name': 'Cappuccino',
        'category': 'coffee',
        'price': 3.50,
        'description': 'Smooth cappuccino with perfectly steamed milk and foam.',
    },
    {
        'name': 'Latte',
        'category': 'coffee',
        'price': 3.75,
        'description': 'Creamy latte with rich espresso and velvety steamed milk.',
    },
    {
        'name': 'Americano',
        'category': 'coffee',
        'price': 2.75,
        'description': 'Classic Americano - espresso shots with hot water.',
    },
    {
        'name': 'Macchiato',
        'category': 'coffee',
        'price': 3.25,
        'description': 'Espresso "marked" with a touch of steamed milk.',
    },
    {
        'name': 'Green Tea',
        'category': 'tea',
        'price': 2.50,
        'description': 'Refreshing organic green tea.',
    },
    {
        'name': 'Black Tea',
        'category': 'tea',
        'price': 2.50,
        'description': 'Premium black tea with a rich flavor.',
    },
    {
        'name': 'Herbal Tea',
        'category': 'tea',
        'price': 2.75,
        'description': 'Soothing herbal tea blend.',
    },
    {
        'name': 'Croissant',
        'category': 'breakfast',
        'price': 3.00,
        'description': 'Flaky, buttery croissant perfect with your morning coffee.',
    },
    {
        'name': 'Bagel with Cream Cheese',
        'category': 'breakfast',
        'price': 4.00,
        'description': 'Fresh bagel with creamy cheese spread.',
    },
    {
        'name': 'Panini Sandwich',
        'category': 'snacks',
        'price': 6.50,
        'description': 'Grilled panini with mozzarella and fresh vegetables.',
    },
    {
        'name': 'Caesar Salad',
        'category': 'snacks',
        'price': 7.00,
        'description': 'Fresh Caesar salad with homemade dressing.',
    },
    {
        'name': 'Chocolate Cake',
        'category': 'desserts',
        'price': 4.50,
        'description': 'Rich and decadent chocolate cake slice.',
    },
    {
        'name': 'Cheesecake',
        'category': 'desserts',
        'price': 4.75,
        'description': 'Creamy New York style cheesecake.',
    },
    {
        'name': 'Brownies',
        'category': 'desserts',
        'price': 3.50,
        'description': 'Fudgy chocolate brownies.',
    },
    {
        'name': 'Orange Juice',
        'category': 'beverages',
        'price': 3.00,
        'description': 'Fresh squeezed orange juice.',
    },
    {
        'name': 'Iced Coffee',
        'category': 'beverages',
        'price': 3.50,
        'description': 'Cold and refreshing iced coffee.',
    },
    {
        'name': 'Smoothie',
        'category': 'beverages',
        'price': 4.50,
        'description': 'Fresh fruit smoothie with yogurt.',
    },
]

# Create menu items
created_count = 0
for item in menu_data:
    menu_item, created = MenuItem.objects.get_or_create(
        name=item['name'],
        defaults={
            'category': item['category'],
            'price': item['price'],
            'description': item['description'],
            'is_available': True,
        }
    )
    if created:
        created_count += 1

print(f"Menu Items: {created_count} new items created")
print(f"Total menu items: {MenuItem.objects.count()}")

print("\n✓ Sample data initialized successfully!")
print("\nNext steps:")
print("1. Go to http://127.0.0.1:8000/admin/")
print("2. Add more menu items as needed")
print("3. Create bookings to test the system")
print("4. Visit http://127.0.0.1:8000/ to view the site")
