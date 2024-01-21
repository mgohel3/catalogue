# Register your models here.
from django.contrib import admin
from .models import Category, Product, Banner, Shop, Seller

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Banner)
admin.site.register(Shop)
admin.site.register(Seller)