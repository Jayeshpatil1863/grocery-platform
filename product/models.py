from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=30)
    price=models.IntegerField()
    description=models.TextField(max_length=300)
    pimg = models.ImageField(upload_to='products/main/', blank=True, null=True)  
    unit=models.CharField(max_length=10,default='1')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering=['name']
        db_table='product'
        

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='extra_images'
    )
    image = models.ImageField(upload_to="images/extra")

    def __str__(self):
        return f"{self.product.name} – extra image"
    

from django import forms
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pimg'].required = False


