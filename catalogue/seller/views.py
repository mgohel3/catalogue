# seller/views.py
from django.shortcuts import render, redirect
from .forms import SellerRegistrationForm, SellerProfileForm
from .models import Seller
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404



def home(request):
    show_header_and_footer = True
    page_title = 'Home'
    return render(request, 'seller/home.html',{'show_header_and_footer': show_header_and_footer})

def seller_registration(request):
    show_header_and_footer = False
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            seller = Seller.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number']
            )
            # Redirect to the seller dashboard after successful registration
            return redirect('seller:dashboard')
    else:
        form = SellerRegistrationForm()
    return render(request, 'seller/registration.html', {'form': form, 'show_header_and_footer': show_header_and_footer})

def seller_login(request):
    is_login_page = True  # Add this variable to indicate the login page
    show_header_and_footer = False
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the seller dashboard after successful login
                return redirect('seller:dashboard')
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'seller/login.html', {'form': form, 'is_login_page': is_login_page,'show_header_and_footer': show_header_and_footer})

def seller_logout(request):
    logout(request)
    messages.success(request, ("You are Logged out"))
    return redirect('home')

def seller_dashboard(request):
    # Add logic for the dashboard here
    show_header_and_footer = False
    return render(request, 'seller/dashboard.html', {'show_header_and_footer': show_header_and_footer})

@login_required
def seller_profile(request):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        if request.method == 'POST':
            form = SellerProfileForm(request.POST)
            if form.is_valid():
                form.save()
                # Optionally, you can add a success message here
                return redirect('seller:profile')
        else:
            form = SellerProfileForm()

        return render(request, 'seller/profile.html', {'form': form})

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=seller)
        if form.is_valid():
            form.save()
            # Optionally, you can add a success message here
            return redirect('seller:profile')
    else:
        form = SellerProfileForm(instance=seller)

    return render(request, 'seller/profile.html', {'form': form})

def features(request):
    show_header_and_footer = True
    page_title = 'features'
    return render(request, 'seller/features.html',{'show_header_and_footer': show_header_and_footer})

def solutions(request):
    show_header_and_footer = True
    page_title = 'solutions'
    return render(request, 'seller/solutions.html',{'show_header_and_footer': show_header_and_footer})

def pricing(request):
    show_header_and_footer = True
    page_title = 'Pricing'
    return render(request, 'seller/pricing.html',{'show_header_and_footer': show_header_and_footer})

def sidebar(request):
    show_header_and_footer = False
    page_title = ''
    return render(request, 'seller/sidebar.html',{'show_header_and_footer': show_header_and_footer})
