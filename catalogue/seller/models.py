# seller/models.py
from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    media = models.ImageField(upload_to='product_media/%Y/%m/%d/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.id})"


class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='company_logos/%Y/%m/%d/', max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    official_email = models.EmailField(max_length=100, null=True, blank=True)
    official_address = models.TextField(null=True, blank=True)
    tax_gst_number = models.CharField(max_length=50, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True, related_name='shops')

    def __str__(self):
        return f"{self.name} ({self.id})"

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    # Add any additional fields for the seller profile if needed

    def __str__(self):
        return f"{self.user.username} ({self.id})"
