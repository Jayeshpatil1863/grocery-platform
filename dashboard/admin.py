from django.contrib import admin
from .models import *
from product.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'unit')
    search_fields = ('name', 'description')