# seller/urls.py
from django.contrib import admin  # Add this line to import the admin module
from django.urls import path
from .views import seller_registration, seller_login, seller_dashboard, seller_profile  # Make sure this import is present
from . import views  # Import the views module
from django.conf import settings
from django.conf.urls.static import static
from .views import shop_page, edit_shop, show_banners, all_banners, delete_banner, add_product, edit_product, edit_category

app_name = 'seller'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.seller_registration, name='register'),
    path('login/', views.seller_login, name='login'),
    path('logout/', views.seller_logout, name='logout'),
    path('dashboard/', views.seller_dashboard, name='dashboard'),
    path('all_product/', views.all_product, name='all_product'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_category/', views.add_category, name='add_category'),
    path('all_category/', views.all_category, name='all_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add_banner/', views.add_banner, name='add_banner'),
    path('show_banners/', views.show_banners, name='show_banner'),
    path('all_banners/', views.all_banners, name='all_banners'),
    path('delete_banner/<int:banner_id>/', delete_banner, name='delete_banner'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
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

