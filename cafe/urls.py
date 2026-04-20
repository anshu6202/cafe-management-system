from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Main Pages
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('menu/<int:id>/', views.menu_detail, name='menu_detail'),
    
    # Booking
    path('book-table/', views.book_table, name='book_table'),
    path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.booking_history, name='booking_history'),
    
    # API Endpoints
    path('api/cafe-timing/', views.get_cafe_timing, name='get_cafe_timing'),
    path('api/search-menu/', views.search_menu, name='search_menu'),
]
