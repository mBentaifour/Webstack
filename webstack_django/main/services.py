from .db_manager import db
from .models import SupabaseProduct
from django.core.cache import cache
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class ProductService:
    @staticmethod
    def get_all_products(use_cache=True) -> List[SupabaseProduct]:
        """Récupère tous les produits avec cache optionnel."""
        cache_key = 'all_products'
        
        if use_cache:
            cached_products = cache.get(cache_key)
            if cached_products:
                return [SupabaseProduct(p) for p in cached_products]
        
        try:
            response = db.get_products()
            products = response.data
            if products:
                if use_cache:
                    cache.set(cache_key, products, timeout=300)  # Cache pour 5 minutes
                return [SupabaseProduct(p) for p in products]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des produits: {str(e)}")
        
        return []

    @staticmethod
    def get_product_by_id(product_id: str) -> Optional[SupabaseProduct]:
        """Récupère un produit par son ID."""
        cache_key = f'product_{product_id}'
        
        cached_product = cache.get(cache_key)
        if cached_product:
            return SupabaseProduct(cached_product)
        
        try:
            response = db.get_product(product_id)
            if response.data:
                cache.set(cache_key, response.data, timeout=300)
                return SupabaseProduct(response.data)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du produit {product_id}: {str(e)}")
        
        return None

    @staticmethod
    def get_products_by_category(category: str) -> List[SupabaseProduct]:
        """Récupère les produits par catégorie."""
        try:
            response = db.get_products(category=category)
            if response.data:
                return [SupabaseProduct(p) for p in response.data]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des produits de la catégorie {category}: {str(e)}")
        
        return []

    @staticmethod
    def update_product_stock(product_id: str, quantity: int) -> bool:
        """Met à jour le stock d'un produit."""
        try:
            product = ProductService.get_product_by_id(product_id)
            if not product:
                return False
            
            new_stock = product.stock - quantity
            if new_stock < 0:
                return False
            
            response = db.update_product(product_id, {'stock': new_stock})
            if response.data:
                # Invalider le cache
                cache.delete(f'product_{product_id}')
                cache.delete('all_products')
                return True
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du stock du produit {product_id}: {str(e)}")
        
        return False
