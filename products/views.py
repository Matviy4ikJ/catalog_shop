from django.shortcuts import render

from products.models import Product


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {"products": products})


def about_us(request):
    return render(request, 'about_us.html')
