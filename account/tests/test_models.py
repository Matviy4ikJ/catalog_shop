import pytest

from account.models import Profile
from products.models import Cart

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIClient


@pytest.mark.django_db
def test_profile_creation(user):
    profile = Profile.objects.get(user=user)
    profile.avatar = 'avatars/ArmA_3_Screenshot_2024.06.05_-_16.57.45.97.png'
    profile.save()
    cart = Cart.objects.get(user=user)

    assert str(profile.avatar) == 'avatars/ArmA_3_Screenshot_2024.06.05_-_16.57.45.97.png'
    assert profile.user == user
    assert cart.user == user
