import os
import pytest
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalog.catalog.settings')
django.setup()

from django.contrib.auth.models import User


@pytest.fixture
def user():
    return User.objects.create(
        username='test-user',
        password='1234'
    )
