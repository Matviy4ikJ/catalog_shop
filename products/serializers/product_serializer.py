import json

from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field, OpenApiTypes

from rest_framework import serializers

from ..models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'entity',
            'price',
            'stock',
            'available',
            'category',
            'nomenclature',
            'created_at',
            'rating',
            'discount',
            'attributes',
            'discount_price',
        ]

    def get_discount_price(self, obj):
        return getattr(obj, "discount_price", None)

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Price should be greater than 0.')
        return value

    def validate_description(self, value):
        if isinstance(value, str):
            return value
        raise serializers.ValidationError('Description must be a text.')

    def validate_category(self, value):
        if not (isinstance(value, str) or isinstance(value, Category)):
            raise serializers.ValidationError('Category must be int or category instance.')
        return value

    def validate_discount(self, value):
        if value < 0:
            raise serializers.ValidationError('Discount should be greater than 0.')
        return value

    def validate_rating(self, value):
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError('Rating must be a number.')
        return value

    def validate_attributes(self, value):
        if not value:
            return value

        if isinstance(value, dict):
            return value

        try:
            return json.loads(value)
        except Exception:
            raise serializers.ValidationError('The attributes must be a valid JSON')
