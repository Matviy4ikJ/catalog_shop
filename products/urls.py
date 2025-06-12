from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.views import index, about_us, product_details, cart_add, cart_detail_view, cart_remove, cart_update, checkout
from .views.product import ProductViewSet
from .views.category import CategoryViewSet
from .views.cart import CartViewSet

from django.conf.urls.static import static
from django.conf import settings


router = DefaultRouter()
router.register(r'products', viewset=ProductViewSet)
router.register(r'categories', viewset=CategoryViewSet)
router.register(r'carts', viewset=CartViewSet, basename='carts')

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
    path('checkout/', checkout, name='checkout'),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        # path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    ]
