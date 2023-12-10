# seller/models.py
from django.contrib.auth.models import User
from django.db import models

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    # Add any additional fields for the seller profile if needed

    def __str__(self):
        return self.user.username