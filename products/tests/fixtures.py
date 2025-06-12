import pytest

from products.models import Category, Product


@pytest.fixture()
def category():
    return Category.objects.create(
        name='test-category'
    )


@pytest.fixture
def product(category):
    return Product.objects.create(
        name='test-product',
        category=category,
        nomenclature='test-nomenclature',
        price=100,
    )


@pytest.fixture
def product_discount(category):
    return Product.objects.create(
        name='test-product',
        category=category,
        nomenclature='test-nomenclature',
        price=100,
        discount=20
    )
