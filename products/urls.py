from django.contrib import admin
from django.urls import path
from .views import index, about_us

urlpatterns = [
    path('', index, name='index'),
    path('about_us/', about_us, name='about_us'),
]
