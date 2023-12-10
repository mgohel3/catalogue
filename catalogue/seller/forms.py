# seller/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Seller
from django.contrib.auth.forms import AuthenticationForm

class SellerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number']

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['first_name', 'last_name', 'email', 'phone_number']
