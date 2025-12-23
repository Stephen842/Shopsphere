from rest_framework import serializers
from .models import Category, Product, Cart, CartItem, Order, OrderItem


# -----------------------------
# CATEGORY SERIALIZER
# -----------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


# -----------------------------
# PRODUCT SERIALIZER
# -----------------------------
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()  # shows category name

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description',
            'price', 'stock', 'image',
            'category', 'created_at', 'updated_at', 'is_active'
        ]


# -----------------------------
# CART ITEM SERIALIZER
# -----------------------------
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'quantity', 'added_at', 'subtotal'
        ]

    def get_subtotal(self, obj):
        return obj.subtotal()


# -----------------------------
# CART SERIALIZER
# -----------------------------
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'items', 'total', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user']

    def get_total(self, obj):
        return obj.total()


# -----------------------------
# ORDER ITEM SERIALIZER
# -----------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


# -----------------------------
# ORDER SERIALIZER
# -----------------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'uuid', 'user', 'status', 'total_amount',
            'created_at', 'updated_at', 'placed_at', 'items'
        ]
        read_only_fields = ['uuid', 'user', 'total_amount']
