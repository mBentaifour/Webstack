from rest_framework import serializers
from .models.base_models import Product, Category, Brand
from .models.order import Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'description']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'items', 'subtotal', 'tax',
            'shipping_cost', 'total', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'user', 'subtotal', 'tax', 'shipping_cost',
            'total', 'status', 'created_at', 'updated_at'
        ]
