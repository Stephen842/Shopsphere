from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError

from .models import Category, Product, Cart, CartItem, Order
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer
from .filters import ProductFilter


# -----------------------------
# CATEGORY ViewSet
# -----------------------------
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


# -----------------------------
# PRODUCT ViewSet
# -----------------------------
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']


# -----------------------------
# CART ViewSet
# -----------------------------
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def list(self, request):
        cart = self.get_cart(request.user)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def add(self, request):
        cart = self.get_cart(request.user)

        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            raise ValidationError({'product_id': "This field is required."})
        
        if quantity < 1:
            raise ValidationError({'quantity': 'Quantity must be at least 1.'})
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            raise ValidationError({'product': 'Product is not found.'})
        
        if product.stock < quantity:
            raise ValidationError({'stock': 'Insufficient stock available.'})

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={'quantity': quantity}
        )

        if not created:
            item.quantity += quantity
            if item.quantity > product.stock:
                raise ValidationError({'stock': 'Insufficient stock available.'})
            item.save()

        return Response({'detail': 'Product added to cart.'}, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['post'])
    def remove(self, request):
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')

        if not product_id:
            raise ValidationError({'product_id': "This field is required."})
        
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response({'detail': 'Product removed from cart.'})
    

    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart = self.get_cart(request.user)
        cart.clear()
        return Response({'detail': 'Cart cleared.'})


# -----------------------------
# ORDER ViewSet
# -----------------------------
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items__product")

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        if not cart.items.exists():
            return Response({'detail': 'Your cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.create_from_cart(cart)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)