# custom_filters.py

from django import template
from catalogue.seller.models import Category  # Update the import path as needed

register = template.Library()

@register.filter(name='filter_shop')
def filter_shop(categories, shop):
    return categories.filter(shop=shop)
