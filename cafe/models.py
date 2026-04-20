from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CafeTiming(models.Model):
    """Store cafe opening and closing times"""
    name = models.CharField(max_length=100, default="Our Cafe")
    opening_time = models.TimeField(default="08:00")
    closing_time = models.TimeField(default="22:00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Cafe Timings"

    def __str__(self):
        return f"{self.name} - {self.opening_time} to {self.closing_time}"


class MenuItem(models.Model):
    """Store menu items with details"""
    CATEGORY_CHOICES = [
        ('coffee', 'Coffee'),
        ('tea', 'Tea'),
        ('snacks', 'Snacks'),
        ('desserts', 'Desserts'),
        ('beverages', 'Beverages'),
        ('breakfast', 'Breakfast'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return f"{self.name} - ${self.price}"


class TableBooking(models.Model):
    """Store table booking information"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking by {self.name} on {self.date} at {self.time}"


class Order(models.Model):
    """Store order and payment details."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_reference = models.CharField(max_length=255, blank=True, null=True)
    delivery_address = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"


class OrderItem(models.Model):
    """Store individual items inside an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        self.price = self.menu_item.price
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
