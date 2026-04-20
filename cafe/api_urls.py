"""
API URL Configuration for Cafe Management System
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api_views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    MenuItemViewSet,
    TableBookingViewSet,
    OrderViewSet,
    CafeTimingViewSet,
    api_root,
    api_docs,
)

# Create a router for viewsets
router = DefaultRouter()
router.register(r'menu', MenuItemViewSet, basename='menu')
router.register(r'bookings', TableBookingViewSet, basename='booking')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'cafe-timing', CafeTimingViewSet, basename='cafe-timing')

# Authentication URLs
auth_patterns = [
    path('register/', UserRegistrationView.as_view(), name='api_register'),
    path('login/', UserLoginView.as_view(), name='api_login'),
    path('logout/', UserLogoutView.as_view(), name='api_logout'),
    path('profile/', UserProfileView.as_view(), name='api_profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# API URL patterns
urlpatterns = [
    # Root API endpoint
    path('', api_root, name='api_root'),
    
    # Documentation
    path('docs/', api_docs, name='api_docs'),
    
    # Authentication endpoints
    path('auth/', include(auth_patterns)),
    
    # ViewSet routes
    path('', include(router.urls)),
]
