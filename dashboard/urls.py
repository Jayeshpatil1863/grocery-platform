from django.urls import path
from . import views as v
from django.contrib.auth import views as auth_views

app_name = 'dashboard'

urlpatterns = [ 
    path('jayesh',v.jayesh),
    # path('admin_home', v.admin_home),
    path('', v.admin_home, name='admin_home'),
    path('admin_search/', v.admin_search, name='admin_search'),
    path('admin_list',v.admin_product_list,name="admin_list"),
    path('orders/', v.admin_order_list, name='orders'),
    path("admin_order_edit/<int:id>/",v.admin_order_edit,name="admin_order_edit"),
    path("admin_order_delete/<int:id>/",v.admin_order_delete,name="admin_order_delete"),
    path("products/",v.Products,name="products"),
    path("users/",v.Users,name="users"),
    path("user_delete/<int:id>/",v.user_delete,name="user_delete"),
    path("user_edit/<int:id>/",v.user_edit,name="user_edit"), 
] 
 