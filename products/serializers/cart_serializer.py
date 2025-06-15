from django.contrib.auth.models import User
from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from ..models import Cart, CartItem
from ..serializers.product_serializer import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'item_total', 'amount']

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError("Amount must be at least 1.")
        return value

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_item_total(self, obj):
        return obj.item_total


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cart_items', many=True)

    class Meta:
        model = Cart
        extra_kwargs = {'total': {'required': True}}
        fields = ['user', 'created_at', 'items', 'total']

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_total(self, obj):
        return obj.total
