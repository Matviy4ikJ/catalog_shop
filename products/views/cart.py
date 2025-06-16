from django.conf import settings
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from ..models import Cart, CartItem, Product, Order, OrderItem, Payment
from ..serializers.cart_serializer import CartSerializer
from ..serializers.product_serializer import ProductSerializer
from ..forms import OrderCreateForm
from utils.email import send_order_confirmation_email


@extend_schema_view(
    add=extend_schema(
        summary="Add product to cart",
        description="Adds the specified product to the cart (for authenticated users or stored in session).",
        parameters=[
            OpenApiParameter(name='product_id', required=True, location=OpenApiParameter.PATH, type=int),
        ],
        responses={
            200: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
    ),
    items=extend_schema(
        summary="Get all cart items",
        description="Returns all products in the cart (for authenticated users or stored in session).",
        responses={
            200: CartSerializer,
        },
    ),
    checkout=extend_schema(
        summary="Checkout the cart",
        description="Processes the cart checkout. If the user is authenticated, an order is created in the database "
                    "and payment is processed; otherwise, it works with the session.",
        responses={
            201: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
    ),
)
class CartViewSet(GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=False, methods=['post'], url_path='add-to-cart')
    def add(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart = request.user.cart
            cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
            if created:
                cart_item.amount = 1
            else:
                cart_item.amount += 1
            cart_item.save()
        else:
            cart = request.session.get(settings.CART_SESSION_ID, default={})
            cart[str(product_id)] = cart.get(str(product_id), 0) + 1
            request.session[settings.CART_SESSION_ID] = cart
            request.session.modified = True

        return Response({'message': f'product №{product_id} is successfully added to cart'}, status=200)

    @action(detail=False, methods=['get'], url_path='get-cart-items/', serializer_class=CartSerializer)
    def items(self, request):
        if request.user.is_authenticated:
            cart = request.user.cart
            return Response(CartSerializer(cart).data)
        else:
            cart = request.session.get(settings.CART_SESSION_ID, default={})
            products = Product.objects.filter(id__in=cart.keys())
            items = []
            total = 0
            for product in products:
                data = ProductSerializer(product).data
                amount = cart.get(str(product.id))
                item_total = product.discount_price if product.discount_price is not None else product.price
                item_total *= amount
                items.append({
                    'product': data,
                    'amount': amount,
                    'item_total': item_total,
                    'cart': None,
                })
                total += item_total
            return Response({'user': None, 'created_at': None, 'items': items, 'total': total})

    @action(detail=False, methods=['post'], url_path='cart-checkout/')
    def checkout(self, request):
        if request.user.is_authenticated:
            cart = request.user.cart
            if not cart or cart.items.count() == 0:
                return Response({'error': 'Cart is empty'}, status=400)
        else:
            cart = request.session.get(settings.CART_SESSION_ID, default={})
            if not cart:
                return Response({'error': 'Cart is empty'}, status=400)

        form = OrderCreateForm(request.data)
        if not form.is_valid():
            return Response({'errors': form.errors}, status=400)

        order = form.save(commit=False)
        if request.user.is_authenticated:
            order.user = request.user
        order.save()

        if request.user.is_authenticated:
            cart_items = order.user.cart.items.select_related('product').all()
            items = OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product=item.product,
                    amount=item.amount,
                    price=item.product.discount_price if item.product.discount_price is not None else item.product.price
                )
                for item in cart_items
            ])
        else:
            cart_items = [{'product': Product.objects.get(id=int(p_id)), 'amount': a} for p_id, a in cart.items()]
            items = OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product=item['product'],
                    amount=item['amount'],
                    price=item['product'].discount_price if item['product'].discount_price is not None else item['product'].price
                )
                for item in cart_items
            ])

        method = form.cleaned_data['payment_method']
        total = sum(item.price * item.amount for item in items)

        if method != 'cash':
            Payment.objects.create(order=order, provider=method, amount=total)
        else:
            order.status = Order.Status.PROCESSING
            order.save()

        if request.user.is_authenticated:
            request.user.cart.items.all().delete()
        else:
            cart.clear()
            request.session[settings.CART_SESSION_ID] = cart
            request.session.modified = True

        send_order_confirmation_email(order=order)

        return Response({'message': f'Order №{order.id} is created'}, status=201)
