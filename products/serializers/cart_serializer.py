from django.contrib.auth.models import User
from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field, OpenApiExample, extend_schema_serializer
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


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Simple Cart Example',
            summary='Example of Cart with items',
            value={
                "user": None,
                "created_at": None,
                "items": [
                    {
                        "cart": None,
                        "product": {
                            "name": "Sample Product",
                            "description": "A simple product",
                            "entity": 1,
                            "price": "100.00",
                            "stock": 5,
                            "available": True,
                            "category": 1,
                            "nomenclature": "SP001",
                            "created_at": "2025-06-17T00:00:00Z",
                            "rating": 4,
                            "discount": 10,
                            "attributes": {"color": "red"},
                            "discount_price": 90.0
                        },
                        "item_total": 180.0,
                        "amount": 2
                    }
                ],
                "total": 180.0
            }
        )
    ]
)
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['user', 'created_at', 'items', 'total']

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_total(self, obj):
        return obj.total


class CartItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField(min_value=1)
