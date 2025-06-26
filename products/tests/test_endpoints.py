import pytest
import uuid

from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal

from products.models import Product
from .fixtures import *


@pytest.mark.django_db
def test_products_list_empty(api_client):
    url = reverse('products:product-list')

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_products_list(api_client, product, product_discount):
    url = reverse('products:product-list')

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_products_detail(api_client, product):
    url = reverse('products:product-detail', kwargs={'pk': product.id})

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['name'] == product.name


@pytest.mark.django_db
def test_product_detail_not_found(api_client):
    url = reverse('products:product-detail', kwargs={'pk': 9999})

    response = api_client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_product_update_not_authorized(api_client, product):
    url = reverse('products:product-detail', kwargs={'pk': product})

    response = api_client.patch(url, data={'price': 82})

    assert response.status_code == 403


@pytest.mark.django_db
def test_product_update_authorized(api_client, product, superuser):
    api_client.force_authenticate(superuser)

    url = reverse('products:product-detail', kwargs={'pk': product.id})

    response = api_client.patch(url, data={'price': 82})

    assert response.status_code == 200
    assert Decimal(response.data.get('price')) == Decimal('82.00')
    product.refresh_from_db()
    assert product.price == Decimal('82.00')


@pytest.mark.django_db
def test_product_create_authorized(api_client, category, superuser):
    url = reverse('products:product-list')
    data = {
        'name': 'test-name',
        'description': 'test-description',
        'category': category.id,
        'nomenclature': str(uuid.uuid4()),
        'price': 100,
    }
    api_client.force_authenticate(superuser)

    response = api_client.post(url, data=data)

    print('Response data:', response.data)
    print('Product ID:', response.data.get('id'))

    assert response.status_code == 201
    assert response.data.get('name') == 'test-name'
    assert Product.objects.filter(id=response.data.get('id')).exists()


