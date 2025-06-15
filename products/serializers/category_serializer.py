from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Category name must be at least 3 characters long.")
        return value