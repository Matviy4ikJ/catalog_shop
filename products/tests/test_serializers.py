import pytest
import pytest_check as check

from .fixtures import *

from products.serializers.product_serializer import ProductSerializer
from products.serializers.order_serializer import OrderSerializer


@pytest.mark.django_db
def test_product_serializer_valid(category):
    data = {
        'name': 'test-name',
        'description': 'test-description',
        'entity': 10,
        'price': 50,
        'available': False,
        'category': category.id,
        'nomenclature': 'test-nomenclature',
        'rating': 5,
        'discount': 20,
        'attributes': {}
    }

    serializer = ProductSerializer(data=data)

    assert serializer.is_valid()
    assert not serializer.errors


@pytest.mark.django_db
def test_product_serializer_invalid(category):
    data = {
        'name': '*' * 101,
        'description': {},
        'entity': -3,
        'price': -100,
        'available': 15,
        'nomenclature': '*' * 101,
        'rating': '*',
        'discount': -10,
        'attributes': '*'
    }

    serializer = ProductSerializer(data=data)

    assert not serializer.is_valid()
    assert serializer.errors
    assert 'Ensure this field has no more than 50 characters.' in serializer.errors['name']
    assert 'Must be a valid boolean.' in serializer.errors['available']
    assert 'Ensure this field has no more than 50 characters.' in serializer.errors['nomenclature']
    assert 'A valid number is required.' in serializer.errors['rating']

    for field in data.keys():
        assert field in serializer.errors


# @pytest.mark.django_db
# def test_products_serializer_read_only(category):
#     data = {
#         'name': 'test-name',
#         'description': 'test-description',
#         'entity': 10,
#         'price': 50,
#         'stock': 100,
#         'available': False,
#         'category': category.id,
#         'nomenclature': 'test-nomenclature',
#         'rating': 5,
#         'discount': 20,
#         'attributes': {}
#     }
#
#     serializer = ProductSerializer(data=data)
#
#     assert serializer.is_valid()
#     assert "category" not in serializer.data


@pytest.mark.django_db
def test_products_serializer_method_field(product_discount):
    serializer = ProductSerializer(product_discount)

    assert serializer.data['discount_price'] == product_discount.discount_price
    assert serializer.data['discount_price'] == 80


@pytest.mark.django_db
def test_order_serializer_read_only(user, order):
    data = {
        'user': user.id,
        'contact_name': 'test-name',
        'contact_email': 'testemail@gmail.com',
        'contact_phone': '3859475892',
        'address': 'test-address',
    }

    serializer = OrderSerializer(data=data)

    assert serializer.is_valid()
    assert "items" not in serializer.validated_data

    serializer = OrderSerializer(order)

    assert 'items' in serializer.data


@pytest.mark.django_db
def test_order_serializer_items(order):
    serializer = OrderSerializer(order)
    items = serializer.data['items']

    assert len(items) == 2

