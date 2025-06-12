import pytest
import pytest_check as check

from .fixtures import *

from products.serializers.product_serializer import ProductSerializer


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
        'name': '*'*101,
        'description': {},
        'entity': -3,
        'price': -100,
        'available': 15,
        'category': 9999999999,
        'nomenclature': '*'*101,
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


@pytest.mark.django_db
def test_products_serializer_read_only(category):
    data = {
        'name': 'test-name',
        'description': 'test-description',
        'entity': 10,
        'price': 50,
        'stock': 100,
        'available': False,
        'category': category.id,
        'nomenclature': 'test-nomenclature',
        'rating': 5,
        'discount': 20,
        'attributes': {}
    }

    serializer = ProductSerializer(data=data)
    assert serializer.is_valid()

    product = serializer.save()

    serializer2 = ProductSerializer(product)

    assert "category" not in serializer2.data
