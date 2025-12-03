
from django.contrib import admin
from django.urls import path,include
from account.views import home
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',home),
    path('',include('dashboard.urls')),
    path('dashboard/', include(('dashboard.urls','dashboard'), namespace='dashboard')),
    path('admin/', admin.site.urls),
    path('account/',include(('account.urls','account'),namespace='account')),
    path('category/',include(('category.urls','category'),namespace='category')),
    path('product/',include(('product.urls','product'),namespace='product')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('order/', include('orderapp.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

