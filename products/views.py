from django.shortcuts import render, get_object_or_404

from products.models import Product, Category


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_name = request.GET.get('category')
    filter_name = request.GET.get('filter')
    product_name = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if product_name:
        products = products.filter(name__icontains=product_name)

    if category_name:
        category = Category.objects.get(name=category_name)
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    match filter_name:
        case "price_increase":
            products = products.order_by("price")

        case "price_decrease":
            products = products.order_by("-price")

        case "rating_increase":
            products = products.order_by("rating")

        case "rating_decrease":
            products = products.order_by("-rating")

        case "date_newest":
            products = products.order_by("-created_at")

        case "date_oldest":
            products = products.order_by("created_at")

    return render(
        request,
        "index.html",
        {"products": products, "categories": categories},
    )


def about_us(request):
    return render(request, 'about_us.html')


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})
