# seller/models.py
from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.core.files.storage import default_storage

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subcategories')
    description = models.TextField(null=True, blank=True)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    media = models.ImageField(upload_to='product_media/%Y/%m/%d/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.id})"


class Banner(models.Model):
    image = models.ImageField(
        upload_to='seller_banners/%Y/%m/%d/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        ]
    )
    shop = models.ForeignKey('shop', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Banner ({self.id})"

    def compress_image(self, max_file_size):
        # Check if the image file exists before opening it
        if default_storage.exists(self.image.name):
            # Open the uploaded image using PIL
            img = Image.open(self.image.path)

            # Check if the image is in RGBA mode and convert to RGB if necessary
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            # Resize the image if its size exceeds the maximum allowed file size
            if img.size[0] * img.size[1] > max_file_size:
                # Calculate the new dimensions while maintaining the original aspect ratio
                aspect_ratio = img.size[0] / img.size[1]
                new_width = int((max_file_size / 2) ** 0.5)
                new_height = int(new_width / aspect_ratio)

                # Resize the image
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

            # Save the compressed image back to the same path
            img.save(self.image.path, 'JPEG', quality=90)

    def save(self, *args, **kwargs):
        # Call the compress_image method before saving
        self.compress_image(max_file_size=2 * 1024 * 1024)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '1. Banners'

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
    banners = models.ManyToManyField(Banner, blank=True, related_name='shops')
    Category = models.ManyToManyField(Category, blank=True, related_name='shops')
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
