from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from rest_framework import viewsets, filters

from ..forms import OrderCreateForm
from ..models import Product, Category, Cart, CartItem, OrderItem, Order


def calculate_discount(value, arg):
    discount_value = value * arg / 100
    return value - discount_value


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


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})

        if cart.get(str(product_id)):  # ключі сесії — це рядки
            cart[str(product_id)] += 1
        else:
            cart[str(product_id)] = 1

        request.session[settings.CART_SESSION_ID] = cart
        return redirect('cart_details')
    else:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.amount += 1
            cart_item.save()

        return redirect('cart_details')


def cart_detail_view(request):
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_items = []
        total_price = 0
        for product in products:
            count = cart[str(product.id)]
            price = count * product.price
            total_price += price

            cart_items.append({
                'product': product,
                'count': count,
                'price': price
            })
        return render(request,
                      'cart_detail.html',
                      {'cart_items': cart_items,
                       'total_price': total_price}
                      )

    else:
        try:
            cart = request.user.cart
        except Cart.DoesNotExist:
            cart = None

        if not cart or not cart.items.count:
            cart_items = []
            total_price = 0
        else:
            cart_items = cart.items.select_related('product').all
            total_price = sum(item.product.price * item.amount for item in cart_items)

        return render(request,
                      'cart_detail.html',
                      {'cart_items': cart_items,
                       'total_price': total_price
                       })


def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        product_id_str = str(product_id)

        if product_id_str in cart:
            del cart[product_id_str]
            request.session[settings.CART_SESSION_ID] = cart

    else:
        cart = get_object_or_404(Cart, user=request.user)
        CartItem.objects.filter(cart=cart, product=product).delete()

    return redirect('cart_details')


def cart_update(request, product_id):
    count = int(request.GET.get('count', 1))
    product = get_object_or_404(Product, id=product_id)

    if count < 1:
        return redirect('cart_remove', product_id=product_id)

    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        cart[str(product_id)] = count
        request.session[settings.CART_SESSION_ID] = cart
    else:
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.amount = count
        cart_item.save()

    return redirect('cart_details')


def checkout(request):
    if (request.user.is_authenticated and not getattr(request.user, 'cart', None)) or (
            not request.user.is_authenticated and not request.session.get(settings.CART_SESSION_ID)):
        messages.error(request, 'Cart is empty')

    if request.method == 'GET':
        form = OrderCreateForm()
        if request.user.is_authenticated:
            form.initial['contact_email'] = request.user.email

    elif request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            cart_items = []

            if request.user.is_authenticated:
                cart = getattr(request.user, 'cart', None)
                cart_items = cart.items.select_related('product').all()
                items = OrderItem.objects.bulk_create([
                    OrderItem(
                        order=order,
                        product=item.product,
                        amount=item.amount,
                        price=calculate_discount(item.product.price, item.product.discount)
                    ) for item in cart_items
                ]
                )
                OrderItem.objects.bulk_create([
                    OrderItem(
                        order=order,
                        product=item.product,
                        amount=item.amount,
                        price=calculate_discount(item.product.price, item.product.discount)
                    ) for item in cart_items
                ]
                )
                total_price = sum(item.product.price*item.amount)
                method = form.cleaned_data.get('payment_method')
                if method != 'cash':
                    Payment.objects.create(order=order, provider=method, amount=total_price)

                cart.items.all().delete()

            else:
                cart = request.session.get(settings.CART_SESSION_ID)
                for product_id, amount in cart.items():
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        amount=amount,
                        price=calculate_discount(product.price, product.discount)
                    )
                request.session[settings.CART_SESSION_ID] = {}

            messages.success(request, 'thx')
            return redirect('index')

    else:
        form = OrderCreateForm()

    return render(request, 'html', {'form': form})
