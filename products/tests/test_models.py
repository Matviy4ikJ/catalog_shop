import pytest

from .fixtures import *

from account.models import Profile
from products.models import Cart, Product, Category, CartItem, Order, OrderItem

from django.urls import reverse

from rest_framework.test import APIClient


@pytest.mark.django_db
def test_product_model():
    category = Category.objects.create(
        name='test_category'
    )
    product = Product.objects.create(
        name='test_product',
        category=category,
        nomenclature='test_nomenclature',
        price=100,
        discount=10
    )

    assert product.discount_price == 90
    assert product.category.name == 'test_category'


@pytest.mark.django_db
def test_cart_model_one_product(user, product):
    cart_item = CartItem.objects.create(
        cart=user.cart,
        product=product
    )

    assert cart_item.item_total == product.price
    assert user.cart.total == product.price


@pytest.mark.django_db
def test_cart_model_many_product(user, product):
    cart_item = CartItem.objects.create(
        cart=user.cart,
        product=product,
        amount=10
    )

    assert cart_item.item_total == product.price * 10
    assert user.cart.total == product.price * 10


@pytest.mark.django_db
def test_cart_model_discount_product(user, product_discount):
    cart_item = CartItem.objects.create(
        cart=user.cart,
        product=product_discount
    )

    assert cart_item.item_total == 80
    assert user.cart.total == 80


@pytest.mark.django_db
def test_cart_model_different_products(user):
    category = Category.objects.create(name="Test Category")

    product = Product.objects.create(
        name="Product A",
        price=100,
        category=category,
        nomenclature="unique_nomenclature_1"
    )

    product_discount = Product.objects.create(
        name="Product B",
        price=80,
        category=category,
        nomenclature="unique_nomenclature_2",
        discount=20
    )

    CartItem.objects.create(cart=user.cart, product=product_discount)
    CartItem.objects.create(cart=user.cart, product=product)

    assert user.cart.total == 164


@pytest.mark.django_db
def test_order_creation(order, product, product_discount):
    # order - фікстура, яка створює Order з двома OrderItem

    # Перевіряємо, що у замовлення два елементи
    assert order.items.count() == 2

    # Перевіряємо загальну суму замовлення:
    # OrderItem 1: price=100, amount=1 (за замовчуванням)
    # OrderItem 2: price=80, amount=2
    expected_total = 100 * 1 + 80 * 2
    assert order.total == expected_total

    # Перевіряємо, що строкове представлення order правильне
    assert str(order) == f'order #{order.id}'


@pytest.mark.django_db
def test_order_item_item_total(product, product_discount):
    order = Order.objects.create(
        user=None,
        contact_name='Test',
        contact_phone='1234567890',
        contact_email='test@example.com',
        address='Test Address',
    )

    # Створюємо OrderItem без знижки
    item1 = OrderItem.objects.create(
        order=order,
        product=product,
        price=product.price,
        amount=3
    )
    assert item1.item_total == product.price * 3

    # Створюємо OrderItem зі знижкою (discount_price)
    item2 = OrderItem.objects.create(
        order=order,
        product=product_discount,
        price=product_discount.discount_price,
        amount=2
    )
    assert item2.item_total == product_discount.discount_price * 2
