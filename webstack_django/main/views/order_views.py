from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models.order import Order, OrderItem
from ..models.base_models import Product
from decimal import Decimal
from django.db import transaction
from ..serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commandes.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retourne uniquement les commandes de l'utilisateur connecté"""
        return Order.objects.filter(user=self.request.user)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Crée une nouvelle commande avec les articles spécifiés.
        
        Format attendu des données:
        {
            "items": [
                {"product": product_id, "quantity": quantity},
                ...
            ]
        }
        """
        # Valider les données
        items_data = request.data.get('items', [])
        if not items_data:
            return Response(
                {'error': 'No items provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier le stock et calculer les totaux
        subtotal = Decimal('0')
        items_to_create = []
        
        for item_data in items_data:
            product_id = item_data.get('product')
            quantity = item_data.get('quantity', 1)
            
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {'error': f'Product {product_id} not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Vérifier le stock
            if product.stock < quantity:
                return Response(
                    {'error': f'Insufficient stock for product {product.name}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculer le sous-total
            item_total = product.price * quantity
            subtotal += item_total
            
            items_to_create.append({
                'product': product,
                'quantity': quantity,
                'price': product.price
            })
        
        # Calculer les taxes et frais de livraison
        tax = subtotal * Decimal('0.20')  # TVA 20%
        shipping_cost = Decimal('0') if subtotal >= Decimal('50') else Decimal('5.99')
        total = subtotal + tax + shipping_cost
        
        # Créer la commande
        order = Order.objects.create(
            user=request.user,
            subtotal=subtotal,
            tax=tax,
            shipping_cost=shipping_cost,
            total=total
        )
        
        # Créer les articles de la commande et mettre à jour le stock
        for item in items_to_create:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )
            
            # Mettre à jour le stock
            product = item['product']
            product.stock -= item['quantity']
            product.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
