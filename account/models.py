from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.db import models
from django.contrib.auth.models import User

from product.models import Product

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


 
class CustomUserCreationForm(UserCreationForm):
    contact_number = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('admin', 'Admin'), ('user', 'User')])

    class Meta:
        model = User
        fields = ['username', 'contact_number', 'email', 'password1', 'password2', 'role']


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
