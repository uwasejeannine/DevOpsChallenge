from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Booking, UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone"]


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []  # No fields needed as we'll set user and fitness_class in the view
