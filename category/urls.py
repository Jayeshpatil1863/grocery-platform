
from . import views as v
from django.urls import path,include


urlpatterns = [
    path('add',v.add_category,name="add"),
    path('list',v.category_list,name="list"),
 
]
