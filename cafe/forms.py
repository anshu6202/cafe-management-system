from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import TableBooking, MenuItem


class UserSignUpForm(UserCreationForm):
    """User signup form"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-input',
            'placeholder': 'Enter your email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-input',
            'placeholder': 'Enter username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-input',
            'placeholder': 'Enter password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-input',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class UserLoginForm(forms.Form):
    """User login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-input',
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-input',
            'placeholder': 'Enter password'
        })
    )


class TableBookingForm(forms.ModelForm):
    """Table booking form"""
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control form-input',
        })
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control form-input',
        })
    )

    class Meta:
        model = TableBooking
        fields = ['name', 'email', 'phone', 'date', 'time', 'number_of_people', 'special_requests']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-input',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-input',
                'placeholder': 'Your Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-input',
                'placeholder': 'Your Phone Number'
            }),
            'number_of_people': forms.NumberInput(attrs={
                'class': 'form-control form-input',
                'placeholder': '1',
                'min': '1',
                'max': '50'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control form-input',
                'placeholder': 'Any special requests?',
                'rows': 4
            }),
        }
