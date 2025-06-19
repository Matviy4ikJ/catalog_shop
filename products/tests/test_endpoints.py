import pytest

from django.urls import reverse

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


