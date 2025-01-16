from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from main.models.order import Order, OrderItem
from main.models.base_models import Product, Category, Brand
from main.serializers import ProductSerializer, CategorySerializer
from .serializers import OrderSerializer, OrderItemSerializer
import stripe
from django.conf import settings
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = CategorySerializer  # Nous utiliserons le même serializer pour l'instant
    permission_classes = [IsAuthenticated]

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        order = get_object_or_404(Order, id=pk, user=request.user)
        
        try:
            # Créer l'intention de paiement Stripe
            intent = stripe.PaymentIntent.create(
                amount=int(order.total * 100),  # Stripe utilise les centimes
                currency='eur',
                customer=request.user.stripe_customer_id,
                metadata={'order_id': str(order.id)}
            )
            
            return Response({
                'clientSecret': intent.client_secret
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Calculer les totaux
        items_data = self.request.data.get('items', [])
        subtotal = Decimal('0')
        
        # Vérifier le stock
        for item in items_data:
            product = get_object_or_404(Product, id=item['product'])
            if product.stock < item['quantity']:
                raise serializers.ValidationError(
                    f"Not enough stock for product {product.name}. "
                    f"Only {product.stock} available."
                )
            subtotal += product.price * Decimal(str(item['quantity']))
        
        # Calculer TVA et frais de livraison
        tax = subtotal * Decimal('0.20')  # TVA 20%
        shipping_cost = Decimal('0') if subtotal > 50 else Decimal('5.99')
        total = subtotal + tax + shipping_cost
        
        # Créer la commande
        order = serializer.save(
            user=self.request.user,
            subtotal=subtotal,
            tax=tax,
            shipping_cost=shipping_cost,
            total=total
        )
        
        # Créer les items et mettre à jour le stock
        for item_data in items_data:
            product = get_object_or_404(Product, id=item_data['product'])
            quantity = item_data['quantity']
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            
            # Mettre à jour le stock
            product.stock -= quantity
            product.save()
        
        return order
