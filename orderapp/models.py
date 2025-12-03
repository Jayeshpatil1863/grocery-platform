from django.db import models
from django.contrib.auth.models import User
from product.models import Product

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Packed', 'Packed'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
]

DELIVERY_SLOTS = [
    ('Morning', 'Morning (8am-12pm)'),
    ('Afternoon', 'Afternoon (12pm-4pm)'),
    ('Evening', 'Evening (4pm-8pm)'),
]


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='order_images/', null=True, blank=True)  # ✔ NEW
    address = models.ForeignKey("Address", on_delete=models.CASCADE, null=True, blank=True) # ✔ NEW
    product_name = models.CharField(max_length=30, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_slot = models.CharField(max_length=20, choices=DELIVERY_SLOTS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'order'

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_slot']
        



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.address_line}, {self.city}"
    


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'address_line', 'city', 'pincode']