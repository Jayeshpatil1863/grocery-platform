from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField(max_length=300)
    class Meta:
        db_table="category"
        

from django import  forms 

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'