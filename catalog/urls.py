from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls', namespace='products')),
    path('account/', include('account.urls', namespace='account')),
    path("captcha/", include("captcha.urls")),
]

