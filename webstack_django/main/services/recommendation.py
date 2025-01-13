from django.db.models import Count, Avg
from main.models.base_models import Product
from main.models.order import Order
from main.models.review import Review

class RecommendationService:
    @staticmethod
    def get_popular_products(limit=10):
        """Récupère les produits les plus populaires basés sur les ventes"""
        return Product.objects.annotate(
            total_sales=Count('orderitem')
        ).order_by('-total_sales')[:limit]

    @staticmethod
    def get_trending_products(days=7, limit=10):
        """Récupère les produits tendance basés sur les ventes récentes"""
        from django.utils import timezone
        from datetime import timedelta
        
        recent_date = timezone.now() - timedelta(days=days)
        
        return Product.objects.filter(
            orderitem__order__created_at__gte=recent_date
        ).annotate(
            recent_sales=Count('orderitem')
        ).order_by('-recent_sales')[:limit]

    @staticmethod
    def get_related_products(product_id, limit=5):
        """Récupère les produits similaires basés sur la catégorie et les tags"""
        product = Product.objects.get(id=product_id)
        
        return Product.objects.filter(
            category=product.category
        ).exclude(
            id=product_id
        ).order_by('?')[:limit]

    @staticmethod
    def get_frequently_bought_together(product_id, limit=3):
        """Récupère les produits souvent achetés ensemble"""
        # Trouver les commandes contenant ce produit
        orders = Order.objects.filter(
            items__product_id=product_id
        )
        
        # Trouver les autres produits dans ces commandes
        related_products = Product.objects.filter(
            orderitem__order__in=orders
        ).exclude(
            id=product_id
        ).annotate(
            frequency=Count('id')
        ).order_by('-frequency')[:limit]
        
        return related_products

    @staticmethod
    def get_personalized_recommendations(user_id, limit=10):
        """Génère des recommandations personnalisées basées sur l'historique d'achat"""
        # Trouver les catégories préférées de l'utilisateur
        favorite_categories = Product.objects.filter(
            orderitem__order__user_id=user_id
        ).values(
            'category'
        ).annotate(
            count=Count('category')
        ).order_by('-count')
        
        # Trouver les produits bien notés dans ces catégories
        recommended_products = Product.objects.filter(
            category__in=favorite_categories.values('category')
        ).exclude(
            orderitem__order__user_id=user_id
        ).annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(
            avg_rating__gte=4
        ).order_by('-avg_rating')[:limit]
        
        return recommended_products
