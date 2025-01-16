from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Inventory

def check_low_stock(category=None, brand=None):
    """
    Vérifie les produits dont le stock est inférieur au seuil d'alerte.
    Peut être filtré par catégorie ou marque.
    """
    queryset = Product.objects.all()
    
    if category:
        queryset = queryset.filter(category=category)
    if brand:
        queryset = queryset.filter(brand=brand)
    
    return [
        product for product in queryset
        if product.stock < product.min_stock_alert
    ]

def send_stock_alert(product):
    """
    Envoie une alerte par email pour un produit en stock bas.
    """
    subject = f'Alerte stock bas - {product.name}'
    message = f"""
    Le produit {product.name} est en stock bas.
    
    Stock actuel : {product.stock}
    Seuil d'alerte : {product.min_stock_alert}
    
    Veuillez réapprovisionner ce produit dès que possible.
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.STOCK_ALERT_EMAIL],
        fail_silently=False,
    )

def process_stock_movement(product, quantity, reason, notes, user):
    """
    Enregistre un mouvement de stock et met à jour le stock du produit.
    Retourne le mouvement créé.
    """
    movement = Inventory.objects.create(
        product=product,
        quantity_changed=quantity,
        reason=reason,
        notes=notes,
        recorded_by=user
    )
    
    product.stock += quantity
    product.save()
    
    # Si le stock est bas après le mouvement, envoyer une alerte
    if product.stock < product.min_stock_alert:
        send_stock_alert(product)
    
    return movement

def generate_stock_report(category=None, brand=None):
    """
    Génère un rapport sur l'état des stocks.
    Peut être filtré par catégorie ou marque.
    """
    products = Product.objects.all()
    if category:
        products = products.filter(category=category)
    if brand:
        products = products.filter(brand=brand)
    
    low_stock = []
    total_value = 0
    
    for product in products:
        total_value += product.price * product.stock
        
        if product.stock < product.min_stock_alert:
            product_info = {
                'name': product.name,
                'stock': product.stock,
                'min_stock_alert': product.min_stock_alert,
                'price': float(product.price),
                'total_value': float(product.price * product.stock)
            }
            low_stock.append(product_info)
    
    # Les produits en rupture sont inclus dans low_stock,
    # mais on les compte séparément pour les statistiques
    out_of_stock_count = sum(1 for p in low_stock if p['stock'] == 0)
    
    # Récupérer les mouvements de stock récents
    recent_movements = Inventory.objects.filter(
        product__in=products
    ).order_by('-date')[:10]
    
    movements = [{
        'product': movement.product.name,
        'quantity': movement.quantity_changed,
        'reason': movement.reason,
        'date': movement.date,
        'user': movement.recorded_by.username if movement.recorded_by else 'Système'
    } for movement in recent_movements]
    
    summary_text = []
    if low_stock:
        summary_text.append('Produits en stock bas')
        if out_of_stock_count:
            summary_text.append('Produits en rupture de stock')
    if movements:
        summary_text.append('Mouvements de stock récents')
    
    return {
        'summary': {
            'total_products': products.count(),
            'low_stock_count': len(low_stock),
            'out_of_stock_count': out_of_stock_count,
            'total_value': total_value,
            'products_in_stock': products.filter(stock__gt=0).count(),
            'alerts': ' | '.join(summary_text)
        },
        'low_stock': low_stock,
        'movements': movements
    }
