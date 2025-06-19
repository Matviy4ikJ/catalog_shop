import pytest

from products.models import Category, Product, Order, OrderItem


@pytest.fixture()
def category():
    return Category.objects.create(
        name='test-category'
    )


@pytest.fixture
def product():

    category_product = Category.objects.create(
        name='category-test'
    )

    return Product.objects.create(
        name='test-product',
        category=category_product,
        nomenclature='test-nomenclature-product',
        price=100,
    )


@pytest.fixture
def product_discount():

    category_product_discount = Category.objects.create(
        name='category-test2'
    )

    return Product.objects.create(
        name='test-product',
        category=category_product_discount,
        nomenclature='test-nomenclature-discount',
        price=100,
        discount=20
    )


@pytest.fixture
def order(user, product, product_discount):
    data_order = Order.objects.create(
        user=user,
        contact_name='test-conctact',
        contact_phone='9754738927',
        contact_email='test-email@gmail.com',
        address='test-address',
    )

    OrderItem.objects.create(
        order=data_order,
        product=product,
        price=100,
    )

    OrderItem.objects.create(
        order=data_order,
        product=product_discount,
        amount=2,
        price=80
    )

    return data_order
