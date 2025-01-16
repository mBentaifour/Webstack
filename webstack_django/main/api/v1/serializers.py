from rest_framework import serializers
from main.models.order import Order, OrderItem
from main.models.base_models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['unit_price', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    items_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'status', 'payment_method',
            'shipping_address', 'billing_address',
            'subtotal', 'tax', 'shipping_cost', 'total',
            'items', 'items_data', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'user', 'subtotal', 'tax', 'shipping_cost',
            'total', 'status', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        items_data = validated_data.pop('items_data', [])
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Vérifier le stock
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for product {product.name}. "
                    f"Only {product.stock} available."
                )
            
            # Créer l'item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price,
                total_price=product.price * quantity
            )
            
            # Mettre à jour le stock
            product.stock -= quantity
            product.save()
        
        return order
