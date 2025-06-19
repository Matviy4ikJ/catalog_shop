import os
import pytest
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_catalog.catalog.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def user():
    return User.objects.create(
        username='test-user',
        password='1234'
    )


@pytest.fixture
def api_client():
    apiclient = APIClient()
    return apiclient
