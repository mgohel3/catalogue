# seller/urls.py
from django.contrib import admin  # Add this line to import the admin module
from django.urls import path
from .views import seller_registration, seller_login, seller_dashboard, seller_profile  # Make sure this import is present
from . import views  # Import the views module
from django.conf import settings
from django.conf.urls.static import static
from .views import shop_page
from .views import add_product



app_name = 'seller'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.seller_registration, name='register'),
    path('login/', views.seller_login, name='login'),
    path('logout/', views.seller_logout, name='logout'),
    path('dashboard/', views.seller_dashboard, name='dashboard'),
    path('all_product/', views.all_product, name='all_product'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('profile/', views.seller_profile, name='profile'),
    path('features/', views.features, name='features'),
    path('solutions/', views.solutions, name='solutions'),
    path('pricing/', views.pricing, name='pricing'),
    path('settings/', views.settings, name='settings'),
    path('settings_plan/', views.settings_plan, name='settings_plan'),
    path('create_shop/', views.create_shop, name='create_shop'),
    path('<str:business_name>/edit_shop/', views.edit_shop, name='edit_shop'),  # Assuming the view name is edit_shop
    path('<str:business_name>/', shop_page, name='shop_page'),  # Assuming the view name is shop_page


    # Add more URL patterns for other seller views if needed
]

