from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    product=models.CharField(max_length=30)
    name=models.CharField(max_length=30)
    image = models.ImageField(upload_to='cart_images/')
    price=models.IntegerField()
    quantity=models.IntegerField()
    total_price=models.IntegerField(default=0)
    
    class Meta:
        db_table='cart'

from django import forms

class CartForm(forms.ModelForm):
    class Meta:
        model=Cart
        fields='__all__'


    

