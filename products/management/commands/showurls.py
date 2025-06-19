from django.urls import get_resolver
from django.core.management.base import BaseCommand

for name in get_resolver().reverse_dict.keys():
    if isinstance(name, str):
        print(name)
