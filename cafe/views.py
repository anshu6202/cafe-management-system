from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime
from .models import MenuItem, TableBooking, CafeTiming
from .forms import UserSignUpForm, UserLoginForm, TableBookingForm


# ============ Helper Functions ============

def get_cafe_status():
    """Check if cafe is currently open or closed"""
    try:
        cafe = CafeTiming.objects.first()
        if not cafe:
            return None, None, None
        
        current_time = timezone.now().time()
        is_open = cafe.opening_time <= current_time <= cafe.closing_time
        
        return {
            'is_open': is_open,
            'opening_time': cafe.opening_time,
            'closing_time': cafe.closing_time,
            'status': 'OPEN' if is_open else 'CLOSED',
            'cafe_name': cafe.name
        }, cafe.opening_time, cafe.closing_time
    except:
        return None, None, None


def get_context_data(request):
    """Get common context data for all pages"""
    cafe_status, _, _ = get_cafe_status()
    return {
        'cafe_status': cafe_status,
        'user': request.user,
    }


# ============ Authentication Views ============

def signup(request):
    """User signup page"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = UserSignUpForm()
    
    context = get_context_data(request)
    context['form'] = form
    return render(request, 'signup.html', context)


def login_view(request):
    """User login page"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    context = get_context_data(request)
    context['form'] = form
    return render(request, 'login.html', context)


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


# ============ Main Pages ============

def home(request):
    """Home page with cafe info"""
    context = get_context_data(request)
    
    # Get menu items for the home page
    menu_items = MenuItem.objects.filter(is_available=True)[:8]  # Show 8 items on home page
    context['menu_items'] = menu_items
    
    # Handle auth forms
    form_login = UserLoginForm()
    form_signup = UserSignUpForm()
    
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:  # Login form
            form_login = UserLoginForm(request.POST)
            if form_login.is_valid():
                username = form_login.cleaned_data['username']
                password = form_login.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password.')
        elif 'email' in request.POST:  # Signup form
            form_signup = UserSignUpForm(request.POST)
            if form_signup.is_valid():
                user = form_signup.save()
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('home')
    
    context['form_login'] = form_login
    context['form_signup'] = form_signup
    
    return render(request, 'home.html', context)


def menu(request):
    """Menu page with filtering"""
    category = request.GET.get('category', 'all')
    search = request.GET.get('search', '').strip()
    
    # Get all menu items
    menu_items = MenuItem.objects.filter(is_available=True)
    
    # Filter by category
    if category != 'all':
        menu_items = menu_items.filter(category=category)
    
    # Search by name or description
    if search:
        menu_items = menu_items.filter(
            models.Q(name__icontains=search) | models.Q(description__icontains=search)
        )
    
    # Get unique categories
    categories = MenuItem.CATEGORY_CHOICES
    
    context = get_context_data(request)
    context.update({
        'menu_items': menu_items,
        'categories': categories,
        'selected_category': category,
        'search_query': search,
    })
    
    return render(request, 'menu.html', context)


def menu_detail(request, id):
    """Menu item detail page"""
    menu_item = get_object_or_404(MenuItem, id=id)
    
    # Get related items from same category
    related_items = MenuItem.objects.filter(
        category=menu_item.category,
        is_available=True
    ).exclude(id=menu_item.id)[:4]
    
    context = get_context_data(request)
    context.update({
        'menu_item': menu_item,
        'related_items': related_items,
    })
    
    return render(request, 'menu_detail.html', context)


# ============ Table Booking Views ============

def book_table(request):
    """Book a table page"""
    cafe_status, _, _ = get_cafe_status()
    
    if request.method == 'POST':
        form = TableBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            
            messages.success(request, 'Table booking successful! We will confirm your booking shortly.')
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = TableBookingForm()
    
    context = get_context_data(request)
    context.update({
        'form': form,
        'cafe_status': cafe_status,
    })
    
    return render(request, 'book_table.html', context)


def booking_success(request, booking_id):
    """Booking success page"""
    booking = get_object_or_404(TableBooking, id=booking_id)
    
    context = get_context_data(request)
    context['booking'] = booking
    
    return render(request, 'booking_success.html', context)


@login_required(login_url='login')
def booking_history(request):
    """User's booking history"""
    bookings = TableBooking.objects.filter(user=request.user)
    
    context = get_context_data(request)
    context['bookings'] = bookings
    
    return render(request, 'booking_history.html', context)


# ============ API Views for AJAX ============

def get_cafe_timing(request):
    """API endpoint to get cafe timing"""
    cafe_status, _, _ = get_cafe_status()
    
    if cafe_status:
        return JsonResponse({
            'status': cafe_status['status'],
            'is_open': cafe_status['is_open'],
            'opening_time': str(cafe_status['opening_time']),
            'closing_time': str(cafe_status['closing_time']),
        })
    
    return JsonResponse({'status': 'UNKNOWN'})


def search_menu(request):
    """AJAX search for menu items"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    items = MenuItem.objects.filter(
        models.Q(name__icontains=query) | models.Q(description__icontains=query),
        is_available=True
    )[:10]
    
    results = [
        {
            'id': item.id,
            'name': item.name,
            'price': str(item.price),
            'category': item.get_category_display(),
            'image_url': item.image.url if item.image else '/static/images/placeholder.jpg',
        }
        for item in items
    ]
    
    return JsonResponse({'results': results})


# ============ Import django models for search functionality ============
from django.db import models
