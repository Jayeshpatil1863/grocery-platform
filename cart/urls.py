
from .import views as v
from django.urls import path

app_name = 'cart'

urlpatterns = [
    path('add/<int:id>', v.add_to_cart, name='add'),
    path('viewcart', v.view_cart, name='viewcart'),
    path('increase/<int:id>', v.increase_quantity, name='increase'),
    path('decrease/<int:id>', v.decrease_quantity, name='decrease'),
    path('delete/<int:id>', v.delete_item, name='delete'),
]
