
from . import views as v
from django.urls import path,include


urlpatterns = [
    path('add',v.add_product,name="add"),
    path('cart/', include('cart.urls')),
    path('list',v.product_list,name="list"),
    path('search',v.product_search,name="search"),
    path('delete/<int:id>',v.delete_product,name="delete"),
    path('edit/<int:id>',v.edit_product,name="edit"),
 
]
