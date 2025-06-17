from django.contrib.auth.models import User
from rest_framework import serializers

from products.models import Order, OrderItem
from products.serializers.product_serializer import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError("Amount must be at least 1.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return getattr(obj, 'total', None)

    def validate_item(self, data):
        if not self.instance and not self.initial_data.get('items'):
            raise serializers.ValidationError("Order must contain at least one item.")
        return data

    class Meta:
        model = Order
        fields = '__all__'


class OrderCheckoutSerializer(serializers.ModelSerializer):
    payment_method = serializers.ChoiceField(choices=[
        ('liqpay', 'Pay with LiqPay'),
        ('monopay', 'Pay with MonoPay'),
        ('googlepay', 'Pay with Google Pay'),
        ('cash', 'With cash'),
    ])

    class Meta:
        model = Order
        fields = [
            'contact_name',
            'contact_email',
            'contact_phone',
            'address',
            'payment_method',
        ]
