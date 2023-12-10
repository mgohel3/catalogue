# seller/urls.py
from django.contrib import admin  # Add this line to import the admin module
from django.urls import path
from .views import seller_registration, seller_login, seller_dashboard, seller_profile  # Make sure this import is present
from . import views  # Import the views module

app_name = 'seller'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.seller_registration, name='register'),
    path('login/', views.seller_login, name='login'),
    path('logout/', views.seller_logout, name='logout'),
    path('dashboard/', views.seller_dashboard, name='dashboard'),
    path('profile/', views.seller_profile, name='profile'),
    path('features/', views.features, name='features'),
    path('solutions/', views.solutions, name='solutions'),
    path('pricing/', views.pricing, name='pricing'),
    # Add more URL patterns for other seller views if needed
]
