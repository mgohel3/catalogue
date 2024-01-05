# seller/forms.py
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Seller
from .models import Shop
from .models import Product

class SellerRegistrationForm(UserCreationForm):
    business_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'business_name', 'email', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SellerRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['first_name', 'last_name', 'email', 'phone_number']

# forms.py
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['logo', 'name', 'description', 'contact_number', 'official_email', 'official_address', 'tax_gst_number']

class ShopEditForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['logo', 'name', 'description', 'contact_number', 'official_email', 'official_address', 'tax_gst_number']

class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'media', 'price']


