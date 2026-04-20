"""
Serializers for Cafe Management System
Handles data validation and transformation for API endpoints
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MenuItem, TableBooking, CafeTiming, Order, OrderItem
import re


# ====================== USER SERIALIZERS ======================

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=6
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=6
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, data):
        """Validate password match"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                'password': "Passwords don't match."
            })
        
        # Check if username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({
                'username': "Username already exists."
            })
        
        # Check if email already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                'email': "Email already registered."
            })
        
        return data

    def create(self, validated_data):
        """Create user with validated data"""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data (read-only public info)
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile (with additional details)
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined')
        read_only_fields = ('id', 'is_staff', 'is_superuser', 'date_joined')


# ====================== MENU SERIALIZERS ======================

class MenuItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Menu Items
    Includes validation for price and category
    """
    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True
    )

    class Meta:
        model = MenuItem
        fields = (
            'id', 'name', 'category', 'category_display', 'price',
            'description', 'image', 'is_available',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'category': {'required': True},
            'price': {'required': True},
            'description': {'required': True, 'allow_blank': False},
        }

    def validate_price(self, value):
        """Validate that price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_name(self, value):
        """Validate menu item name"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value


class MenuItemCreateUpdateSerializer(MenuItemSerializer):
    """
    Serializer for creating and updating menu items (admin only)
    Includes additional validation
    """
    pass


class MenuItemDetailSerializer(MenuItemSerializer):
    """
    Detailed serializer for single menu item
    """
    pass


# ====================== BOOKING SERIALIZERS ======================

class TableBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Table Bookings
    """
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    user_detail = UserSerializer(
        source='user',
        read_only=True
    )
    booking_date_time = serializers.SerializerMethodField()

    class Meta:
        model = TableBooking
        fields = (
            'id', 'name', 'email', 'phone', 'date', 'time',
            'number_of_people', 'special_requests', 'status',
            'status_display', 'user_detail', 'booking_date_time',
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'status', 'user_detail', 'created_at', 'updated_at'
        )
        extra_kwargs = {
            'date': {'required': True},
            'time': {'required': True},
            'number_of_people': {'required': True},
        }

    def get_booking_date_time(self, obj):
        """Combine date and time into single datetime string"""
        from datetime import datetime
        dt = datetime.combine(obj.date, obj.time)
        return dt.isoformat()

    def validate(self, data):
        """Validate booking data"""
        from django.utils import timezone
        from datetime import datetime

        # Validate date and time are in future
        booking_datetime = datetime.combine(data['date'], data['time'])
        if booking_datetime <= timezone.now():
            raise serializers.ValidationError(
                "Booking date and time must be in the future."
            )

        # Validate number of people
        if data['number_of_people'] < 1:
            raise serializers.ValidationError(
                "Number of people must be at least 1."
            )
        if data['number_of_people'] > 20:
            raise serializers.ValidationError(
                "Maximum 20 people per booking."
            )

        return data

    def validate_email(self, value):
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email format.")
        return value


class TableBookingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating table bookings
    """
    class Meta:
        model = TableBooking
        fields = (
            'name', 'email', 'phone', 'date', 'time',
            'number_of_people', 'special_requests'
        )

    def validate(self, data):
        """Validate booking data"""
        from django.utils import timezone
        from datetime import datetime

        booking_datetime = datetime.combine(data['date'], data['time'])
        if booking_datetime <= timezone.now():
            raise serializers.ValidationError(
                "Booking date and time must be in the future."
            )

        if data['number_of_people'] < 1 or data['number_of_people'] > 20:
            raise serializers.ValidationError(
                "Number of people must be between 1 and 20."
            )

        return data


class TableBookingUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating table bookings
    """
    class Meta:
        model = TableBooking
        fields = (
            'name', 'email', 'phone', 'date', 'time',
            'number_of_people', 'special_requests', 'status'
        )


class BookingHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for user's booking history
    """
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = TableBooking
        fields = (
            'id', 'name', 'email', 'date', 'time',
            'number_of_people', 'status', 'status_display',
            'created_at'
        )
        read_only_fields = '__all__'


# ====================== ORDER SERIALIZERS ======================

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items"""
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_image = serializers.ImageField(source='menu_item.image', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'menu_item', 'menu_item_name', 'menu_item_image', 'quantity', 'price', 'total_price')
        read_only_fields = ('id', 'price', 'total_price', 'menu_item_name', 'menu_item_image')


class OrderCreateItemSerializer(serializers.Serializer):
    """Serializer for items in an order create request"""
    menu_item = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for creating an order"""
    items = OrderCreateItemSerializer(many=True)
    delivery_address = serializers.CharField(required=False, allow_blank=True)
    payment_reference = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError('Order must contain at least one item.')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data.pop('items')
        delivery_address = validated_data.get('delivery_address', '')
        total_amount = 0

        order = Order.objects.create(
            user=user,
            total_amount=0,
            status='pending',
            payment_status='pending',
            delivery_address=delivery_address,
        )

        for item_data in items_data:
            menu_item = MenuItem.objects.filter(id=item_data['menu_item'], is_available=True).first()
            if not menu_item:
                order.delete()
                raise serializers.ValidationError({
                    'items': f"Menu item {item_data['menu_item']} not found or unavailable."
                })

            quantity = item_data['quantity']
            item_total = menu_item.price * quantity
            total_amount += item_total

            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                price=menu_item.price,
                total_price=item_total,
            )

        order.total_amount = total_amount
        order.save()
        return order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders with nested items"""
    items = OrderItemSerializer(many=True, read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'user_detail', 'total_amount', 'status', 'payment_status',
            'payment_reference', 'delivery_address', 'items', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user_detail', 'created_at', 'updated_at')


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating order status"""
    class Meta:
        model = Order
        fields = ('status', 'payment_status', 'payment_reference')

class CafeTimingSerializer(serializers.ModelSerializer):
    """
    Serializer for Cafe Timing
    """
    class Meta:
        model = CafeTiming
        fields = ('id', 'name', 'opening_time', 'closing_time', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'name': {'required': True},
            'opening_time': {'required': True},
            'closing_time': {'required': True},
        }

    def validate(self, data):
        """Validate opening and closing times"""
        if data['opening_time'] >= data['closing_time']:
            raise serializers.ValidationError(
                "Opening time must be before closing time."
            )
        return data


class CafeStatusSerializer(serializers.Serializer):
    """
    Serializer for cafe status (open/closed)
    """
    name = serializers.CharField()
    is_open = serializers.BooleanField()
    status = serializers.CharField()
    opening_time = serializers.TimeField()
    closing_time = serializers.TimeField()
    current_time = serializers.TimeField(read_only=True)
