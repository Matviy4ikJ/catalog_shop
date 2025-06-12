import pytest

from .fixtures import *

from account.models import Profile
from products.models import Cart, Product, Category, CartItem

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
