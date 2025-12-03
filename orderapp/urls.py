from django.conf import settings
from django.urls import path
from . import views

from django.conf.urls.static import static

app_name = 'orderapp'

urlpatterns = [
    path('place/', views.place_order, name='place'),
    path('my', views.my_orders, name='my'),
    path('all/', views.all_orders, name='all_orders'),
    path('update/<int:id>/', views.update_order_status, name='update'),
    path('delete/<int:id>/', views.delete_order, name='delete'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/', views.order_success, name='success'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)