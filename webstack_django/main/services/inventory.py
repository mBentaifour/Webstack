from django.db import transaction
from django.core.exceptions import ValidationError
from main.models.base_models import Product
from main.models.order import Order, OrderItem

class InventoryService:
    @staticmethod
    @transaction.atomic
    def reserve_stock(order_id):
        """Réserve le stock pour une commande"""
        order = Order.objects.select_for_update().get(id=order_id)
        
        if order.status != 'pending':
            raise ValidationError("Can only reserve stock for pending orders")
            
        for item in order.items.all():
            product = Product.objects.select_for_update().get(id=item.product.id)
            
            if product.stock < item.quantity:
                raise ValidationError(f"Not enough stock for product {product.name}")
                
            product.stock -= item.quantity
            product.save()
            
        order.status = 'processing'
        order.save()
        
        return True

    @staticmethod
    @transaction.atomic
    def release_stock(order_id):
        """Libère le stock réservé si la commande est annulée"""
        order = Order.objects.select_for_update().get(id=order_id)
        
        if order.status not in ['processing', 'failed']:
            raise ValidationError("Can only release stock for processing or failed orders")
            
        for item in order.items.all():
            product = Product.objects.select_for_update().get(id=item.product.id)
            product.stock += item.quantity
            product.save()
            
        order.status = 'cancelled'
        order.save()
        
        return True

    @staticmethod
    def check_stock_availability(items):
        """Vérifie la disponibilité du stock pour une liste d'articles"""
        unavailable_items = []
        
        for item in items:
            product = Product.objects.get(id=item['product_id'])
            if product.stock < item['quantity']:
                unavailable_items.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'requested_quantity': item['quantity'],
                    'available_quantity': product.stock
                })
                
        return len(unavailable_items) == 0, unavailable_items

    @staticmethod
    def get_low_stock_products(threshold=10):
        """Récupère les produits dont le stock est bas"""
        return Product.objects.filter(stock__lte=threshold)
