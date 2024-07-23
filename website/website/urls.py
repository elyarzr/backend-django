from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls',namespace='home')),#url address for home app
    path('accounts/',include('accounts.urls',namespace='accounts')),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('cart/',include('cart.urls',namespace='cart')),
    path('order/',include('order.urls',namespace='order')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)










