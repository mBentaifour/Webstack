from rest_framework import serializers
from main.models.order import Order, OrderItem, Payment
from main.models.base_models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['unit_price', 'total_price']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value

    def validate(self, data):
        # Vérifier le stock disponible
        product = data['product']
        quantity = data['quantity']
        
        if product.stock < quantity:
            raise serializers.ValidationError(f"Not enough stock. Only {product.stock} items available.")
        
        # Définir le prix unitaire basé sur le prix actuel du produit
        data['unit_price'] = product.price
        return data

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'user_email', 'status', 'status_display',
            'payment_method', 'payment_method_display', 'subtotal', 'tax',
            'shipping_cost', 'total', 'shipping_address', 'billing_address',
            'notes', 'tracking_number', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['order_number', 'user', 'total', 'created_at', 'updated_at']

    def validate_shipping_address(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Shipping address is too short")
        return value

    def validate_billing_address(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Billing address is too short")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        
        # Calculer les totaux
        subtotal = sum(
            item['quantity'] * item['product'].price
            for item in items_data
        )
        
        # Calculer la TVA (20%)
        tax = subtotal * 0.20
        
        # Frais de livraison gratuits au-dessus de 50€
        shipping_cost = 0 if subtotal > 50 else 5.99
        
        validated_data.update({
            'subtotal': subtotal,
            'tax': tax,
            'shipping_cost': shipping_cost,
            'total': subtotal + tax + shipping_cost
        })
        
        order = super().create(validated_data)
        
        # Créer les items de la commande
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                unit_price=item_data['product'].price,
                total_price=item_data['quantity'] * item_data['product'].price
            )
        
        return order

class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_number', 'amount', 'payment_method',
            'payment_method_display', 'status', 'status_display',
            'transaction_id', 'payment_details', 'error_message',
            'refund_reason', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'transaction_id', 'status', 'error_message',
            'refund_reason', 'created_at', 'updated_at'
        ]

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Payment amount must be greater than 0")
        
        # Vérifier que le montant correspond au total de la commande
        order = data['order']
        if data['amount'] != order.total:
            raise serializers.ValidationError(
                f"Payment amount ({data['amount']}) does not match order total ({order.total})"
            )
        
        return data
