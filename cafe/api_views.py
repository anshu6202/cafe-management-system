"""
API Views for Cafe Management System
Handles all API endpoints for the application
"""

from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Q, Sum

from .models import MenuItem, TableBooking, CafeTiming, Order, OrderItem
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserProfileSerializer,
    MenuItemSerializer,
    MenuItemCreateUpdateSerializer,
    MenuItemDetailSerializer,
    TableBookingSerializer,
    TableBookingCreateSerializer,
    TableBookingUpdateSerializer,
    BookingHistorySerializer,
    CafeTimingSerializer,
    CafeStatusSerializer,
    OrderCreateSerializer,
    OrderSerializer,
    OrderStatusUpdateSerializer,
)
from .permissions import (
    IsAdminOrReadOnly,
    IsAdminUser,
    IsOwnerOrAdmin,
    IsAuthenticatedAndNotAnonymous,
)


# ====================== HELPER FUNCTIONS ======================

def send_booking_confirmation_email(booking):
    subject = 'Booking Confirmed - Cafe Management'
    message = (
        f"Hi {booking.name},\n\n"
        f"Your booking for {booking.date} at {booking.time} has been received.\n"
        f"Status: {booking.status}\n"
        f"Number of people: {booking.number_of_people}\n\n"
        "Thank you for choosing our cafe!"
    )
    send_mail(subject, message, 'no-reply@cafemanagement.local', [booking.email], fail_silently=True)


def send_order_confirmation_email(order):
    subject = 'Order Confirmation - Cafe Management'
    items_text = '\n'.join([
        f"- {item.menu_item.name} x{item.quantity}: ${item.total_price}" for item in order.items.all()
    ])
    message = (
        f"Hi {order.user.username},\n\n"
        "Thank you for your order. Here are the details:\n\n"
        f"Order ID: {order.id}\n"
        f"Total Amount: ${order.total_amount}\n"
        f"Payment Status: {order.payment_status}\n"
        f"Order Status: {order.status}\n\n"
        f"Items:\n{items_text}\n\n"
        "We will notify you once your order is ready."
    )
    send_mail(subject, message, 'no-reply@cafemanagement.local', [order.user.email], fail_silently=True)


