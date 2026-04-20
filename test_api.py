"""
Example Python Script to Test the Cafe Management API
This script demonstrates how to interact with the API using the requests library
"""

import requests
import json
from datetime import datetime, timedelta

# Base URL
BASE_URL = "http://localhost:8000/api"

# Store tokens for use across requests
ACCESS_TOKEN = None
REFRESH_TOKEN = None

def print_response(response, title="Response"):
    """Pretty print response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print()


def test_registration():
    """Test user registration"""
    url = f"{BASE_URL}/auth/register/"
    
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123",
        "password2": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(url, json=data)
    print_response(response, "USER REGISTRATION")
    return response.json() if response.status_code == 201 else None


def test_login():
    """Test user login and get JWT token"""
    global ACCESS_TOKEN, REFRESH_TOKEN
    
    url = f"{BASE_URL}/auth/login/"
    
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = requests.post(url, json=data)
    print_response(response, "USER LOGIN")
    
    if response.status_code == 200:
        result = response.json()
        ACCESS_TOKEN = result.get('access')
        REFRESH_TOKEN = result.get('refresh')
        print(f"✓ Access Token: {ACCESS_TOKEN[:50]}...")
        print(f"✓ Refresh Token: {REFRESH_TOKEN[:50]}...")
    
    return response


def test_get_profile():
    """Test getting user profile"""
    url = f"{BASE_URL}/auth/profile/"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    print_response(response, "GET USER PROFILE")
    return response


def test_update_profile():
    """Test updating user profile"""
    url = f"{BASE_URL}/auth/profile/"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "first_name": "Updated",
        "last_name": "Name"
    }
    
    response = requests.patch(url, json=data, headers=headers)
    print_response(response, "UPDATE USER PROFILE")
    return response


def test_get_all_menu():
    """Test getting all menu items"""
    url = f"{BASE_URL}/menu/"
    
    response = requests.get(url)
    print_response(response, "GET ALL MENU ITEMS")
    return response


def test_search_menu():
    """Test searching menu items"""
    url = f"{BASE_URL}/menu/search/?q=coffee"
    
    response = requests.get(url)
    print_response(response, "SEARCH MENU (q=coffee)")
    return response


def test_get_menu_by_category():
    """Test getting menu by category"""
    url = f"{BASE_URL}/menu/by_category/?category=coffee"
    
    response = requests.get(url)
    print_response(response, "GET MENU BY CATEGORY (coffee)")
    return response


def test_get_available_menu():
    """Test getting available menu items"""
    url = f"{BASE_URL}/menu/available/"
    
    response = requests.get(url)
    print_response(response, "GET AVAILABLE MENU ITEMS")
    return response


def test_get_single_menu(menu_id=1):
    """Test getting a single menu item"""
    url = f"{BASE_URL}/menu/{menu_id}/"
    
    response = requests.get(url)
    print_response(response, f"GET SINGLE MENU ITEM (ID: {menu_id})")
    return response


def test_create_booking():
    """Test creating a table booking"""
    url = f"{BASE_URL}/bookings/"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Calculate future date and time
    future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    future_time = "18:30"
    
    data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "phone": "123-456-7890",
        "date": future_date,
        "time": future_time,
        "number_of_people": 4,
        "special_requests": "Window seat if possible"
    }
    
    response = requests.post(url, json=data, headers=headers)
    print_response(response, "CREATE TABLE BOOKING")
    
    if response.status_code == 201:
        booking_id = response.json().get('booking', {}).get('id')
        return booking_id
    return None


def test_get_my_bookings():
    """Test getting user's bookings"""
    url = f"{BASE_URL}/bookings/my_bookings/"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    print_response(response, "GET MY BOOKINGS")
    return response


def test_get_single_booking(booking_id):
    """Test getting a single booking"""
    url = f"{BASE_URL}/bookings/{booking_id}/"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    print_response(response, f"GET SINGLE BOOKING (ID: {booking_id})")
    return response


def test_update_booking(booking_id):
    """Test updating a booking"""
    url = f"{BASE_URL}/bookings/{booking_id}/"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "time": "19:00",
        "number_of_people": 5
    }
    
    response = requests.patch(url, json=data, headers=headers)
    print_response(response, f"UPDATE BOOKING (ID: {booking_id})")
    return response


def test_cancel_booking(booking_id):
    """Test canceling a booking"""
    url = f"{BASE_URL}/bookings/{booking_id}/"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.delete(url, headers=headers)
    print_response(response, f"CANCEL BOOKING (ID: {booking_id})")
    return response


def test_get_cafe_timing():
    """Test getting cafe timing"""
    url = f"{BASE_URL}/cafe-timing/"
    
    response = requests.get(url)
    print_response(response, "GET CAFE TIMING")
    return response


def test_get_cafe_status():
    """Test getting cafe open/closed status"""
    url = f"{BASE_URL}/cafe-timing/status/"
    
    response = requests.get(url)
    print_response(response, "GET CAFE STATUS")
    return response


def test_api_root():
    """Test API root endpoint"""
    url = f"{BASE_URL}/"
    
    response = requests.get(url)
    print_response(response, "API ROOT")
    return response


def test_api_docs():
    """Test API documentation endpoint"""
    url = f"{BASE_URL}/docs/"
    
    response = requests.get(url)
    print_response(response, "API DOCUMENTATION")
    return response


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("CAFE MANAGEMENT API - TEST SCRIPT")
    print("="*60)
    
    # Test 1: Get API root
    test_api_root()
    
    # Test 2: User Registration
    test_registration()
    
    # Test 3: User Login
    test_login()
    
    # Test 4: Get Profile
    test_get_profile()
    
    # Test 5: Update Profile
    test_update_profile()
    
    # Test 6: Get All Menu Items
    test_get_all_menu()
    
    # Test 7: Get Single Menu Item
    test_get_single_menu(1)
    
    # Test 8: Search Menu
    test_search_menu()
    
    # Test 9: Get Menu by Category
    test_get_menu_by_category()
    
    # Test 10: Get Available Menu
    test_get_available_menu()
    
    # Test 11: Get Cafe Timing
    test_get_cafe_timing()
    
    # Test 12: Get Cafe Status
    test_get_cafe_status()
    
    # Test 13: Create Booking
    booking_id = test_create_booking()
    
    if booking_id:
        # Test 14: Get My Bookings
        test_get_my_bookings()
        
        # Test 15: Get Single Booking
        test_get_single_booking(booking_id)
        
        # Test 16: Update Booking
        test_update_booking(booking_id)
        
        # Test 17: Cancel Booking
        test_cancel_booking(booking_id)
    
    # Test 18: Get API Docs
    test_api_docs()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()
