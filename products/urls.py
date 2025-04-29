from django.contrib import admin
from django.urls import path, include
from .views import index, about_us, product_details, cart_add, cart_detail_view, cart_remove, cart_update, checkout
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('about_us/', about_us, name='about_us'),
    path('product/<int:product_id>/', product_details, name='product_details'),
    path('captcha/', include('captcha.urls')),
    path('account/', include('account.urls')),
    path('cart_add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart_details/', cart_detail_view, name='cart_details'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', cart_update, name='cart_update'),
    path('checkout/', checkout, name='checkout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