# ====================== AUTHENTICATION VIEWS ======================

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            {
                'message': 'User registered successfully',
                'user': UserSerializer(serializer.instance).data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UserLoginView(generics.GenericAPIView):
    """
    API endpoint for user login
    POST /api/auth/login/
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Both username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'message': 'Login successful',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserProfileSerializer(user).data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid username or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class UserLogoutView(generics.GenericAPIView):
    """
    API endpoint for user logout
    POST /api/auth/logout/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for user profile
    GET /api/auth/profile/
    PUT /api/auth/profile/
    PATCH /api/auth/profile/
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# ====================== MENU ITEM VIEWS ======================

class MenuItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for menu items
    GET /api/menu/ - Get all menu items
    POST /api/menu/ - Create menu item (admin only)
    GET /api/menu/{id}/ - Get single menu item
    PUT /api/menu/{id}/ - Update menu item (admin only)
    PATCH /api/menu/{id}/ - Partial update (admin only)
    DELETE /api/menu/{id}/ - Delete menu item (admin only)
    GET /api/menu/?category=coffee - Filter by category
    GET /api/menu/?search=coffee - Search menu items
    """
    queryset = MenuItem.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return MenuItemCreateUpdateSerializer
        if self.action == 'retrieve':
            return MenuItemDetailSerializer
        return MenuItemSerializer

    def create(self, request, *args, **kwargs):
        """Override create to check admin permission"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admins can create menu items.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def by_category(self, request):
        """
        Get menu items by category
        GET /api/menu/by_category/?category=coffee
        """
        category = request.query_params.get('category')
        if not category:
            return Response(
                {'error': 'Category parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        items = MenuItem.objects.filter(category=category, is_available=True)
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def search(self, request):
        """
        Search menu items
        GET /api/menu/search/?q=coffee
        """
        query = request.query_params.get('q', '').strip()
        if len(query) < 2:
            return Response(
                {'error': 'Search query must be at least 2 characters.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        items = MenuItem.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_available=True
        )
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def available(self, request):
        """
        Get only available menu items
        GET /api/menu/available/
        """
        items = MenuItem.objects.filter(is_available=True)
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)


# ====================== BOOKING VIEWS ======================

class TableBookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for table bookings
    GET /api/bookings/ - Get all bookings (admin only)
    POST /api/bookings/ - Create booking
    GET /api/bookings/{id}/ - Get single booking
    PUT /api/bookings/{id}/ - Update booking
    PATCH /api/bookings/{id}/ - Partial update
    DELETE /api/bookings/{id}/ - Delete booking
    """
    queryset = TableBooking.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'date']
    ordering_fields = ['date', 'time', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return TableBookingCreateSerializer
        if self.action in ['update', 'partial_update']:
            return TableBookingUpdateSerializer
        if self.action == 'my_bookings':
            return BookingHistorySerializer
        return TableBookingSerializer

    def get_queryset(self):
        """
        Filter bookings based on user role
        Admins see all bookings
        Regular users see only their bookings
        """
        if self.request.user.is_staff:
            return TableBooking.objects.all()
        return TableBooking.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new booking"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        booking = serializer.save(user=request.user)
        
        return Response(
            {
                'message': 'Booking created successfully',
                'booking': TableBookingSerializer(booking).data
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """Update booking - admins can update status, users can only update their own"""
        booking = self.get_object()
        
        if booking.user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only update your own bookings.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete booking - cancel only if not completed"""
        booking = self.get_object()
        
        if booking.user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only delete your own bookings.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status == 'completed':
            return Response(
                {'error': 'Cannot cancel a completed booking.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        
        return Response(
            {'message': 'Booking cancelled successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_bookings(self, request):
        """
        Get current user's bookings
        GET /api/bookings/my_bookings/
        """
        bookings = TableBooking.objects.filter(user=request.user).order_by('-created_at')
        serializer = self.get_serializer(bookings, many=True)
        
        return Response(
            {
                'count': bookings.count(),
                'results': serializer.data
            }
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def all_bookings(self, request):
        """
        Get all bookings (admin only)
        GET /api/bookings/all_bookings/
        """
        status_filter = request.query_params.get('status')
        
        bookings = TableBooking.objects.all()
        if status_filter:
            bookings = bookings.filter(status=status_filter)
        
        bookings = bookings.order_by('-created_at')
        serializer = TableBookingSerializer(bookings, many=True)
        
        return Response(
            {
                'count': bookings.count(),
                'results': serializer.data
            }
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def confirm_booking(self, request, pk=None):
        """
        Confirm a booking (admin only)
        POST /api/bookings/{id}/confirm_booking/
        """
        booking = self.get_object()
        booking.status = 'confirmed'
        booking.save()
        
        return Response(
            {
                'message': 'Booking confirmed',
                'booking': TableBookingSerializer(booking).data
            }
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def complete_booking(self, request, pk=None):
        """
        Mark booking as completed (admin only)
        POST /api/bookings/{id}/complete_booking/
        """
        booking = self.get_object()
        booking.status = 'completed'
        booking.save()
        
        return Response(
            {
                'message': 'Booking marked as completed',
                'booking': TableBookingSerializer(booking).data
            }
        )


# ====================== ORDER VIEWS ======================

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for orders
    POST /api/orders/ - Create order
    GET /api/orders/ - List orders (user or admin)
    GET /api/orders/{id}/ - Retrieve order
    PATCH /api/orders/{id}/ - Update order status
    DELETE /api/orders/{id}/ - Cancel order
    """
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'payment_status']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action in ['partial_update', 'update']:
            return OrderStatusUpdateSerializer
        return OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # For demo, payment will be pending unless a reference is passed.
        if request.data.get('payment_reference'):
            order.payment_status = 'paid'
            order.status = 'paid'
            order.payment_reference = request.data.get('payment_reference')
            order.save()

        send_order_confirmation_email(order)

        return Response(
            {
                'message': 'Order created successfully',
                'order': OrderSerializer(order).data
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if not request.user.is_staff and order.user != request.user:
            return Response(
                {'error': 'You do not have permission to update this order.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if order.status == 'paid' and order.payment_status == 'paid':
            send_order_confirmation_email(order)

        return Response(OrderSerializer(order).data)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        if order.user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only cancel your own order.'},
                status=status.HTTP_403_FORBIDDEN
            )
        order.status = 'cancelled'
        order.payment_status = 'failed'
        order.save()
        return Response(
            {'message': 'Order cancelled successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_orders(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = self.get_serializer(orders, many=True)
        return Response({
            'count': orders.count(),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(payment_status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
        popular_items = OrderItem.objects.values('menu_item__name').annotate(count=Sum('quantity')).order_by('-count')[:5]
        return Response({
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'popular_items': list(popular_items),
        })


# ====================== CAFE TIMING VIEWS ======================

class CafeTimingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for cafe timing
    GET /api/cafe-timing/ - Get cafe timing
    POST /api/cafe-timing/ - Create/update cafe timing (admin only)
    """
    queryset = CafeTiming.objects.all()
    serializer_class = CafeTimingSerializer
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        """Get the current cafe timing"""
        cafe = CafeTiming.objects.first()
        if not cafe:
            return Response(
                {'error': 'Cafe timing not configured.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(cafe)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create or update cafe timing"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admins can update cafe timing.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        cafe = CafeTiming.objects.first()
        if cafe:
            serializer = self.get_serializer(cafe, data=request.data, partial=True)
        else:
            serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {
                'message': 'Cafe timing updated successfully',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def status(self, request):
        """
        Get cafe open/closed status
        GET /api/cafe-timing/status/
        """
        cafe = CafeTiming.objects.first()
        if not cafe:
            return Response(
                {'error': 'Cafe timing not configured.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        current_time = timezone.now().time()
        is_open = cafe.opening_time <= current_time <= cafe.closing_time
        
        data = {
            'name': cafe.name,
            'is_open': is_open,
            'status': 'OPEN' if is_open else 'CLOSED',
            'opening_time': str(cafe.opening_time),
            'closing_time': str(cafe.closing_time),
            'current_time': str(current_time),
        }
        
        return Response(data)


# ====================== GENERIC API VIEWS ======================

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    Root API endpoint
    GET /api/
    """
    return Response({
        'message': 'Welcome to Cafe Management API',
        'version': '1.0.0',
        'endpoints': {
            'authentication': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/',
                'profile': '/api/auth/profile/',
                'token': '/api/token/',
                'token_refresh': '/api/token/refresh/',
            },
            'menu': '/api/menu/',
            'bookings': '/api/bookings/',
            'orders': '/api/orders/',
            'cafe_timing': '/api/cafe-timing/',
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_docs(request):
    """
    API documentation endpoint
    GET /api/docs/
    """
    return Response({
        'documentation': 'API Documentation for Cafe Management System',
        'base_url': request.build_absolute_uri('/api/'),
        'endpoints': {
            'Authentication': {
                'Register': 'POST /api/auth/register/',
                'Login': 'POST /api/auth/login/',
                'Logout': 'POST /api/auth/logout/',
                'Profile': 'GET|PUT|PATCH /api/auth/profile/',
            },
            'Menu': {
                'List All': 'GET /api/menu/',
                'Create': 'POST /api/menu/ (admin only)',
                'Retrieve': 'GET /api/menu/{id}/',
                'Update': 'PUT /api/menu/{id}/ (admin only)',
                'Partial Update': 'PATCH /api/menu/{id}/ (admin only)',
                'Delete': 'DELETE /api/menu/{id}/ (admin only)',
                'By Category': 'GET /api/menu/by_category/?category=coffee',
                'Search': 'GET /api/menu/search/?q=coffee',
                'Available': 'GET /api/menu/available/',
            },
            'Bookings': {
                'Create': 'POST /api/bookings/',
                'My Bookings': 'GET /api/bookings/my_bookings/',
                'All Bookings': 'GET /api/bookings/all_bookings/ (admin)',
                'Retrieve': 'GET /api/bookings/{id}/',
                'Update': 'PUT /api/bookings/{id}/',
                'Partial Update': 'PATCH /api/bookings/{id}/',
                'Cancel': 'DELETE /api/bookings/{id}/',
                'Confirm': 'POST /api/bookings/{id}/confirm_booking/ (admin)',
                'Complete': 'POST /api/bookings/{id}/complete_booking/ (admin)',
            },
            'Orders': {
                'Create': 'POST /api/orders/',
                'My Orders': 'GET /api/orders/my_orders/',
                'Retrieve': 'GET /api/orders/{id}/',
                'Update': 'PATCH /api/orders/{id}/',
                'Cancel': 'DELETE /api/orders/{id}/',
                'Statistics': 'GET /api/orders/statistics/ (admin)',
            },
            'Cafe Timing': {
                'Get Timing': 'GET /api/cafe-timing/',
                'Update Timing': 'POST /api/cafe-timing/ (admin only)',
                'Status': 'GET /api/cafe-timing/status/',
            },
        },
        'authentication': 'JWT Token Authentication (Bearer token in Authorization header)'
    })
