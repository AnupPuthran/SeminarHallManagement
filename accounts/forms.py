from django import forms
from django.contrib.auth.models import User
from .models import SeminarHall, Booking


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password']


class SeminarHallForm(forms.ModelForm):

    class Meta:
        model = SeminarHall
        fields = [
            'hall_name',
            'capacity',
            'location',
            'description',
            'image'
        ]


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['hall', 'booking_date', 'start_time', 'end_time']